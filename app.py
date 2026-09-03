from flask import Flask, render_template, request
import PyPDF2
from docx import Document
import re

app = Flask(__name__)
# home page
@app.route("/")
def home():
    return render_template("index.html")
# ANALYZE RESUME
@app.route("/analyze", methods=["POST"])
def analyze():
#file check
    if "resume" not in request.files:
        return "No file selected"

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a file"

    filename = file.filename.lower()
#resume read
    resume_text = ""
    # READ PDF
    if filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
    # READ DOCX
    elif filename.endswith(".docx"):
        document = Document(file)
        for paragraph in document.paragraphs:
            resume_text += paragraph.text + "\n"


    else:
        return "Please upload only PDF or DOCX files"

    # TEXT CLEANING
    cleaned_text = resume_text.lower()
    cleaned_text = " ".join(cleaned_text.split())

    # SKILL DETECTION
    skills_list = [

        "python",
        "java",
        "c",
        "c++",
        "sql",

        "machine learning",
        "deep learning",

        "tensorflow",
        "keras",
        "scikit-learn",
        "pytorch",

        "nlp",
        "computer vision",
        "cnn",
        "rnn",
        "ann",

        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",

        "data analysis",
        "data visualization",
        "business analytics",

        "excel",
        "advanced excel",

        "generative ai",
        "prompt engineering",
        "llm",
        "large language models",

        "aws",
        "azure",
        "google cloud",
        "devops",
        "linux",

        "flask",
        "mysql",
        "sqlite",

        "html",
        "css",
        "javascript",
        "typescript",
        "react",

        "github",

        "oops",
        "dsa",
        "dbms",

        "cybersecurity",
        "network security",
        "ethical hacking",

        "project management",
        "market research",
        "process mapping",
        "technical documentation",
        "marketing"
    ]


    detected_list = []
    missing_skills = []


    for skill in skills_list:

        if skill in cleaned_text:
            detected_list.append(skill)

        else:
            missing_skills.append(skill)

#role skills

    ai_role = [

        "python",
        "pandas",
        "matplotlib",
        "tensorflow",
        "machine learning",
        "scikit-learn",
        "ann",
        "nlp",
        "java",
        "c",
        "keras",
        "deep learning",
        "pytorch",
        "llm",
        "large language models",
        "prompt engineering"
    ]


    data_analyst = [

        "python",
        "java",
        "c",
        "c++",
        "sql",
        "pandas",
        "numpy",
        "matplotlib",
        "data analysis",
        "data visualization",
        "seaborn",
        "excel"
    ]


    cloud_devops = [

        "aws",
        "azure",
        "google cloud",
        "devops"
    ]


    cybersecurity_role = [

        "cybersecurity",
        "network security",
        "ethical hacking"
    ]


    project_manager = [

        "project management",
        "market research",
        "process mapping",
        "technical documentation",
        "marketing"
    ]

#AI role matching
    matched_skills = []
    ai_missing_skills = []


    for skill in ai_role:

        if skill in detected_list:
            matched_skills.append(skill)

        else:
            ai_missing_skills.append(skill)


    ai_no_matched_list = len(matched_skills)
#data science matching

    data_matched_skills = []
    data_missing_skills = []


    for skill in data_analyst:

        if skill in detected_list:
            data_matched_skills.append(skill)

        else:
            data_missing_skills.append(skill)


    data_no_matched_list = len(data_matched_skills)
#cloud matching

    cloud_matched_skills = []
    cloud_missing_skills = []

    for skill in cloud_devops:

        if skill in detected_list:
            cloud_matched_skills.append(skill)

        else:
            cloud_missing_skills.append(skill)


    no_cloud_matched_skills = len(cloud_matched_skills)

#
    cyber_matched_skills = []
    cyber_missing_skills = []

    for skill in cybersecurity_role:

        if skill in detected_list:
            cyber_matched_skills.append(skill)

        else:
            cyber_missing_skills.append(skill)

    no_cyber_matched_skills = len(cyber_matched_skills)

# PROJECT MANAGER MATCHING
    product_matched_skills = []
    product_missing_skills = []

    for skill in project_manager:

        if skill in detected_list:
            product_matched_skills.append(skill)

        else:
            product_missing_skills.append(skill)

    no_product_matched_skills = len(product_matched_skills)



 # CONTACT SCORE
    contact_score = 0
    if "@" in cleaned_text:

        econ = 5
        contact_score += 5

    else:

        econ = 0

    if "linkedin" in cleaned_text:

        lincon = 5
        contact_score += 5

    else:

        lincon = 0


    phone_numbers = re.findall(
        r'\+?\d[\d\s\-]{7,}\d',
        resume_text
    )

    if phone_numbers:

        pcon = 5
        contact_score += 5

    else:

        pcon = 0

    # SKILLS SCORE
    skills_score = 0

    if len(detected_list) >= 8:

        skills_score = 20

    elif len(detected_list) >= 6:

        skills_score = 15

    elif len(detected_list) >= 4:

        skills_score = 10

    elif len(detected_list) >= 2:

        skills_score = 5

    else:

        skills_score = 0

    # EDUCATION SCORE

    education_score = 0

    education_keywords = [

        "college",
        "university",
        "institute",
        "masters",
        "m-tech",
        "mtech",
        "bachelor",
        "btech",
        "b-tech",
        "engineering",
        "cse",
        "aiml",
        "data science"
    ]


    for keyword in education_keywords:

        if keyword in cleaned_text:

            education_score = 15
            break

    # PROJECT SCORE

    project_keywords = [

        "built",
        "designed",
        "developed",
        "created",
        "implemented"
    ]

    project_section = resume_text

    if "projects" in cleaned_text:

        start = resume_text.lower().find("projects")
        project_section = resume_text[start:]


    lines = project_section.split("\n")

    project_count = 0


    for line in lines:

        line = line.lower()

        for keyword in project_keywords:

            if keyword in line:

                project_count += 1
                break


    if project_count >= 5:

        project_score = 20

    elif project_count >= 3:

        project_score = 15

    elif project_count >= 1:

        project_score = 10

    else:

        project_score = 0

    # RESUME STRUCTURE SCORE
    structure_score = 0
    structure_sections = [

        "summary",
        "objective",
        "experience",
        "internship",
        "skills",
        "projects",
        "education"
    ]

    structure_missing = []
    for section in structure_sections:

        if section in cleaned_text:

            structure_score += 3

            if structure_score >= 15:
                break

        else:

            structure_missing.append(section)

    # RESUME COMPLETENESS

    completeness = 0

    if "summary" in cleaned_text or "objective" in cleaned_text:

        summary_text = 5

    else:

        summary_text = 0


    completeness += summary_text
    # CERTIFICATION
    certification_score = 0

    if "certifications" in cleaned_text or "certificates" in cleaned_text:

        certification_score = 5

    else:

        certification_score = 0
    completeness += certification_score
# EXPERIENCE SCORE

    experience_score = 0

    experience_found = False

    experience_keywords = [

        "experience",
        "internship",
        "internships",
        "work experience"
    ]

    for key in experience_keywords:

        if key in cleaned_text:

            experience_found = True
            break

    years = re.findall(
        r'\d+\s*years?',
        cleaned_text
    )

    months = re.findall(
        r'\d+\s*months?',
        cleaned_text
    )

    total_years = 0

    for year in years:

        num = re.findall(r'\d+', year)

        if num:

            total_years += int(num[0])


    for month in months:

        num = re.findall(r'\d+', month)

        if num:

            total_years += int(num[0]) / 12


    if total_years >= 2:

        experience_score = 5


    elif total_years >= 1:

        experience_score = 3


    elif total_years >= 0.08:

        experience_score = 1


    elif experience_found:

        experience_score = 1


    else:

        experience_score = 0


    completeness += experience_score


    # ==========================================
    # FINAL SCORE CALCULATION
    # ==========================================

    resume_score = (

        contact_score
        + skills_score
        + education_score
        + project_score
        + structure_score
        + completeness
    )


    if resume_score > 100:

        resume_score = 100

    # RESUME RATING

    if resume_score >= 90:

        resume_rating = "Excellent"

    elif resume_score >= 80:

        resume_rating = "Very Good"

    elif resume_score >= 70:

        resume_rating = "Good"

    elif resume_score >= 60:

        resume_rating = "Average"

    else:

        resume_rating = "Needs Improvement"

    # ROLE PERCENTAGES

    ai_percentage = round(

        (ai_no_matched_list / len(ai_role)) * 100,
        2
    )

    data_percentage = round(

        (data_no_matched_list / len(data_analyst)) * 100,
        2
    )


    cloud_percentage = round(

        (no_cloud_matched_skills / len(cloud_devops)) * 100,
        2
    )


    cyber_percentage = round(

        (no_cyber_matched_skills / len(cybersecurity_role)) * 100,
        2
    )


    product_percentage = round(

        (no_product_matched_skills / len(project_manager)) * 100,
        2
    )

    # SUGGESTIONS

    suggestions = []

    # CONTACT
    if contact_score < 15:

        if econ == 0:

            suggestions.append(
                "Add your email address."
            )

        if lincon == 0:

            suggestions.append(
                "Add your LinkedIn profile."
            )

        if pcon == 0:

            suggestions.append(
                "Add your phone number."
            )

    # SKILLS

    if skills_score < 20:

        suggestions.append(
            "Add more relevant technical skills to your resume."
        )

    # EDUCATION

    if education_score < 15:

        suggestions.append(
            "Add complete education details."
        )

    # PROJECTS

    if project_score == 15:

        suggestions.append(
            "Add one or two more projects."
        )

    elif project_score == 10:

        suggestions.append(
            "Add two or three more projects."
        )

    elif project_score == 0:

        suggestions.append(
            "Add practical projects to demonstrate your skills."
        )

    # SUMMARY

    if summary_text == 0:

        suggestions.append(
            "Add a professional summary or career objective."
        )

    # CERTIFICATION

    if certification_score == 0:

        suggestions.append(
            "Add relevant certifications if you have completed any."
        )

    # EXPERIENCE

    if experience_score == 0:

        suggestions.append(
            "Add internship experience or practical experience."
        )

    elif experience_score == 1:

        suggestions.append(
            "Add more details about your internship or practical experience."
        )

    # GOOD RESUME

    if len(suggestions) == 0:

        suggestions.append(
            "Your resume looks well structured. Keep updating it with new skills and projects."
        )


    # SEND RESULTS TO RESULTS.HTML

    return render_template(

        "results.html",

        resume_score=resume_score,
        resume_rating=resume_rating,

        detected_list=detected_list,
        missing_skills=missing_skills,

        matched_skills=matched_skills,
        ai_missing_skills=ai_missing_skills,

        data_matched_skills=data_matched_skills,
        data_missing_skills=data_missing_skills,

        cloud_matched_skills=cloud_matched_skills,
        cloud_missing_skills=cloud_missing_skills,

        cyber_matched_skills=cyber_matched_skills,
        cyber_missing_skills=cyber_missing_skills,

        product_matched_skills=product_matched_skills,
        product_missing_skills=product_missing_skills,

        contact_score=contact_score,
        skills_score=skills_score,
        education_score=education_score,
        project_score=project_score,
        structure_score=structure_score,
        completeness=completeness,

        ai_percentage=ai_percentage,
        data_percentage=data_percentage,
        cloud_percentage=cloud_percentage,
        cyber_percentage=cyber_percentage,
        product_percentage=product_percentage,

        suggestions=suggestions
    )

# RUN APPLICATION
if __name__ == "__main__":

    app.run(debug=True)