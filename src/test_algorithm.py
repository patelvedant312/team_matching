# test_algorithm.py

import json
from graph_algorithm import match_users_to_projects

try:
    # Load sample data
    with open('data/sample_users.json') as user_file:
        users = json.load(user_file)
        print("Loaded Users:", users)  # Add this for debugging
    
    with open('data/sample_projects.json') as project_file:
        projects = json.load(project_file)
        print("Loaded Projects:", projects)  # Add this for debugging

    # Run the algorithm
    matching_results = match_users_to_projects(users, projects)
    
    # Output the matching results
    print("Matching Results:", matching_results)

except FileNotFoundError as e:
    print(f"Error: {e}")
except json.JSONDecodeError:
    print("Error: Could not decode JSON.")
