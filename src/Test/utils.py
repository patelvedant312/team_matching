# src/utils.py

from decimal import Decimal

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
    return levels.get(level.lower(), Decimal('0'))  # Returns 0 if level is unrecognized

def get_resource_skills_with_levels(resource):
    """
    Parses the skills of a resource and returns a dictionary with skill names and their levels.

    Args:
        resource (Resource): The resource object.

    Returns:
        dict: A dictionary mapping skill names to their levels.
    """
    skills_with_levels = {}
    for skill in resource.Skills:
        if ':' in skill:
            skill_name, skill_level = skill.split(':', 1)
            skills_with_levels[skill_name.strip().lower()] = skill_level.strip().lower()
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
    weight += weights_config['rate'] * (Decimal('100') - resource.Rate)  # Assuming rate <= 100

    # Experience: Sum of years in relevant past job titles
    total_experience = 0
    for title in resource.PastJobTitles:
        try:
            _, years = title.split(':')
            total_experience += int(years.strip())
        except:
            continue
    weight += weights_config['experience'] * Decimal(total_experience)

    # Skill Level: Average required skill levels
    required_skills = req.get('Skills', [])
    skill_levels = []
    resource_skills = get_resource_skills_with_levels(resource)
    for skill in required_skills:
        try:
            skill_name, required_level = skill.split(':')
            resource_level = resource_skills.get(skill_name.strip().lower(), 'beginner')
            skill_numeric = level_to_numeric(resource_level)
            skill_levels.append(skill_numeric)
        except:
            skill_levels.append(Decimal('0'))
    if skill_levels:
        avg_skill_level = sum(skill_levels) / Decimal(len(skill_levels))
    else:
        avg_skill_level = Decimal('0')
    weight += weights_config['skill_level'] * avg_skill_level

    return weight
