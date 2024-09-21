# utils.py

import numpy as np

# Calculate the edge weight based on user-project skill matching
def calculate_edge_weight(user, project):
    user_skills = {skill['name']: skill['level'] for skill in user['skills']}
    project_skills = {skill['name'] for skill in project['required_skills']}

    matches = len(set(user_skills.keys()) & project_skills)
    if matches == 0:
        return 0

    experience_score = sum(
        3 if user_skills[skill] == 'expert' else
        2 if user_skills[skill] == 'intermediate' else 1
        for skill in project_skills if skill in user_skills
    )

    weight = matches + experience_score
    print(f"Weight between User {user['id']} and Project {project['id']}: {weight}")
    return weight


# Generate adjacency matrix for Hungarian Algorithm input
def generate_adjacency_matrix(graph, users, projects):
    matrix = np.zeros((len(users), len(projects)))

    for i, user in enumerate(users):
        for j, project in enumerate(projects):
            weight = graph.get_edge_data(f"user_{user['id']}", f"project_{project['id']}", {}).get('weight', 0)
            matrix[i, j] = weight

    return matrix
