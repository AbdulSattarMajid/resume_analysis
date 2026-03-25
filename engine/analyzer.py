import spacy
import json
import os
import re

# LOAD THE LINGUISTIC ENGINE
nlp = spacy.load("en_core_web_sm")

def load_skills():
    """Step 1: Loads the Categorized JSON Taxonomy """
    json_path = os.path.join("data", "skill_taxonomy.json")
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def analyze_skills(resume_text, jd_text, target_role):
    """
    UNIVERSAL ATS MATCHER (Enterprise Logic):
    1. Combines ALL skills from ALL roles into a master list.
    2. Finds which skills from the master list are requested in the JD.
    3. Checks if the candidate has those specific skills.
    """
    all_role_data = load_skills()
    
    # NEW: Merge all categories across all roles to prevent silos
    universal_categories = {}
    for role, categories in all_role_data.items():
        for category, skills in categories.items():
            if category not in universal_categories:
                universal_categories[category] = set()
            universal_categories[category].update(skills)
    
    category_results = {}
    total_found = []
    total_missing = []

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    # Process the new universal categories
    for category, skills in universal_categories.items():
        found_in_cat = set()
        missing_in_cat = set()
        
        for skill in skills:
            skill_lower = skill.lower()
            # Regex boundary to match exactly, optionally with 's' (handles API vs APIs)
            pattern = r'\b' + re.escape(skill_lower) + r'(?:s)?\b'
            
            # STEP 1: Is this skill actually required in the Job Description?
            if re.search(pattern, jd_lower) or skill_lower in jd_lower:
                
                # STEP 2: Yes, it is required. Does the candidate have it?
                if re.search(pattern, resume_lower) or skill_lower in resume_lower:
                    found_in_cat.add(skill)
                else:
                    missing_in_cat.add(skill)
                    
        # Only add the category to the final report if the JD actually required skills from it
        if found_in_cat or missing_in_cat:
            category_results[category] = {
                "found": list(found_in_cat),
                "missing": list(missing_in_cat)
            }
            total_found.extend(list(found_in_cat))
            total_missing.extend(list(missing_in_cat))

    # Calculate the true JD Score based ONLY on the required skills
    total_jd_requirements = len(total_found) + len(total_missing)
    true_jd_score = (len(total_found) / total_jd_requirements) * 100 if total_jd_requirements > 0 else 0.0

    return {
        "score": round(true_jd_score, 2),
        "found": list(set(total_found)),
        "missing": list(set(total_missing)),
        "detailed": category_results
    }