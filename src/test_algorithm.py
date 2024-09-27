# src/test_algorithm.py

from src import create_app, db
from src.team_formation import match_resources_to_projects

def main():
    # Create the Flask application
    app = create_app()
    
    # Use the Flask application context to interact with the database
    with app.app_context():
        try:
            project_assignments, unfilled_roles = match_resources_to_projects()
            
            # Print Project Assignments
            print("Project Assignments:")
            for project, assignments in project_assignments.items():
                print(f"\nProject: {project}")
                for assignment in assignments:
                    print(f" - Employee: {assignment['Employee']}")
            
            # Print Unfilled Roles
            if unfilled_roles:
                print("\nUnfilled Roles:")
                for role, count in unfilled_roles.items():
                    print(f" - Role: {role}, Unfilled Positions: {count}")
            else:
                print("\nAll roles have been successfully filled.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
