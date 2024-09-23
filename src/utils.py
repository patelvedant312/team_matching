# src/utils.py

def level_to_numeric(level):
    level_mapping = {
        'beginner': 1,
        'intermediate': 2,
        'expert': 3
    }
    return level_mapping.get(level.lower(), 0)

def match_skill_level(user_level, required_level):
    return level_to_numeric(user_level) >= level_to_numeric(required_level)
