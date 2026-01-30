"""
Socium HR-Tech - Générateur simplifié pour KPIs
Génère les 5 produits: Job, Doc, Payroll, Perf, Workflow
Insertion directe dans MongoDB
"""

import os
import sys
import random
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
from faker import Faker
import logging
from pymongo import MongoClient

# ----- CONFIGURATION -----
NUM_COMPANIES = 10
MAX_EMPLOYEES_PER_COMPANY = 50
MAX_JOB_POSTINGS = 5
MAX_APPLICATIONS = 15
MAX_DOCS = 10
MAX_PAYROLL_MONTHS = 6
MAX_PERF_REVIEWS = 3
MAX_WORKFLOWS = 5

DEPARTMENTS = ['RH', 'IT', 'Finance', 'Commercial', 'Marketing', 'Ops']
JOB_TITLES = {
    'IT': ['Dev', 'Data Analyst', 'DevOps'],
    'RH': ['Chargé RH', 'DRH'],
    'Finance': ['Comptable', 'DAF'],
    'Commercial': ['Commercial', 'Business Dev'],
    'Marketing': ['Chef de Produit', 'CMO'],
    'Ops': ['Responsable Ops', 'Chef de Projet']
}
DOCUMENT_TYPES = ['Contrat', 'Avenant', 'Fiche de Paie', 'Certificat']
WORKFLOW_TYPES = ['Congé', 'Note de Frais', 'Formation', 'Augmentation']

APPLICATION_STATUSES = ['applied', 'screening', 'interview', 'offer', 'hired', 'rejected']
DOCUMENT_STATUSES = ['draft', 'pending', 'signed', 'archived', 'expired']

fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

# ----- LOGGING -----
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ----- UTILITAIRES -----
def gen_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# ----- GÉNÉRATEUR -----
def generate_data():
    data = defaultdict(list)
    
    for _ in range(NUM_COMPANIES):
        company = {
            'id': gen_id('CLI'),
            'name': fake.company(),
            'city': fake.city(),
            'country': fake.country(),
            'employees': []
        }
        num_emps = random.randint(5, MAX_EMPLOYEES_PER_COMPANY)
        
        # Employés
        for _ in range(num_emps):
            dept = random.choice(DEPARTMENTS)
            emp = {
                'id': gen_id('EMP'),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'department': dept,
                'position': random.choice(JOB_TITLES.get(dept, ['Employé'])),
                'hire_date': fake.date_time_between(start_date='-2y', end_date='now'),
                'status': random.choices(['active','on_leave','terminated'], weights=[85,10,5])[0]
            }
            company['employees'].append(emp)
            data['employees'].append(emp)
        
        data['companies'].append(company)
        
        # JOB
        for _ in range(random.randint(1, MAX_JOB_POSTINGS)):
            posting = {
                'id': gen_id('JOB'),
                'client_id': company['id'],
                'title': random.choice(JOB_TITLES[random.choice(DEPARTMENTS)]),
                'department': random.choice(DEPARTMENTS),
                'posted_at': fake.date_time_between(start_date='-1y', end_date='now'),
                'status': random.choice(['open','closed']),
                'applications': []
            }
            for _ in range(random.randint(3, MAX_APPLICATIONS)):
                app = {
                    'id': gen_id('APP'),
                    'job_posting_id': posting['id'],
                    'candidate_name': fake.name(),
                    'status': random.choice(APPLICATION_STATUSES),
                    'applied_at': fake.date_time_between(start_date=posting['posted_at'], end_date='now')
                }
                posting['applications'].append(app)
                data['applications'].append(app)
            data['job_postings'].append(posting)
        
        # Documents
        for emp in company['employees']:
            for _ in range(random.randint(1, MAX_DOCS)):
                doc = {
                    'id': gen_id('DOC'),
                    'employee_id': emp['id'],
                    'type': random.choice(DOCUMENT_TYPES),
                    'status': random.choice(DOCUMENT_STATUSES),
                    'created_at': fake.date_time_between(start_date=emp['hire_date'], end_date='now')
                }
                data['documents'].append(doc)
        
        # Payroll
        for month in range(MAX_PAYROLL_MONTHS):
            for emp in company['employees']:
                payroll = {
                    'id': gen_id('PAY'),
                    'employee_id': emp['id'],
                    'period': (datetime.now() - timedelta(days=30*month)).strftime('%Y-%m'),
                    'gross_salary': random.randint(200_000, 1_000_000),
                    'net_salary': random.randint(150_000, 900_000)
                }
                data['payrolls'].append(payroll)
        
        # Performance
        for emp in company['employees']:
            for _ in range(random.randint(1, MAX_PERF_REVIEWS)):
                review = {
                    'id': gen_id('REV'),
                    'employee_id': emp['id'],
                    'review_date': fake.date_time_between(start_date=emp['hire_date'], end_date='now'),
                    'score': random.randint(1,5)
                }
                data['performance_reviews'].append(review)
        
        # Workflows
        for emp in company['employees']:
            for _ in range(random.randint(1, MAX_WORKFLOWS)):
                wf = {
                    'id': gen_id('WF'),
                    'employee_id': emp['id'],
                    'type': random.choice(WORKFLOW_TYPES),
                    'status': random.choice(['pending','approved','rejected']),
                    'created_at': fake.date_time_between(start_date=emp['hire_date'], end_date='now')
                }
                data['workflows'].append(wf)
    
    return data

# ----- MAIN -----
if __name__ == "__main__":
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        logger.error("❌ Variable MONGODB_URI non définie")
        sys.exit(1)
    
    try:
        # Génération
        logger.info("Génération des données...")
        data = generate_data()
        
        # Connexion MongoDB
        logger.info("Connexion à MongoDB...")
        client = MongoClient(mongodb_uri)
        db = client.get_database()
        
        # Nettoyage collections
        for col in data.keys():
            db[col].delete_many({})
            logger.info(f"Collection {col} nettoyée")
        
        # Insertion
        for col, items in data.items():
            if items:
                db[col].insert_many(items)
                logger.info(f"{len(items)} documents insérés dans {col}")
        
        client.close()
        logger.info("🎉 Génération et insertion terminées avec succès!")
        logger.info(f"📊 Entreprises: {len(data['companies'])}")
        logger.info(f"👥 Employés: {len(data['employees'])}")
        logger.info(f"💼 JOB: {len(data['job_postings'])}, candidatures: {len(data['applications'])}")
        logger.info(f"📄 Documents: {len(data['documents'])}")
        logger.info(f"💰 Payrolls: {len(data['payrolls'])}")
        logger.info(f"⭐ Performance Reviews: {len(data['performance_reviews'])}")
        logger.info(f"🔄 Workflows: {len(data['workflows'])}")
    
    except Exception as e:
        logger.error("❌ Erreur fatale: %s", e, exc_info=True)
        sys.exit(1)
