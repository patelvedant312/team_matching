# src/utils.py

from decimal import Decimal
import logging

# Configure logging for the utils module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def level_to_numeric(level):
    """
    Converts skill level from string to numeric value for comparison.

    Args:
        level (str): Skill level as a string ('beginner', 'intermediate', 'expert').

    Returns:
        Decimal: Numeric representation of the skill level.
    """
    levels = {
        'beginner': Decimal('1'),
        'intermediate': Decimal('2'),
        'expert': Decimal('3')
    }
    numeric_level = levels.get(level.lower(), Decimal('0'))  # Returns 0 if level is unrecognized
    if numeric_level == Decimal('0'):
        logger.warning(f"Unrecognized skill level '{level}'. Defaulting to 0.")
    return numeric_level

def get_resource_skills_with_levels(resource):
    """
    Parses the skills of a resource and returns a dictionary with skill names and their levels.

    Args:
        resource (Resource): The resource object.

    Returns:
        dict: A dictionary mapping skill names to their levels.
    """
    skills_with_levels = {}
    try:
        for skill_name, details in resource.Skills.items():
            skill_level = details.get('level', 'beginner').strip().lower()
            skills_with_levels[skill_name.strip().lower()] = skill_level
    except AttributeError as e:
        logger.error(f"Error parsing skills for resource {resource.Name}: {e}")
    return skills_with_levels

def calculate_weight(resource, req, project):
    """
    Calculates a weight for a resource based on various parameters.

    Args:
        resource (Resource): The resource being evaluated.
        req (dict): The role requirement.
        project (Project): The project to which the role belongs.

    Returns:
        Decimal: The calculated weight.
    """
    weight = Decimal('0.0')
    weights_config = {
        'rate': Decimal('0.5'),
        'experience': Decimal('1.0'),
        'skill_level': Decimal('1.0')
    }

    # Rate: Lower rate is better
    try:
        rate = Decimal(resource.Rate)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid rate for resource {resource.Name}: {e}")
        rate = Decimal('100')  # Assign a default high rate if invalid

    # Normalize rate to ensure it's not negative
    rate = max(rate, Decimal('0'))

    # Calculate rate weight: higher rate decreases the weight
    weight += weights_config['rate'] * (Decimal('100') - rate)

    # Experience: Sum of years in all past job titles
    total_experience = Decimal('0.0')
    try:
        for title, details in resource.PastJobTitles.items():
            years = details.get('years', 0)
            total_experience += Decimal(str(years))
    except (ValueError, TypeError, AttributeError) as e:
        logger.error(f"Error parsing past job titles for resource {resource.Name}: {e}")

    weight += weights_config['experience'] * total_experience

    # Skill Level: Average of resource's skill levels for required skills
    required_skills = req.get('Skills', {})
    skill_levels = []
    resource_skills = get_resource_skills_with_levels(resource)

    for skill_name, details in required_skills.items():
        required_level = details.get('level', 'beginner').strip().lower()
        resource_level = resource_skills.get(skill_name.strip().lower(), 'beginner')
        skill_numeric = level_to_numeric(resource_level)
        skill_levels.append(skill_numeric)

    if skill_levels:
        avg_skill_level = sum(skill_levels) / Decimal(len(skill_levels))
    else:
        avg_skill_level = Decimal('0')

    weight += weights_config['skill_level'] * avg_skill_level

    logger.debug(
        f"Calculated weight for resource {resource.Name} for role '{req['Role']}' in project '{project.ProjectName}': {weight}"
    )

    return weight