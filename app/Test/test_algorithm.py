# src/Test/test_algorithm.py

import logging
from src.Test import create_app, db
from src.Test.team_formation import match_resources_to_projects

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    app = create_app()
    with app.app_context():
        project_assignments, unfilled_roles = match_resources_to_projects()
        logger.info(f"Project Assignments: {project_assignments}")
        logger.info(f"Unfilled Roles: {unfilled_roles}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")