from learning_resources import LEARNING_RESOURCES
from resource_utils import build_learning_search_url, normalize_skill_name
from skill_data import ROLES

def analyze_skill_gap(target_role, user_skills):
    role_skills = ROLES.get(target_role)

    if not role_skills:
        return {"error": "Invalid role selected"}

    total_weight = sum(role_skills.values())
    if total_weight <= 0:
            return {"error": "Role has no configured skills"}

    matched_weight = 0
    missing_skills = []

    for skill, weight in role_skills.items():
        if skill in user_skills:
            matched_weight += weight
        else:
            missing_skills.append((skill, weight))

    match_percentage = round((matched_weight / total_weight) * 100, 2)

    # Sort missing skills by weight descending
    missing_skills_sorted = sorted(missing_skills, key=lambda x: x[1], reverse=True)

    top_priority = [skill for skill, _ in missing_skills_sorted[:2]]

    return {
        "match_percentage": match_percentage,
            "missing_skills": [
                {
                    "skill": skill,
                    "weight": weight,
                "learning_link": LEARNING_RESOURCES.get(
                    normalize_skill_name(skill),
                    build_learning_search_url(skill)
                )
                }
                for skill, weight in missing_skills_sorted
            ],
        "priority_skills": top_priority
    }