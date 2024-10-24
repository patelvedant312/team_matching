# app/services/team_formation.py

from collections import defaultdict
from decimal import Decimal
import logging
from munkres import Munkres

from app.models import db
from app.models import Resource, Project, Team

# Import utility functions (adjust the import path if necessary)
from app.services.utils import level_to_numeric, get_resource_skills_with_levels, calculate_weight

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def is_level_sufficient(resource_level, required_level):
    """
    Determines if the resource's skill level meets or exceeds the required level.
    """
    levels = ['beginner', 'intermediate', 'expert']
    try:
        resource_index = levels.index(resource_level.lower())
        required_index = levels.index(required_level.lower())
        return resource_index >= required_index
    except ValueError:
        # If either level is not recognized, treat as insufficient
        return False

def build_cost_matrix(projects, resources, weights):
    """
    Builds a cost matrix for the Hungarian algorithm.
    Rows represent project roles, and columns represent resources.
    """
    cost_matrix = []
    role_list = []
    resource_list = resources  # Use the passed resources list directly

    for project in projects:
        for req in project.RequiredResources:
            role = req['Role']
            skills = req['Skills']
            quantity = req['Quantity']
            for _ in range(quantity):
                role_list.append((project, req))

    for role in role_list:
        row = []
        project, req = role
        required_skills = req['Skills']
        for resource in resource_list:
            # Skip resources already assigned to a team
            if not resource.OnBench:
                cost = Decimal('1000000')  # High cost to discourage assignment
            else:
                resource_skills = get_resource_skills_with_levels(resource)
                # Check if resource has all required skills with sufficient levels
                has_all_skills = all(
                    is_level_sufficient(
                        resource_skills.get(skill.lower(), 'beginner'),
                        details['level'].lower()
                    )
                    for skill, details in required_skills.items()
                )
                # We can remove the availability check here since resources are already filtered
                if has_all_skills:
                    # Calculate weight based on desired parameters
                    weight = calculate_weight(resource, req, project)
                    # Since Munkres finds minimum cost, invert the weight
                    cost = -weight
                else:
                    # Assign a large positive cost to discourage assignment
                    cost = Decimal('1000000')
            row.append(cost)
        cost_matrix.append(row)

    return cost_matrix, role_list, resource_list

def find_optimal_assignment(projects, resources, weights):
    """
    Uses the Hungarian algorithm to find the optimal assignment.
    """
    cost_matrix, role_list, resource_list = build_cost_matrix(projects, resources, weights)
    m = Munkres()
    try:
        indexes = m.compute(cost_matrix)
    except Exception as e:
        logger.error(f"Error in Munkres algorithm: {e}")
        raise e
    assignments = []
    unfilled_roles = defaultdict(int)

    for row, column in indexes:
        if cost_matrix[row][column] < Decimal('1000000'):
            project, req = role_list[row]
            resource = resource_list[column]
            assignments.append((project, req, resource))
        else:
            project, req = role_list[row]
            unfilled_roles[req['Role']] += 1

    return assignments, unfilled_roles

def match_resources_to_projects(project_id, resources):
    """
    Assigns resources to a specific project using the Hungarian algorithm.
    """
    project_assignments = defaultdict(list)
    unfilled_roles_overall = defaultdict(int)
    
    try:
        # Fetch the specific project
        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")
        logger.info(f"Processing project '{project.ProjectName}' (ID: {project.ProjectID})")

        # Resources are now passed as a parameter; no need to fetch them here

        if not resources:
            logger.warning(f"No available resources for project '{project.ProjectName}'.")
            return {}, {'message': 'No available resources for this project.'}

        # Define weights for parameters (can be adjusted)
        weights = {
            'rate': Decimal('1.0'),
            'experience': Decimal('1.0'),
            'skill_level': Decimal('1.0')
            # Add more parameters and weights as needed
        }

        # Find optimal assignments for this project
        assignments, unfilled_roles = find_optimal_assignment([project], resources, weights)

        # Process assignments
        assigned_resource_ids = set()
        for proj, req, resource in assignments:
            if resource.ResourceID not in assigned_resource_ids:
                project_assignments[proj.ProjectName].append(resource)
                assigned_resource_ids.add(resource.ResourceID)
                logger.info(f"Assigned {resource.Name} to project '{proj.ProjectName}' for role '{req['Role']}'.")
            else:
                # Resource already assigned, mark role as unfilled
                unfilled_roles[req['Role']] += 1
                logger.warning(f"Resource {resource.Name} already assigned. Cannot assign to project '{proj.ProjectName}' for role '{req['Role']}'.")

        # Aggregate unfilled roles
        for role, count in unfilled_roles.items():
            unfilled_roles_overall[role] += count
            logger.warning(f"Unfilled role '{role}': {count} position(s).")
        
        # Update the database with team assignments
        assigned_resources = project_assignments.get(project.ProjectName, [])
        total_resources = len(assigned_resources)
        existing_team = Team.query.filter_by(ProjectID=project.ProjectID).first()
        if existing_team:
            # Assign resources to the team by setting their TeamID
            for res in assigned_resources:
                res.TeamID = existing_team.TeamID
            existing_team.TotalResources = total_resources
            logger.info(f"Updated team for project '{project.ProjectName}' with {total_resources} resources.")
            team = existing_team
        else:
            # Create a new team for the project
            new_team = Team(
                ProjectID=project.ProjectID,
                TotalResources=total_resources,
                OrgID=project.OrgID
            )
            db.session.add(new_team)
            db.session.commit()  # Commit to generate TeamID

            # Assign resources to the new team
            for res in assigned_resources:
                res.TeamID = new_team.TeamID
                res.OnBench = False 
            new_team.TotalResources = total_resources
            logger.info(f"Created team for project '{project.ProjectName}' with {total_resources} resources.")
            team = new_team

        # Commit all changes to the database
        db.session.commit()
        logger.info("All team assignments have been committed to the database.")

        # Prepare data to return
        team_data = {
            'TeamID': team.TeamID,
            'ProjectID': project.ProjectID,
            'TotalResources': total_resources,
            'OrgID': project.OrgID,
            'project': project.serialize(),
            'organization': project.organization.serialize(),
            'resources': [res.serialize() for res in assigned_resources]
        }

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred during team assignment: {e}")
        raise e

    return team_data, dict(unfilled_roles_overall)
