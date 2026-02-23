def analyze_burnout(sleep_hours, focus_score, stress_level, study_hours):
    score = 0

    if sleep_hours < 6:
        score += 25
    if focus_score < 5:
        score += 25
    if stress_level > 7:
        score += 25
    if study_hours > 8:
        score += 25

    if score >= 75:
        risk = "HIGH"
    elif score >= 40:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return {
        "burnout_score": score,
        "burnout_risk": risk
    }