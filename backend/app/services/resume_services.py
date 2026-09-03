def calc_resume_score(text):
    score=0
    suggestions=[]
    text_lower=text.lower()
    skills=["python","java","javascript","fastapi","django","react","sql","postgresql","mongodb","docker","aws","git"]
    skills_found=[]
    for skill in skills:
        if skill in text_lower:
            skills_found.append(skill)
    score += min(len(skills_found) * 5, 30)
    sections = {
        "education": "education",
        "experience": "experience",
        "projects": "projects",
        "skills": "skills",
        "certifications": "certification"
    }

    for section, keyword in sections.items():

        if keyword in text_lower:
            score += 10
        else:
            suggestions.append(
                f"Consider adding a {section} section"
            )

    # Maximum score
    score = min(score, 100)

    return {
        "score": score,
        "skills_found": skills_found,
        "suggestions": suggestions
    }