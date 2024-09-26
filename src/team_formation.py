# src/team_formation.py

from collections import defaultdict
from datetime import datetime
import logging

from sqlalchemy.orm import joinedload

from src import db
from src.models import Employee, Project, Skill, employee_skill_association, Team
from src.utils import level_to_numeric  # Ensure this function exists in src/utils.py

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def is_level_sufficient(employee_level, required_level):
    """
    Determines if the employee's skill level meets or exceeds the required level.

    Args:
        employee_level (str): The employee's skill level.
        required_level (str): The required skill level.

    Returns:
        bool: True if sufficient, False otherwise.
    """
    levels = ['beginner', 'intermediate', 'expert']
    try:
        employee_index = levels.index(employee_level.lower())
        required_index = levels.index(required_level.lower())
        return employee_index >= required_index
    except ValueError:
        # If the level is not recognized, treat it as insufficient
        return False

def get_employee_skills_with_levels(employee):
    """
    Retrieves a dictionary of skill names and their corresponding levels for an employee.

    Args:
        employee (Employee): The employee object.

    Returns:
        dict: A dictionary mapping skill names to levels.
    """
    skills_with_levels = {}
    associations = db.session.query(employee_skill_association).filter_by(EmployeeID=employee.EmployeeID).all()
    for assoc in associations:
        skill = Skill.query.get(assoc.SkillID)
        if skill:
            skills_with_levels[skill.SkillName.lower()] = assoc.Level.lower()
    return skills_with_levels

def find_best_team_for_project(project, users, org_id=None):
    """
    Finds the best team for a given project based on required skills, roles, and employee availability.

    Args:
        project (Project): The project to assign a team to.
        users (list): List of Employee objects.
        org_id (int, optional): Organization ID to filter employees. Defaults to None.

    Returns:
        tuple: (team list, unfilled_roles dict)
    """
    required_resources = project.RequiredResources  # List of dicts
    project_domain = project.Domain
    project_start_date = project.ProjectStartDate or datetime.strptime('2023-01-01', '%Y-%m-%d')
    number_of_days = project.NumberOfDays or 0

    team_employee_ids = []
    unfilled_roles = {}

    for resource in required_resources:
        role = resource.get('Role')
        required_level = resource.get('Level', 'beginner')
        required_skills = resource.get('Skills', [])
        quantity = resource.get('Quantity', 1)  # Default to 1 if not specified

        if not role or not required_skills:
            unfilled_roles[role] = unfilled_roles.get(role, 0) + quantity
            continue

        candidates = []
        for user in users:
            if user.EmployeeID in team_employee_ids:
                continue  # Ensure employee is only in one team
            if org_id and user.OrgID != org_id:
                continue

            user_skills = get_employee_skills_with_levels(user)

            # Check if user has all required skills with sufficient levels
            has_all_skills = True
            for skill in required_skills:
                user_level = user_skills.get(skill.lower(), 'beginner')
                if not is_level_sufficient(user_level, required_level):
                    has_all_skills = False
                    break
            if has_all_skills and user.AvailableDate <= project_start_date:
                candidates.append(user)

        if not candidates:
            unfilled_roles[role] = unfilled_roles.get(role, 0) + quantity
            continue

        # Sort candidates based on a scoring system (e.g., lower rate preferred, higher experience)
        # Here, we'll sort by YearsOfExperience descending and Rate ascending
        candidates.sort(key=lambda x: (-x.YearsOfExperience, x.Rate))

        # Assign the required number of employees for the role
        for _ in range(quantity):
            if not candidates:
                unfilled_roles[role] = unfilled_roles.get(role, 0) + (quantity - len(team_employee_ids))
                break
            selected_employee = candidates.pop(0)
            team_employee_ids.append(selected_employee.EmployeeID)
            logger.info(f"Assigned employee '{selected_employee.Name}' to role '{role}' in project '{project.ProjectName}'.")

    total_employees = len(team_employee_ids)

    # Create or update the Team entry
    existing_team = Team.query.filter_by(ProjectID=project.ProjectID).first()
    if existing_team:
        existing_team.EmployeeIDs = team_employee_ids
        existing_team.TotalEmployees = total_employees
        existing_team.OrgID = project.OrgID  # Update OrgID if necessary
        logger.info(f"Updated team for project '{project.ProjectName}' with {total_employees} employees.")
    else:
        new_team = Team(
            ProjectID=project.ProjectID,
            EmployeeIDs=team_employee_ids,
            TotalEmployees=total_employees,
            OrgID=project.OrgID
        )
        db.session.add(new_team)
        logger.info(f"Created team for project '{project.ProjectName}' with {total_employees} employees.")

    return team_employee_ids, unfilled_roles

def match_users_to_projects():
    """
    Assigns employees to projects based on skill matching, experience, and availability.

    Returns:
        tuple: (project_assignments dict, unfilled_roles_overall dict)
    """
    project_assignments = defaultdict(list)
    unfilled_roles_overall = defaultdict(int)

    try:
        # Fetch all employees with their skills
        employees = Employee.query.options(joinedload(Employee.skills)).all()
        logger.info(f"Fetched {len(employees)} employees from the database.")

        # Fetch all projects
        projects = Project.query.all()
        logger.info(f"Fetched {len(projects)} projects from the database.")

        # Iterate over each project to assign employees
        for project in projects:
            logger.info(f"Processing project: {project.ProjectName}")

            # Use the find_best_team_for_project function
            team_employee_ids, unfilled_roles = find_best_team_for_project(project, employees, org_id=project.OrgID)

            # Assign team members to the project
            for emp_id in team_employee_ids:
                employee = Employee.query.get(emp_id)
                if employee:
                    project_assignments[project.ProjectName].append({'Employee': employee.Name})

            # Handle unfilled roles
            for role, count in unfilled_roles.items():
                unfilled_roles_overall[role] += count
                logger.warning(f"Project '{project.ProjectName}' has {count} unfilled positions for role '{role}'.")

        # Commit all team assignments to the database
        db.session.commit()
        logger.info("All team assignments have been committed to the database.")

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred during team assignment: {e}")
        raise e

    return project_assignments, dict(unfilled_roles_overall)

def main():
    """
    Main function to execute the team matching process.
    """
    project_assignments, unfilled_roles = match_users_to_projects()

    # Display the project assignments
    print("Project Assignments:\n")
    for project, members in project_assignments.items():
        print(f"Project: {project}")
        for member in members:
            print(f" - {member['Employee']}")
        print()

    # Display unfilled roles if any
    if unfilled_roles:
        print("Unfilled Roles:")
        for role, count in unfilled_roles.items():
            print(f" - {role}: {count} position(s)")
    else:
        print("All roles have been successfully filled.")

if __name__ == "__main__":
    main()
