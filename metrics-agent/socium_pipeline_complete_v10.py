"""
Socium HR-Tech
Pipeline MongoDB → Datadog
KPIs: Job, Documents, Payroll, Performance, Workflows, System
"""

import os
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries
from dotenv import load_dotenv

load_dotenv()


class SociumDataPipeline:

    def __init__(self):
        # MongoDB
        self.mongo = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.mongo[os.getenv("MONGODB_DATABASE", "socium")]

        # Datadog
        config = Configuration()
        config.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
        config.api_key["appKeyAuth"] = os.getenv("DATADOG_APP_KEY")
        config.server_variables["site"] = os.getenv("DATADOG_SITE", "datadoghq.com")

        self.dd = MetricsApi(ApiClient(config))
        self.sent = 0
        self.failed = 0

    # ---------- CORE ----------
    def send_metric(self, name, value, tags=None, timestamp=None):
        if value is None:
            self.failed += 1
            return

        try:
            value = float(value)
        except:
            self.failed += 1
            return

        tags = tags or []
        tags += ["env:dev", "source:mongo", "app:socium"]

        ts = int(timestamp or time.time())

        payload = MetricPayload(series=[
            MetricSeries(
                metric=f"socium.v10.{name}",
                type=MetricIntakeType.GAUGE,
                points=[MetricPoint(timestamp=ts, value=value)],
                tags=tags
            )
        ])

        try:
            self.dd.submit_metrics(body=payload)
            self.sent += 1
        except:
            self.failed += 1

    # ================= JOB =================
    def extract_job_kpis(self):
        print("💼 JOB KPIs")

        # Nombre de candidatures par jour
        pipeline = [
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$applied_at"}},
                "count": {"$sum": 1}
            }}
        ]
        for d in self.db.applications.aggregate(pipeline):
            ts = int(datetime.strptime(d["_id"], "%Y-%m-%d").timestamp())
            self.send_metric("job.applications.count", d["count"], ["granularity:day"], ts)

        # Funnel
        for d in self.db.applications.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]):
            self.send_metric("job.funnel", d["count"], [f"status:{d['_id']}"])

        # Volume par poste
        for d in self.db.job_postings.aggregate([
            {"$group": {"_id": "$title", "count": {"$sum": 1}}}
        ]):
            self.send_metric("job.postings.by_title", d["count"], [f"title:{d['_id']}"])

    # ================= DOCUMENTS =================
    def extract_document_kpis(self):
        print("📄 DOCUMENT KPIs")

        for d in self.db.documents.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]):
            self.send_metric("documents.count", d["count"], [f"status:{d['_id']}"])

        expired = self.db.documents.count_documents({"status": "expired"})
        self.send_metric("documents.expired", expired)

    # ================= PAYROLL =================
    def extract_payroll_kpis(self):
        print("💰 PAYROLL KPIs")

        pipeline = [
            {"$group": {
                "_id": "$period",
                "gross": {"$sum": "$gross_salary"},
                "net": {"$sum": "$net_salary"},
                "count": {"$sum": 1}
            }}
        ]
        for d in self.db.payrolls.aggregate(pipeline):
            self.send_metric("payroll.bulletins.count", d["count"], [f"period:{d['_id']}"])
            self.send_metric("payroll.gross_salary", d["gross"], [f"period:{d['_id']}"])
            self.send_metric("payroll.net_salary", d["net"], [f"period:{d['_id']}"])

    # ================= PERFORMANCE =================
    def extract_performance_kpis(self):
        print("⭐ PERFORMANCE KPIs")

        r = list(self.db.performance_reviews.aggregate([
            {"$group": {
                "_id": None,
                "avg": {"$avg": "$score"},
                "count": {"$sum": 1}
            }}
        ]))
        if r:
            self.send_metric("performance.avg_score", r[0]["avg"])
            self.send_metric("performance.reviews.count", r[0]["count"])

    # ================= WORKFLOWS =================
    def extract_workflow_kpis(self):
        print("🔄 WORKFLOW KPIs")

        for d in self.db.workflows.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]):
            self.send_metric("workflows.count", d["count"], [f"status:{d['_id']}"])

        pending = self.db.workflows.count_documents({"status": "pending"})
        self.send_metric("workflows.pending", pending)

    # ================= SYSTEM =================
    def extract_system_kpis(self):
        print("📊 SYSTEM KPIs")

        for col in [
            "companies", "employees", "applications",
            "job_postings", "documents",
            "payrolls", "performance_reviews", "workflows"
        ]:
            count = self.db[col].count_documents({})
            self.send_metric("system.collection.count", count, [f"collection:{col}"])

    # ================= RUN =================
    def run(self):
        start = time.time()
        self.extract_job_kpis()
        self.extract_document_kpis()
        self.extract_payroll_kpis()
        self.extract_performance_kpis()
        self.extract_workflow_kpis()
        self.extract_system_kpis()

        print("=" * 50)
        print(f"✅ DONE in {time.time() - start:.2f}s")
        print(f"📤 Sent: {self.sent}")
        print(f"❌ Failed: {self.failed}")
        print("=" * 50)


if __name__ == "__main__":
    SociumDataPipeline().run()
