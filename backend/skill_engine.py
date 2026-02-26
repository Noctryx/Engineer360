from skill_data import ROLES

LEARNING_RESOURCES = {
    "PYTHON": "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "MACHINE_LEARNING": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
    "DEEP_LEARNING": "https://www.youtube.com/watch?v=aircAruvnKk",
    "STATISTICS": "https://www.youtube.com/watch?v=xxpc-HPKN28",
    "LINEAR_ALGEBRA": "https://www.youtube.com/watch?v=ZK3O402wf1c",
    "JAVASCRIPT": "https://www.youtube.com/watch?v=W6NZfCO5SIk",
    "REACT": "https://www.youtube.com/watch?v=bMknfKXIFA8",
    "NODE_JS": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
    "SQL": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
    "DATA_CLEANING": "https://www.youtube.com/watch?v=vmEHCJofslg",
    # Add remaining gradually
}

def analyze_skill_gap(target_role, user_skills):
    role_skills = ROLES.get(target_role)

    if not role_skills:
        return {"error": "Invalid role selected"}

    total_weight = sum(role_skills.values())
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
            "learning_link": LEARNING_RESOURCES.get(skill, "#")
        }
        for skill, weight in missing_skills_sorted
    ],
        "priority_skills": top_priority
    }