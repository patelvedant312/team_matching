# src/cleanup_db.py

from src import create_app, db
from src.models import Employee, Project, Team, Organization, Skill
import logging

def cleanup_database():
    app = create_app()
    with app.app_context():
        try:
            logging.info("Starting database cleanup...")
            
            # Delete in the order of dependencies
            Team.query.delete()
            Project.query.delete()
            Employee.query.delete()
            Skill.query.delete()
            Organization.query.delete()
            
            db.session.commit()
            logging.info("All tables have been cleared successfully.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"An error occurred during database cleanup: {e}")
            raise e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cleanup_database()
