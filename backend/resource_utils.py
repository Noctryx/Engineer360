from urllib.parse import quote_plus


def normalize_skill_name(skill_name):
    return skill_name.strip().upper().replace(" ", "_").replace("-", "_")


def build_learning_search_url(skill_name):
    normalized_name = normalize_skill_name(skill_name)
    search_query = quote_plus(normalized_name.replace("_", " "))
    return f"https://www.youtube.com/results?search_query={search_query}"
