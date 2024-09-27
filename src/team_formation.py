from collections import defaultdict
from datetime import datetime
import logging

from sqlalchemy.orm import joinedload

from src import db
from src.models import Resource, Project, Team
from src.utils import level_to_numeric  # Ensure this function exists in src/utils.py

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def is_level_sufficient(resource_level, required_level):
    levels = ['beginner', 'intermediate', 'expert']
    try:
        resource_index = levels.index(resource_level.lower())
        required_index = levels.index(required_level.lower())
        return resource_index >= required_index
    except ValueError:
        return False


def get_resource_skills_with_levels(resource):
    skills_with_levels = {}
    for skill in resource.Skills:
        skill_name, skill_level = skill.split(':')
        skills_with_levels[skill_name.strip().lower()] = skill_level.strip().lower()
    return skills_with_levels


def find_best_team_for_project(project, resources, org_id=None):
    logger.info(f"Starting to find a team for project: {project.ProjectName}")
    
    required_resources = project.RequiredResources
    project_start_date = project.ProjectStartDate or datetime.strptime('2023-01-01', '%Y-%m-%d')

    team_resource_ids = []
    unfilled_roles = {}

    for resource_requirement in required_resources:
        role = resource_requirement.get('Role')
        required_skills = resource_requirement.get('Skills', [])
        quantity = resource_requirement.get('Quantity', 1)

        if not role or not required_skills:
            unfilled_roles[role] = unfilled_roles.get(role, 0) + quantity
            continue

        candidates = []
        for resource in resources:
            if resource.ResourceID in team_resource_ids:
                continue  # Ensure resource is only in one team
            if org_id and resource.OrgID != org_id:
                continue

            resource_skills = get_resource_skills_with_levels(resource)
            logger.info(f"Checking resource {resource.Name} with skills: {resource_skills}")

            # Check if resource has all required skills with sufficient levels
            has_all_skills = True
            for skill in required_skills:
                skill_name, required_level = skill.split(':')
                resource_level = resource_skills.get(skill_name.strip().lower(), 'beginner')
                logger.info(f"Checking if {resource.Name} has skill {skill_name.strip()} at required level {required_level.strip()}")
                if not is_level_sufficient(resource_level, required_level.strip()):
                    has_all_skills = False
                    break

            if has_all_skills and resource.AvailableDate <= project_start_date:
                candidates.append(resource)

        if not candidates:
            unfilled_roles[role] = unfilled_roles.get(role, 0) + quantity
            continue

        # Sort candidates based on rate (lower is better)
        candidates.sort(key=lambda x: x.Rate)

        for _ in range(quantity):
            if not candidates:
                unfilled_roles[role] = unfilled_roles.get(role, 0) + (quantity - len(team_resource_ids))
                break
            selected_resource = candidates.pop(0)
            team_resource_ids.append(selected_resource.ResourceID)
            logger.info(f"Assigned resource '{selected_resource.Name}' to role '{role}' in project '{project.ProjectName}'.")

    total_resources = len(team_resource_ids)

    existing_team = Team.query.filter_by(ProjectID=project.ProjectID).first()
    if existing_team:
        existing_team.ResourceIDs = team_resource_ids
        existing_team.TotalResources = total_resources
        logger.info(f"Updated team for project '{project.ProjectName}' with {total_resources} resources.")
    else:
        new_team = Team(
            ProjectID=project.ProjectID,
            ResourceIDs=team_resource_ids,
            TotalResources=total_resources,
            OrgID=project.OrgID
        )
        db.session.add(new_team)
        logger.info(f"Created team for project '{project.ProjectName}' with {total_resources} resources.")

    return team_resource_ids, unfilled_roles


def match_resources_to_projects():
    """
    Assigns resources to projects based on skill matching, experience, and availability.

    Returns:
        tuple: (project_assignments dict, unfilled_roles_overall dict)
    """
    project_assignments = defaultdict(list)
    unfilled_roles_overall = defaultdict(int)

    try:
        # Fetch all resources with their skills
        resources = Resource.query.all()
        logger.info(f"Fetched {len(resources)} resources from the database.")

        # Fetch all projects
        projects = Project.query.all()
        logger.info(f"Fetched {len(projects)} projects from the database.")

        # Iterate over each project to assign resources
        for project in projects:
            logger.info(f"Processing project: {project.ProjectName}")

            # Use the find_best_team_for_project function
            team_resource_ids, unfilled_roles = find_best_team_for_project(project, resources, org_id=project.OrgID)

            # Assign team members to the project
            for resource_id in team_resource_ids:
                resource = Resource.query.get(resource_id)
                if resource:
                    project_assignments[project.ProjectName].append({'Resource': resource.Name})

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
    project_assignments, unfilled_roles = match_resources_to_projects()

    # Display the project assignments
    print("Project Assignments:\n")
    for project, members in project_assignments.items():
        print(f"Project: {project}")
        for member in members:
            print(f" - {member['Resource']}")
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
