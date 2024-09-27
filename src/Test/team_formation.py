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
    "AI Assistants",
    "Cloud Computing",
    "Blockchain",
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
    "Python, Django",
    "JavaScript, React",
    "Java, Spring Boot",
    "C++, ROS",
    "C#, Unity",
    "Node.js, Express",
    "React, Node.js",
    "Python, TensorFlow",
    "AWS, Docker",
    "Solidity, Blockchain",
    "React Native, Redux",
    "HTML, CSS"
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

def generate_skills():
    """Generates a list of skill dictionaries for a resource or project role."""
    num_skills = random.randint(2, 5)
    selected_skills = random.sample(SKILLS, num_skills)
    skills_with_levels = []
    for skill in selected_skills:
        level = random.choice(SKILL_LEVELS)
        skills_with_levels.append({skill: {"level": level}})
    return skills_with_levels

def generate_past_jobs():
    """Generates a list of past job dictionaries for a resource."""
    num_jobs = random.randint(2, 4)
    selected_jobs = random.sample(JOB_TITLES, num_jobs)
    past_jobs = []
    for job in selected_jobs:
        years = round(random.uniform(1.0, 10.0), 1)
        past_jobs.append({job: {"years": years}})
    return past_jobs

def generate_domains():
    """Generates a list of domains for a resource or project."""
    num_domains = random.randint(1, 3)
    return random.sample(DOMAINS, num_domains)

def generate_resources(num_resources):
    """Generates a list of resource dictionaries."""
    resources = []
    for i in range(1, num_resources + 1):
        name = fake.name()
        rate = round(random.uniform(40.0, 100.0), 2)
        
        # Assign skills
        skills = generate_skills()
        
        # Assign past job titles
        past_jobs = generate_past_jobs()
        
        # Assign domains
        domains = generate_domains()
        
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

def generate_required_resources():
    """Generates a list of required resource dictionaries for a project."""
    num_required = random.randint(2, 4)
    required_resources = []
    selected_roles = random.sample(ROLES, num_required)
    for role in selected_roles:
        # Assign skills for the role
        skills = generate_skills()
        # Assign quantity
        quantity = random.randint(1, 3)
        required_resources.append({
            "Role": role,
            "Skills": skills,
            "Quantity": quantity
        })
    return required_resources

def generate_projects(num_projects):
    """Generates a list of project dictionaries."""
    projects = []
    for i in range(1, num_projects + 1):
        project_name = PROJECT_NAMES[i - 1]  # Ensure unique names
        org = random.choice(ORGANIZATIONS)
        org_id = org["OrgID"]
        
        # Assign required resources
        required_resources = generate_required_resources()
        
        number_of_days = random.randint(60, 180)
        
        # Start date within the next 30 days
        project_start_date = fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d')
        
        technology = random.choice(TECHNOLOGIES)
        domain = random.choice(DOMAINS)
        
        project = {
            "ProjectID": i,
            "ProjectName": project_name,
            "OrgID": org_id,
            "RequiredResources": required_resources,
            "NumberOfDays": number_of_days,
            "ProjectStartDate": project_start_date,
            "Technology": technology,
            "Domain": domain
        }
        projects.append(project)
    return projects

def main():
    """Generates resources and projects, then saves them to JSON files."""
    resources = generate_resources(NUM_RESOURCES)
    projects = generate_projects(NUM_PROJECTS)
    
    # Save to JSON files
    with open('sample_resources.json', 'w') as f:
        json.dump(resources, f, indent=4)
    
    with open('sample_projects.json', 'w') as f:
        json.dump(projects, f, indent=4)
    
    print(f"Generated {NUM_RESOURCES} resources and {NUM_PROJECTS} projects successfully.")

if __name__ == "__main__":
    main()
