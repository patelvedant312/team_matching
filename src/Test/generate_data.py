import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Configuration
NUM_RESOURCES = 65
NUM_PROJECTS = 12
NUM_ORGANIZATIONS = 3  # Assuming OrgID ranges from 1 to 3

# Predefined Lists
SKILLS = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "C#",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "AWS",
    "DevOps",
    "Blockchain",
    "Unity",
    "3D Modeling",
    "ETL",
    "Data Engineering",
    "Financial Modeling",
    "Data Science",
    "TensorFlow",
    "NLP",
    "Spring Boot",
    "Express",
    "WebSockets",
    "Redux",
    "Docker",
    "Solidity",
    "React Native",
    "HTML",
    "CSS",
    "Ruby",
    "Rails",
    "Go",
    "Kubernetes",
    "Swift",
    "Objective-C",
    "TypeScript",
    "GraphQL"
]

SKILL_LEVELS = ["beginner", "intermediate", "expert"]

DOMAINS = [
    "Healthcare",
    "Finance",
    "E-commerce",
    "Gaming",
    "Education",
    "Media",
    "Cloud Computing",
    "Autonomous Systems",
    "Retail",
    "Communication"
]

ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Data Scientist",
    "Data Engineer",
    "3D Designer",
    "Game Developer",
    "Financial Analyst",
    "DevOps Engineer",
    "Blockchain Developer",
    "UI/UX Designer",
    "Full Stack Developer",
    "Machine Learning Engineer"
]

TECHNOLOGIES = [
    "Python",
    "Django",
    "JavaScript",
    "React",
    "Java",
    "Spring Boot",
    "C++",
    "ROS",
    "C#",
    "Unity",
    "Node.js",
    "Express",
    "TensorFlow",
    "AWS",
    "Docker",
    "Solidity",
    "Blockchain",
    "React Native",
    "Redux",
    "HTML",
    "CSS",
    "Ruby",
    "Rails",
    "Go",
    "Kubernetes",
    "Swift",
    "Objective-C",
    "TypeScript",
    "GraphQL"
]

PROJECT_NAMES = [
    "Smart Healthcare Platform",
    "Financial Forecasting System",
    "E-commerce Web App",
    "3D Game Development",
    "Real-Time Chat Application",
    "Healthcare Data Analysis",
    "Blockchain Governance Tool",
    "Autonomous Drone Control",
    "AI-Powered Media Analytics",
    "Cloud-Based Retail Solution",
    "Education Management System",
    "Communication Enhancement Platform"
]

JOB_TITLES = [
    "Data Scientist",
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "DevOps Engineer",
    "Blockchain Developer",
    "Financial Analyst",
    "3D Designer",
    "Machine Learning Engineer",
    "Full Stack Developer",
    "UI/UX Designer",
    "Data Engineer",
    "Cloud Engineer",
    "Robotics Engineer",
    "AI Engineer",
    "System Administrator",
    "Smart Contract Developer",
    "NLP Specialist",
    "Data Analyst",
    "Database Administrator"
]

ORGANIZATIONS = [
    {"OrgID": 1, "OrgName": "OrgA"},
    {"OrgID": 2, "OrgName": "OrgB"},
    {"OrgID": 3, "OrgName": "OrgC"}
]

def generate_resources(num_resources):
    resources = []
    for i in range(1, num_resources + 1):
        name = fake.name()
        rate = round(random.uniform(40.0, 100.0), 2)
        
        # Assign 3-5 skills with random levels
        num_skills = random.randint(3, 5)
        skills = {}
        selected_skills = random.sample(SKILLS, num_skills)
        for skill in selected_skills:
            level = random.choice(SKILL_LEVELS)
            skills[skill] = {"level": level}
        
        # Assign 2-4 past job titles with random years
        num_jobs = random.randint(2, 4)
        past_jobs = {}
        selected_jobs = random.sample(JOB_TITLES, num_jobs)
        for job in selected_jobs:
            years = round(random.uniform(1.0, 10.0), 1)
            past_jobs[job] = {"years": years}
        
        # Assign 1-3 domains
        num_domains = random.randint(1, 3)
        domains = random.sample(DOMAINS, num_domains)
        
        # Available date within the next 90 days
        available_date = fake.date_between(start_date='today', end_date='+90d').strftime('%Y-%m-%d')
        
        # Random OrgID
        org = random.choice(ORGANIZATIONS)
        org_id = org["OrgID"]
        
        resource = {
            "ResourceID": i,
            "Name": name,
            "Rate": rate,
            "Skills": skills,
            "PastJobTitles": past_jobs,
            "Domain": domains,
            "AvailableDate": available_date,
            "OrgID": org_id
        }
        resources.append(resource)
    return resources

def generate_projects(num_projects):
    projects = []
    for i in range(1, num_projects + 1):
        project_name = PROJECT_NAMES[i - 1]  # Ensure unique names
        org = random.choice(ORGANIZATIONS)
        org_id = org["OrgID"]
        
        # Assign 2-4 required resources
        num_required = random.randint(2, 4)
        required_resources = []
        selected_roles = random.sample(ROLES, num_required)
        for role in selected_roles:
            # Assign 2-4 skills per role
            num_skills = random.randint(2, 4)
            role_skills = {}
            selected_role_skills = random.sample(SKILLS, num_skills)
            for skill in selected_role_skills:
                level = random.choice(SKILL_LEVELS)
                role_skills[skill] = {"level": level}
            # Assign quantity 1-3
            quantity = random.randint(1, 3)
            required_resources.append({
                "Role": role,
                "Skills": role_skills,
                "Quantity": quantity
            })
        
        number_of_days = random.randint(60, 180)
        
        # Start date within the next 30 days
        project_start_date = fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d')
        
        # Assign 1-3 technologies
        num_technologies = random.randint(1, 3)
        technologies = random.sample(TECHNOLOGIES, num_technologies)
        
        # Assign 1-3 domains
        num_domains = random.randint(1, 3)
        domains = random.sample(DOMAINS, num_domains)
        
        project = {
            "ProjectID": i,
            "ProjectName": project_name,
            "OrgID": org_id,
            "RequiredResources": required_resources,
            "NumberOfDays": number_of_days,
            "ProjectStartDate": project_start_date,
            "Technology": technologies,
            "Domain": domains
        }
        projects.append(project)
    return projects

def main():
    resources = generate_resources(NUM_RESOURCES)
    projects = generate_projects(NUM_PROJECTS)
    
    # Save to JSON files
    with open('data/sample_resources.json', 'w') as f:
        json.dump(resources, f, indent=4)
    
    with open('data/sample_projects.json', 'w') as f:
        json.dump(projects, f, indent=4)
    
    print(f"Generated {NUM_RESOURCES} resources and {NUM_PROJECTS} projects successfully.")

if __name__ == "__main__":
    main()