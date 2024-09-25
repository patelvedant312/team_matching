# src/test_algorithm.py

import json
import os
from team_formation import match_users_to_projects

def load_data(file_path):
    with open(file_path) as f:
        return json.load(f)

def main():
    try:
        # Load sample data
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        users = load_data(os.path.join(data_dir, 'sample_users.json'))
        projects = load_data(os.path.join(data_dir, 'sample_projects.json'))

        # Specify the organization ID to filter users (optional)
        org_id = None  # Set to None to include all organizations

        # Run the algorithm
        matching_results = match_users_to_projects(users, projects, org_id)

        # Output the matching results
        print("Matching Results:", matching_results)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
