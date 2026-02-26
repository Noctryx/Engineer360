from learning_resources import LEARNING_RESOURCES

def generate_recommendation(skill_result, burnout_result):

    match = skill_result["match_percentage"]
    burnout = burnout_result["burnout_risk"]

    missing_skills = skill_result.get("missing_skills", [])

    resource_links = {}

    for skill_item in missing_skills:

        if isinstance(skill_item, dict):
            skill_name = skill_item.get("skill")
        else:
            skill_name = skill_item

    # SAFETY CHECK
        if not isinstance(skill_name, str):
            continue

        resource_links[skill_name] = LEARNING_RESOURCES.get(
            skill_name,
            "https://www.youtube.com/results?search_query=" + skill_name.replace("_", "+")
        )

    if burnout == "HIGH":
        message = "High burnout detected. Reduce load."
    elif match < 50:
        message = "Skill gap exists. Focus on core skills."
    elif match >= 75:
        message = "Strong alignment. Maintain momentum."
    else:
        message = "Maintain steady improvement."

    return {
        "message": message,
        "resources": resource_links
    }