def generate_recommendation(skill_result, burnout_result):
    match = skill_result["match_percentage"]
    burnout = burnout_result["burnout_risk"]

    if burnout == "HIGH":
        return f"High burnout detected. Focus only on {skill_result['priority_skills'][0]} and improve sleep."

    if burnout == "MODERATE" and match < 50:
        return "Skill gap exists but avoid overload. Study 1–2 focused hours daily."

    if burnout == "LOW" and match < 50:
        return "Good mental condition. Increase learning intensity and focus on missing core skills."

    if match >= 75:
        return "Strong alignment with target role. Maintain consistency and refine advanced skills."

    return "Maintain balanced progress and steady improvement."