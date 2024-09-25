# src/team_formation.py

import datetime
from collections import defaultdict
from utils import level_to_numeric

def find_best_team_for_project(project, users, org_id=None):
    required_skills = {skill['name']: skill['level'] for skill in project['required_skills']}
    num_people_required = project.get('num_of_people_required', {})
    project_domain = project.get('domain', None)
    project_start_date = datetime.datetime.strptime(project.get('project_start_date', '2023-01-01'), '%Y-%m-%d')
    number_of_days = project.get('number_of_days', 0)
    project_end_date = project_start_date + datetime.timedelta(days=number_of_days)

    # Define the mapping from roles to required skills
    role_to_skills_map = {
        "game_developers": ["Game Development", "Unity", "C#"],
        "3d_designers": ["3D Modeling", "Animation", "Unity"],
        "data_scientists": ["Machine Learning", "Data Analysis", "Python"],
        "data_engineers": ["SQL", "ETL", "Python"],
        "frontend_developers": ["JavaScript", "React", "HTML", "CSS"],
        "backend_developers": ["Python", "Node.js", "Java", "C++"],
        "blockchain_developers": ["Blockchain", "Solidity", "Cryptography"],
        "security_experts": ["Cybersecurity", "Penetration Testing", "Cryptography"],
        "cloud_engineers": ["AWS", "Azure", "Cloud Computing"],
        "devops_engineers": ["DevOps", "Docker", "CI/CD"],
        "iot_engineers": ["IoT", "Embedded Systems", "Arduino"],
        "embedded_systems_engineers": ["Embedded Systems", "C++", "Microcontrollers"],
        "nlp_experts": ["NLP", "Natural Language Processing", "Machine Learning"],
        "machine_learning_engineers": ["Machine Learning", "Python", "TensorFlow"],
        "software_engineers": ["Python", "C++", "Java"],
        "robotics_engineers": ["Robotics", "ROS", "C++"],
        "computer_vision_engineers": ["Computer Vision", "OpenCV", "C++"],
        "financial_analysts": ["Finance", "Data Analysis", "Python"],
        # Add other roles as needed
    }

    team = []
    assigned_users = set()
    unfilled_roles = {}

    for role, count_required in num_people_required.items():
        if count_required == 0:
            continue
        required_role_skills = role_to_skills_map.get(role, [])
        if not required_role_skills:
            # Role not defined in mapping
            unfilled_roles[role] = count_required
            continue
        candidates = []
        for user in users:
            if user['id'] in assigned_users:
                continue
            if org_id and user.get('org_id') != org_id:
                continue  # Skip users not in the specified organization
            user_skills = {skill['name']: skill['level'] for skill in user['skills']}
            user_domain = user.get('past_work_domain', '')
            user_experience = user.get('years_of_exp', 0)
            user_available_date = datetime.datetime.strptime(user.get('available_date', '2023-01-01'), '%Y-%m-%d')
            domain_match = project_domain == user_domain
            skill_matches = [skill for skill in required_role_skills if skill in user_skills]
            if skill_matches:
                # Ensure user has required skill levels
                user_skill_levels = [level_to_numeric(user_skills[skill]) for skill in skill_matches]
                required_skill_levels = [level_to_numeric(required_skills.get(skill, 'beginner')) for skill in skill_matches if skill in required_skills]
                
                # Check if required_skill_levels is empty
                if not required_skill_levels:
                    # Default to beginner level if not specified
                    required_skill_levels = [1] * len(skill_matches)
                
                # Avoid calling max() on an empty list
                if user_skill_levels and required_skill_levels:
                    skill_level = max(user_skill_levels)
                    required_skill_level = max(required_skill_levels)
                    if skill_level >= required_skill_level:
                        # Allow users who are available within a grace period after project start
                        grace_period_days = 0  # Adjust as needed
                        if user_available_date <= project_start_date + datetime.timedelta(days=grace_period_days):
                            candidates.append({
                                'user': user,
                                'domain_match': domain_match,
                                'experience': user_experience,
                                'rate': user.get('rate', 0),
                                'skill_level': skill_level,
                                'available_date': user_available_date
                            })
        # Now assign candidates to the role
        if not candidates:
            # No candidates found for this role
            unfilled_roles[role] = count_required
            continue
        # Sort candidates
        candidates.sort(key=lambda x: (
            not x['domain_match'],       # Prioritize domain match
            -x['experience'],            # More experience
            -x['skill_level'],           # Higher skill level
            x['available_date'],         # Available sooner
            x['rate']                    # Lower rate
        ))
        # Select candidates
        selected = 0
        for candidate in candidates:
            if selected >= count_required:
                break
            team.append({'user': candidate['user'], 'role': role})
            assigned_users.add(candidate['user']['id'])
            selected += 1
        if selected < count_required:
            # Not enough candidates for this role
            unfilled_roles[role] = count_required - selected
    return team, unfilled_roles

def match_users_to_projects(users, projects, org_id=None):
    if not users or not projects:
        raise ValueError("Users and projects must not be empty")

    # Filter users by organization if org_id is provided
    if org_id:
        users = [user for user in users if user.get('org_id') == org_id]
        if not users:
            print(f"No users found for organization ID: {org_id}")
            return {}

    project_assignments = {}

    for project in projects:
        team, unfilled_roles = find_best_team_for_project(project, users, org_id)
        if team or unfilled_roles:
            project_assignments[project['id']] = [member['user']['id'] for member in team]
            print(f"Project: {project['name']}")
            if team:
                print("  Assigned Team:")
                for member in team:
                    user = member['user']
                    role = member['role']
                    skills = ", ".join([f"{skill['name']} ({skill['level']})" for skill in user['skills']])
                    available_from = user.get('available_date', 'N/A')
                    print(f"    - {user['name']} (ID: {user['id']}), Available From: {available_from}, Role: {role.replace('_', ' ').title()}, Skills: {skills}")
            else:
                print("  No team members assigned.")
            # Print unfilled roles
            if unfilled_roles:
                print("  Unfilled Roles:")
                for role, count in unfilled_roles.items():
                    print(f"    - {count} {role.replace('_', ' ').title()} needed")
            print()
            # Remove assigned users from the pool
            users = [user for user in users if user['id'] not in project_assignments[project['id']]]
        else:
            print(f"Project: {project['name']}")
            print("  Could not form a suitable team.")
            print()

    return project_assignments
