# src/team_formation.py

from collections import defaultdict
from datetime import datetime
import logging
from munkres import Munkres

from .utils import level_to_numeric, get_resource_skills_with_levels, calculate_weight

from src.Test import db
from .models import Resource, Project, Team

from decimal import Decimal

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
    resource_list = []

    for project in projects:
        for req in project.RequiredResources:
            role = req['Role']
            skills = req['Skills']
            quantity = req['Quantity']
            for _ in range(quantity):
                role_list.append((project, req))

    for resource in resources:
        resource_list.append(resource)

    for role in role_list:
        row = []
        project, req = role
        required_skills = req['Skills']
        for resource in resource_list:
            # Skip resources already assigned to a team
            if resource.TeamID is not None:
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
                # Check availability
                available = resource.AvailableDate is not None and resource.AvailableDate <= project.ProjectStartDate
                if has_all_skills and available:
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
    indexes = m.compute(cost_matrix)
    assignments = []
    unfilled_roles = defaultdict(int)

    for row, column in indexes:
        if cost_matrix[row][column] < Decimal('1000000'):
            project, req = role_list[row]
            resource = resource_list[column]
            assignments.append((project, req, resource))
        else:
            project, req = role_list[row]
            unfilled_roles[req['Role']] +=1

    return assignments, unfilled_roles

def match_resources_to_projects():
    """
    Assigns resources to projects using the Hungarian algorithm.
    """
    project_assignments = defaultdict(list)
    unfilled_roles_overall = defaultdict(int)
    
    try:
        # Fetch all resources and projects
        resources = Resource.query.all()
        projects = Project.query.all()
        logger.info(f"Fetched {len(resources)} resources and {len(projects)} projects.")

        # Define weights for parameters (can be adjusted)
        weights = {
            'rate': Decimal('1.0'),
            'experience': Decimal('1.0'),
            'skill_level': Decimal('1.0')
            # Add more parameters and weights as needed
        }

        # Find optimal assignments
        assignments, unfilled_roles = find_optimal_assignment(projects, resources, weights)

        # Process assignments
        assigned_resource_ids = set()
        for project, req, resource in assignments:
            if resource.ResourceID not in assigned_resource_ids:
                project_assignments[project.ProjectName].append(resource.Name)
                assigned_resource_ids.add(resource.ResourceID)
                logger.info(f"Assigned {resource.Name} to project '{project.ProjectName}' for role '{req['Role']}'.")
            else:
                # Resource already assigned, mark role as unfilled
                unfilled_roles[req['Role']] +=1
                logger.warning(f"Resource {resource.Name} already assigned. Cannot assign to project '{project.ProjectName}' for role '{req['Role']}'.")

        # Aggregate unfilled roles
        for role, count in unfilled_roles.items():
            unfilled_roles_overall[role] += count
            logger.warning(f"Unfilled role '{role}': {count} position(s).")
        
        # Update the database with team assignments
        for project in projects:
            assigned_resources = [
                res for res in resources if res.Name in project_assignments.get(project.ProjectName, [])
            ]
            total_resources = len(assigned_resources)
            existing_team = Team.query.filter_by(ProjectID=project.ProjectID).first()
            if existing_team:
                # Assign resources to the team by setting their TeamID
                for res in assigned_resources:
                    res.TeamID = existing_team.TeamID
                existing_team.TotalResources = total_resources
                logger.info(f"Updated team for project '{project.ProjectName}' with {total_resources} resources.")
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
                new_team.TotalResources = total_resources
                logger.info(f"Created team for project '{project.ProjectName}' with {total_resources} resources.")

        # Commit all changes to the database
        db.session.commit()
        logger.info("All team assignments have been committed to the database.")

    except Exception as e:
        db.session.rollback()
        logger.error(f"An error occurred during team assignment: {e}")
        raise e

    return project_assignments, dict(unfilled_roles_overall)