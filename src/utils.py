# src/utils.py

def level_to_numeric(level):
    """
    Converts skill level from string to numeric value for comparison.

    Args:
        level (str): Skill level as a string ('beginner', 'intermediate', 'expert').

    Returns:
        int: Numeric representation of the skill level.
    """
    levels = {
        'beginner': 1,
        'intermediate': 2,
        'expert': 3
    }
    return levels.get(level.lower(), 0)  # Returns 0 if level is unrecognized
