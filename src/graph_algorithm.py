# graph_algorithm.py

import networkx as nx
from scipy.optimize import linear_sum_assignment
from utils import generate_adjacency_matrix, calculate_edge_weight

def display_team_user_details(teams):
    for team_name, users in teams.items():
        print(f"Team: {team_name}")
        for user in users:
            skills = ", ".join([f"{skill['name']} ({skill['level']})" for skill in user['skills']])
            print(f"  ID: {user['id']}, Name: {user['name']}, Skills: {skills}, Rate: ${user['rate']}/hr")
        print()  # Blank line for better readability


def match_users_to_projects(users, projects):
    if not users or not projects:
        raise ValueError("Users and projects must not be empty")

    project_assignments = {project['id']: [] for project in projects}

    skill_to_role_map = {
        'Machine Learning': 'data_scientists',
        'Python': 'backend_developers',
        'React': 'frontend_developers',
        'Node.js': 'backend_developers',
        'SQL': 'backend_developers',
        'Java': 'android_developers',
        'Android Development': 'android_developers',
        'Data Analysis': 'data_analysts',
        'Arduino': 'iot_engineers',
        'IoT': 'iot_engineers'
    }

    for project in projects:
        project_id = project['id']
        required_skills = project['required_skills']
        num_of_people_required = project.get('num_of_people_required', {})

        if not required_skills or not num_of_people_required:
            raise ValueError(f"Project {project_id} must have required skills and number of people required")

        def skill_match(user):
            return sum(1 for skill in required_skills if any(s['name'] == skill['name'] and s['level'] >= skill['level'] for s in user['skills']))

        sorted_users = sorted(users, key=skill_match, reverse=True)

        assigned_roles = {role: 0 for role in num_of_people_required.keys()}

        for user in sorted_users:
            if not user['skills']:
                continue  # Skip users without skills

            has_required_skills = skill_match(user) > 0

            if has_required_skills:
                for role, count in num_of_people_required.items():
                    if assigned_roles[role] < count:
                        user_roles = [skill_to_role_map.get(skill['name'], '') for skill in user['skills']]
                        if role in user_roles:
                            project_assignments[project_id].append(user['id'])
                            assigned_roles[role] += 1
                            break

    print_project_assignments(projects, project_assignments, users)

    return project_assignments

def print_project_assignments(projects, project_assignments, users):
    for project in projects:
        project_id = project['id']
        print(f"Project: {project['name']}")
        assigned_users = project_assignments[project_id]
        if assigned_users:
            for user_id in assigned_users:
                user = next(u for u in users if u['id'] == user_id)
                skills = ", ".join([f"{skill['name']} ({skill['level']})" for skill in user['skills']])
                print(f"  User ID: {user['id']}, Name: {user['name']}, Skills: {skills}, Rate: ${user['rate']}/hr")
        else:
            print("  No users assigned.")
        print()  # Blank line for better readability


