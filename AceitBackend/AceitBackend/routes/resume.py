from fastapi import APIRouter, UploadFile, File, Form
import re
from datetime import datetime
from database import progress_data
import pdfplumber
from PyPDF2 import PdfReader
from io import BytesIO

router = APIRouter()

# Required skills for different job roles
JOB_ROLE_SKILLS = {
    "software_developer": ["python", "java", "javascript", "sql", "git", "rest api", "docker", "react", "node.js", "aws", "mongodb", "postgresql", "html", "css", "typescript"],
    "data_scientist": ["python", "r", "sql", "machine learning", "statistics", "pandas", "numpy", "matplotlib", "scikit-learn", "tensorflow", "pytorch", "data visualization", "deep learning"],
    "frontend_developer": ["javascript", "react", "html", "css", "typescript", "redux", "vue.js", "angular", "bootstrap", "sass", "webpack", "jquery", "responsive design"],
    "backend_developer": ["python", "java", "node.js", "sql", "mongodb", "aws", "docker", "postgresql", "mysql", "rest api", "microservices", "redis", "kubernetes"],
    "full_stack_developer": ["javascript", "react", "node.js", "html", "css", "python", "sql", "mongodb", "aws", "docker", "typescript", "postgresql", "rest api"],
    "machine_learning_engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "data preprocessing", "neural networks", "computer vision", "nlp"],
    "devops_engineer": ["docker", "kubernetes", "aws", "jenkins", "terraform", "ansible", "git", "linux", "ci/cd", "prometheus", "grafana", "nginx"],
    "product_manager": ["product strategy", "market research", "agile", "scrum", "user experience", "data analysis", "stakeholder management", "product roadmap", "a/b testing", "customer development"]
}

# ATS-friendly keywords
ATS_KEYWORDS = [
    "experience", "skills", "education", "projects", "achievements", "responsibilities",
    "proficient", "expertise", "certifications", "qualifications", "summary", "objective",
    "contact", "email", "phone", "linkedin", "github", "portfolio", "work", "internship",
    "bachelor", "master", "phd", "university", "degree", "gpa", "graduated", "graduation",
    "developed", "implemented", "managed", "led", "created", "designed", "optimized",
    "increased", "decreased", "improved", "reduced", "launched", "built", "maintained"
]

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF using multiple methods for better accuracy"""
    text = ""
    
    # Method 1: Using pdfplumber (better for text extraction)
    try:
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
    
    # Method 2: Using PyPDF2 as fallback
    if not text.strip():
        try:
            pdf_reader = PdfReader(BytesIO(file_content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
    
    return text.strip()

def preprocess_text(text: str) -> str:
    """Clean and preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces and basic punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def analyze_ats_friendlyness(text: str) -> dict:
    """Analyze how ATS-friendly the resume is"""
    ats_score = 0
    found_keywords = []
    missing_keywords = []
    
    # Check for presence of key ATS keywords
    for keyword in ATS_KEYWORDS:
        if keyword.lower() in text.lower():
            ats_score += 1
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    # Calculate ATS score (out of 100)
    if ATS_KEYWORDS:
        ats_score = (ats_score / len(ATS_KEYWORDS)) * 100
    
    # Check for proper formatting
    formatting_score = 0
    formatting_issues = []
    
    # Check for clear section headers
    section_headers = ["experience", "education", "skills", "projects", "summary"]
    found_sections = [header for header in section_headers if header in text.lower()]
    formatting_score += len(found_sections) * 10
    
    if len(found_sections) < 3:
        formatting_issues.append("Missing key sections (Experience, Education, Skills)")
    
    # Check for bullet points (indicates good formatting)
    bullet_points = text.count("•") + text.count("-") + text.count("*")
    if bullet_points > 5:
        formatting_score += 20
    else:
        formatting_issues.append("Consider using more bullet points for better readability")
    
    # Check for action verbs
    action_verbs = ["developed", "managed", "created", "implemented", "improved", "increased", "led", "designed"]
    action_verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    formatting_score += min(action_verb_count * 5, 30)
    
    # Normalize formatting score
    formatting_score = min(formatting_score, 100)
    
    # Overall ATS score
    overall_ats_score = (ats_score + formatting_score) / 2
    
    return {
        "ats_score": round(overall_ats_score, 2),
        "keyword_match_score": round(ats_score, 2),
        "formatting_score": formatting_score,
        "found_keywords": found_keywords[:10],  # Limit to top 10
        "missing_keywords": missing_keywords[:10],  # Limit to top 10
        "formatting_issues": formatting_issues
    }

def extract_contact_info(text: str) -> dict:
    """Extract contact information from resume"""
    contact_info = {}
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact_info["email"] = emails[0] if emails else None
    
    # Extract phone number
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    contact_info["phone"] = phones[0] if phones else None
    
    # Extract LinkedIn/GitHub links
    linkedin_pattern = r'linkedin\.com/[^\s]+'
    github_pattern = r'github\.com/[^\s]+'
    
    linkedin_links = re.findall(linkedin_pattern, text)
    github_links = re.findall(github_pattern, text)
    
    contact_info["linkedin"] = linkedin_links[0] if linkedin_links else None
    contact_info["github"] = github_links[0] if github_links else None
    
    return contact_info

def extract_experience_details(text: str) -> dict:
    """Extract detailed experience information"""
    experience_info = {
        "total_experience_years": 0,
        "companies": [],
        "positions": [],
        "achievements": []
    }
    
    # Extract years of experience
    experience_patterns = [
        r'(\d+)\+?\s*years?.*?experience',
        r'experience.*?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?.*?professional',
        r'professional.*?(\d+)\+?\s*years?'
    ]
    
    for pattern in experience_patterns:
        match = re.search(pattern, text.lower())
        if match:
            experience_info["total_experience_years"] = int(match.group(1))
            break
    
    # Extract company names (look for capitalized words that might be company names)
    # This is a simplified approach - in a real system, you'd use NER
    company_pattern = r'(?:at|with|for)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)'
    companies = re.findall(company_pattern, text)
    experience_info["companies"] = list(set(companies))[:5]  # Limit to 5 unique companies
    
    # Extract positions
    position_keywords = ["developer", "engineer", "manager", "analyst", "specialist", "consultant", "lead", "senior"]
    positions = []
    for keyword in position_keywords:
        pattern = rf'([A-Za-z\s]+{keyword}[A-Za-z\s]*)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        positions.extend(matches)
    experience_info["positions"] = list(set(positions))[:5]  # Limit to 5 unique positions
    
    # Extract achievements (sentences with numbers/percentages)
    achievement_patterns = [
        r'[A-Za-z\s]+(?:increased|decreased|improved|reduced|achieved|generated|saved|boosted)[^.]*?(?:\d+[%]|\d+\s*(?:percent|%)|\$\d+|\d+\s*(?:k|million|billion))[^.]*',
        r'[A-Za-z\s]+(?:led|managed|developed|created|built)[^.]*?(?:\d+\s*(?:projects|team members|users|clients))[^.]*'
    ]
    
    achievements = []
    for pattern in achievement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        achievements.extend(matches)
    
    experience_info["achievements"] = achievements[:5]  # Limit to 5 achievements
    
    return experience_info

def analyze_skills_match(resume_text: str, job_role: str) -> dict:
    """Analyze how well resume skills match the job role requirements"""
    resume_text_lower = resume_text.lower()
    
    # Get required skills for the job role
    required_skills = JOB_ROLE_SKILLS.get(job_role, [])
    
    # Find matching skills
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        # Check for exact match or partial match
        if skill.lower() in resume_text_lower:
            matched_skills.append(skill)
        else:
            # Check for partial matches (substrings)
            skill_words = skill.lower().split()
            if any(word in resume_text_lower for word in skill_words):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
    
    # Calculate match score
    if required_skills:
        match_score = (len(matched_skills) / len(required_skills)) * 100
    else:
        match_score = 0
    
    return {
        "match_score": round(match_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:10],  # Limit to top 10
        "total_required_skills": len(required_skills),
        "matched_skills_count": len(matched_skills)
    }

def generate_improvement_suggestions(analysis_results: dict, job_role: str) -> list:
    """Generate actionable suggestions for resume improvement"""
    suggestions = []
    
    # ATS-related suggestions
    ats_analysis = analysis_results.get("ats_analysis", {})
    if ats_analysis.get("ats_score", 0) < 70:
        suggestions.append("Add more ATS-friendly keywords to improve parsing by applicant tracking systems")
        missing_keywords = ats_analysis.get("missing_keywords", [])
        if missing_keywords:
            suggestions.append(f"Consider adding these important keywords: {', '.join(missing_keywords[:5])}")
    
    formatting_issues = ats_analysis.get("formatting_issues", [])
    suggestions.extend(formatting_issues)
    
    # Skills-related suggestions
    skills_analysis = analysis_results.get("skills_analysis", {})
    if skills_analysis.get("match_score", 0) < 60:
        missing_skills = skills_analysis.get("missing_skills", [])
        if missing_skills:
            suggestions.append(f"Add these job-relevant skills: {', '.join(missing_skills[:5])}")
    
    # Experience-related suggestions
    experience_info = analysis_results.get("experience_info", {})
    if experience_info.get("total_experience_years", 0) < 2:
        suggestions.append("Highlight personal projects, internships, and coursework to compensate for limited professional experience")
    
    # Achievement suggestions
    achievements = experience_info.get("achievements", [])
    if len(achievements) < 3:
        suggestions.append("Include more quantifiable achievements with specific numbers, percentages, or dollar amounts")
    
    # Contact information suggestions
    contact_info = analysis_results.get("contact_info", {})
    if not contact_info.get("email"):
        suggestions.append("Add your email address for direct contact")
    if not contact_info.get("phone"):
        suggestions.append("Include your phone number for easy communication")
    if not contact_info.get("linkedin"):
        suggestions.append("Add your LinkedIn profile to showcase your professional network")
    if not contact_info.get("github") and "developer" in job_role.lower():
        suggestions.append("Include your GitHub profile to showcase your coding projects")
    
    # General suggestions if no specific issues found
    if not suggestions:
        suggestions.append("Your resume looks strong! Consider adding more quantifiable achievements to make it even better.")
        suggestions.append("Review your resume for any typos or grammatical errors.")
        suggestions.append("Ensure your most relevant experience is highlighted at the top.")
    
    return suggestions

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(None),
    job_role: str = Form(...),
    user_id: str = Form(...),
    resume_text: str = Form(None)  # For demo - in real app, process PDF file
):
    """
    Analyze resume against job role requirements with ATS-friendly analysis
    """
    # Extract text from PDF if provided
    if file and file.filename:
        # Read file content
        file_content = await file.read()
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_content)
        
        if not resume_text.strip():
            return {
                "error": "Could not extract text from the uploaded PDF. Please ensure it's a text-based PDF (not scanned image)."
            }
    elif not resume_text:
        return {
            "error": "Please provide either a PDF file or resume text for analysis."
        }
    
    # Preprocess text
    processed_text = preprocess_text(resume_text)
    
    # Perform comprehensive analysis
    analysis = {
        "job_role": job_role,
        "text_length": len(processed_text),
        "ats_analysis": analyze_ats_friendlyness(processed_text),
        "skills_analysis": analyze_skills_match(processed_text, job_role),
        "contact_info": extract_contact_info(processed_text),
        "experience_info": extract_experience_details(processed_text)
    }
    
    # Generate overall score
    ats_score = analysis["ats_analysis"]["ats_score"]
    skills_score = analysis["skills_analysis"]["match_score"]
    overall_score = (ats_score * 0.4) + (skills_score * 0.6)
    
    analysis["overall_score"] = round(overall_score, 2)
    
    # Generate suggestions
    analysis["suggestions"] = generate_improvement_suggestions(analysis, job_role)
    
    # Generate overall feedback
    if overall_score >= 80:
        analysis["overall_feedback"] = "Excellent! Your resume is well-optimized for both ATS systems and human reviewers."
    elif overall_score >= 60:
        analysis["overall_feedback"] = "Good resume with some room for improvement. Address the suggestions to make it stronger."
    elif overall_score >= 40:
        analysis["overall_feedback"] = "Fair resume that needs significant improvements to be competitive."
    else:
        analysis["overall_feedback"] = "Your resume needs major revisions to meet industry standards."
    
    # Save progress
    progress_data.append({
        "user_id": user_id,
        "module": "resume_analysis",
        "score": analysis["overall_score"],
        "timestamp": datetime.utcnow(),
        "job_role": job_role,
        "analysis": analysis
    })
    
    return analysis

@router.get("/job-roles")
async def get_job_roles():
    """Get available job roles for analysis"""
    return [{"id": key, "name": key.replace("_", " ").title()} for key in JOB_ROLE_SKILLS.keys()]