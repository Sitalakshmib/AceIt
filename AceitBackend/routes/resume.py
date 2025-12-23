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

def extract_contact_info(text: str) -> dict:
    """Extract contact information from resume with improved accuracy"""
    contact_info = {}
    
    # Extract email with better pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact_info["email"] = emails[0] if emails else "Not found"
    
    # Extract phone number with multiple patterns
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # Standard US format
        r'\+?\d{10,15}',  # Continuous digits
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',  # Parentheses format
    ]
    
    phone = "Not found"
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            phone = phones[0]
            break
    contact_info["phone"] = phone
    
    # Extract LinkedIn with better pattern
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[^\s]+'
    linkedin_links = re.findall(linkedin_pattern, text)
    contact_info["linkedin"] = linkedin_links[0] if linkedin_links else "Not found"
    
    # Extract GitHub with better pattern
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[^\s]+'
    github_links = re.findall(github_pattern, text)
    contact_info["github"] = github_links[0] if github_links else "Not found"
    
    # Extract portfolio/website
    website_pattern = r'(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
    websites = re.findall(website_pattern, text)
    # Filter out common non-portfolio websites
    portfolio_sites = [site for site in websites if not any(domain in site for domain in ['linkedin.com', 'github.com', 'gmail.com', 'yahoo.com'])]
    contact_info["portfolio"] = portfolio_sites[0] if portfolio_sites else "Not found"
    
    return contact_info

def analyze_resume_sections(text: str) -> dict:
    """Analyze resume sections with improved accuracy"""
    sections = {
        "has_summary": False,
        "has_experience": False,
        "has_education": False,
        "has_skills": False,
        "has_projects": False,
        "section_details": {}
    }
    
    # Define section patterns
    section_patterns = {
        "summary": [r'\b(?:summary|objective|profile|about me)\b'],
        "experience": [r'\b(?:experience|work experience|employment|professional experience)\b'],
        "education": [r'\b(?:education|academic|university|degree)\b'],
        "skills": [r'\b(?:skills|technical skills|competencies|abilities)\b'],
        "projects": [r'\b(?:projects|portfolio|work samples)\b']
    }
    
    # Check for each section
    for section, patterns in section_patterns.items():
        found = False
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found = True
                break
        sections[f"has_{section}"] = found
        
        # Extract section content
        if found:
            # Find the section header and extract content until next section or end
            section_match = None
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    section_match = match
                    break
            
            if section_match:
                start_pos = section_match.end()
                # Find next section or end of document
                next_section_patterns = [
                    r'\b(?:summary|objective|profile|about me|experience|work experience|employment|professional experience|education|academic|university|degree|skills|technical skills|competencies|abilities|projects|portfolio|work samples)\b'
                ]
                
                next_pos = len(text)
                for next_pattern in next_section_patterns:
                    next_match = re.search(next_pattern, text[start_pos:], re.IGNORECASE)
                    if next_match and next_match.start() > 0:
                        next_pos = start_pos + next_match.start()
                        break
                
                section_content = text[start_pos:next_pos].strip()
                sections["section_details"][section] = section_content[:500]  # Limit to 500 chars
    
    return sections

def count_resume_elements(text: str) -> dict:
    """Count various elements in resume for scoring"""
    elements = {
        "bullet_points": 0,
        "action_verbs": 0,
        "quantifiable_achievements": 0,
        "dates": 0,
        "skills_mentioned": 0
    }
    
    # Count bullet points
    elements["bullet_points"] = len(re.findall(r'[\*\-\•]', text))
    
    # Count action verbs
    action_verbs = [
        "developed", "managed", "created", "implemented", "improved", "increased", "reduced", 
        "led", "designed", "optimized", "launched", "built", "maintained", "collaborated",
        "contributed", "resolved", "tested", "debugged", "documented", "presented", "communicated",
        "achieved", "generated", "saved", "boosted", "enhanced", "streamlined", "directed",
        "supervised", "coordinated", "planned", "organized", "executed", "delivered"
    ]
    
    for verb in action_verbs:
        elements["action_verbs"] += len(re.findall(r'\b' + verb + r'\b', text, re.IGNORECASE))
    
    # Count quantifiable achievements
    quantifiable_patterns = [
        r'\d+\s*%',  # percentages
        r'\$\d+',    # dollar amounts
        r'\d+\s*(?:k|million|billion)',  # large numbers
        r'\d+\s*(?:years|months)',  # time periods
        r'\d+\s*(?:projects|team members|users|clients|revenue|efficiency|performance)'
    ]
    
    for pattern in quantifiable_patterns:
        elements["quantifiable_achievements"] += len(re.findall(pattern, text, re.IGNORECASE))
    
    # Count dates (indicating experience)
    date_patterns = [
        r'\b\d{4}\b',  # Years
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{4}\b',  # Month Year
        r'\d{1,2}/\d{4}'  # MM/YYYY
    ]
    
    for pattern in date_patterns:
        elements["dates"] += len(re.findall(pattern, text, re.IGNORECASE))
    
    return elements

def analyze_ats_compatibility(text: str, contact_info: dict, sections: dict, elements: dict) -> dict:
    """Analyze ATS compatibility with realistic scoring"""
    ats_analysis = {
        "ats_score": 0,
        "contact_info_score": 0,
        "section_score": 0,
        "formatting_score": 0,
        "content_score": 0,
        "missing_elements": []
    }
    
    # Contact info scoring (max 25 points)
    contact_score = 0
    if contact_info.get("email") != "Not found":
        contact_score += 8
    else:
        ats_analysis["missing_elements"].append("Email address")
        
    if contact_info.get("phone") != "Not found":
        contact_score += 8
    else:
        ats_analysis["missing_elements"].append("Phone number")
        
    if contact_info.get("linkedin") != "Not found":
        contact_score += 5
    if contact_info.get("github") != "Not found":
        contact_score += 4
    
    ats_analysis["contact_info_score"] = contact_score
    
    # Section scoring (max 30 points)
    section_score = 0
    required_sections = ["summary", "experience", "education", "skills"]
    for section in required_sections:
        if sections.get(f"has_{section}", False):
            section_score += 7
    
    if sections.get("has_projects", False):
        section_score += 2
    
    ats_analysis["section_score"] = section_score
    
    # Formatting scoring (max 20 points)
    formatting_score = 0
    if elements["bullet_points"] >= 5:
        formatting_score += 10
    elif elements["bullet_points"] >= 1:
        formatting_score += 5
    else:
        ats_analysis["missing_elements"].append("More bullet points")
    
    if elements["action_verbs"] >= 10:
        formatting_score += 10
    elif elements["action_verbs"] >= 5:
        formatting_score += 5
    else:
        ats_analysis["missing_elements"].append("More action verbs")
    
    ats_analysis["formatting_score"] = formatting_score
    
    # Content scoring (max 25 points)
    content_score = 0
    if elements["quantifiable_achievements"] >= 3:
        content_score += 10
    elif elements["quantifiable_achievements"] >= 1:
        content_score += 5
    else:
        ats_analysis["missing_elements"].append("Quantifiable achievements")
    
    if elements["dates"] >= 4:
        content_score += 10
    elif elements["dates"] >= 2:
        content_score += 5
    else:
        ats_analysis["missing_elements"].append("More dated experience entries")
    
    # Check for keywords
    keyword_count = 0
    common_keywords = ["experience", "skills", "education", "projects", "achievements", 
                      "responsibilities", "proficient", "expertise", "certifications"]
    for keyword in common_keywords:
        if keyword in text.lower():
            keyword_count += 1
    
    if keyword_count >= 8:
        content_score += 5
    elif keyword_count >= 5:
        content_score += 3
    
    ats_analysis["content_score"] = content_score
    
    # Calculate overall ATS score
    ats_analysis["ats_score"] = contact_score + section_score + formatting_score + content_score
    
    return ats_analysis

def analyze_skills_match(resume_text: str, job_role: str) -> dict:
    """Analyze skills match with improved accuracy"""
    # Get required skills for the job role
    required_skills = JOB_ROLE_SKILLS.get(job_role, [])
    
    if not required_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "total_required_skills": 0,
            "matched_skills_count": 0
        }
    
    # Find matching skills
    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        # Check for exact match first
        if skill.lower() in resume_text.lower():
            matched_skills.append(skill)
        else:
            # Check for partial matches
            skill_words = skill.lower().split()
            found_words = 0
            for word in skill_words:
                # Look for the word in the resume
                if re.search(r'\b' + re.escape(word) + r'\b', resume_text.lower()):
                    found_words += 1
            
            # If at least half the words are found, consider it a match
            if found_words >= max(1, len(skill_words) // 2):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
    
    # Calculate match score (0-100)
    match_score = (len(matched_skills) / len(required_skills)) * 100
    
    return {
        "match_score": round(match_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": len(required_skills),
        "matched_skills_count": len(matched_skills)
    }

def generate_detailed_feedback(ats_analysis: dict, skills_analysis: dict, contact_info: dict, sections: dict) -> list:
    """Generate detailed, actionable feedback"""
    feedback = []
    
    # ATS feedback
    if ats_analysis["ats_score"] < 50:
        feedback.append("Your resume needs significant improvements to pass ATS systems.")
    elif ats_analysis["ats_score"] < 70:
        feedback.append("Your resume has room for improvement to better pass ATS systems.")
    else:
        feedback.append("Your resume is well-structured for ATS systems.")
    
    # Contact info feedback
    missing_contact = []
    if contact_info.get("email") == "Not found":
        missing_contact.append("email address")
    if contact_info.get("phone") == "Not found":
        missing_contact.append("phone number")
    
    if missing_contact:
        feedback.append(f"Add your {' and '.join(missing_contact)} for direct contact.")
    
    # Section feedback
    missing_sections = []
    required_sections = ["summary", "experience", "education", "skills"]
    for section in required_sections:
        if not sections.get(f"has_{section}", False):
            missing_sections.append(section.capitalize())
    
    if missing_sections:
        feedback.append(f"Add these sections: {', '.join(missing_sections)}")
    
    # Skills feedback
    if skills_analysis["match_score"] < 60:
        missing_skills = skills_analysis.get("missing_skills", [])
        if missing_skills:
            feedback.append(f"Add these relevant skills: {', '.join(missing_skills[:3])}")
    
    # Formatting feedback
    if ats_analysis["formatting_score"] < 10:
        feedback.append("Use more bullet points and action verbs to describe your achievements.")
    
    # Content feedback
    if ats_analysis["content_score"] < 15:
        feedback.append("Include quantifiable achievements with numbers, percentages, or dollar amounts.")
    
    if not feedback:
        feedback.append("Your resume looks strong! Consider adding more specific achievements to make it even better.")
    
    return feedback

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(None),
    job_role: str = Form(...),
    user_id: str = Form(...),
    resume_text: str = Form(None)
):
    """
    Analyze resume with accurate, realistic assessment
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
    
    # Extract contact information
    contact_info = extract_contact_info(processed_text)
    
    # Analyze resume sections
    sections = analyze_resume_sections(processed_text)
    
    # Count resume elements
    elements = count_resume_elements(processed_text)
    
    # Analyze ATS compatibility
    ats_analysis = analyze_ats_compatibility(processed_text, contact_info, sections, elements)
    
    # Analyze skills match
    skills_analysis = analyze_skills_match(processed_text, job_role)
    
    # Generate overall score (weighted average)
    # ATS score (60%) + Skills score (40%)
    overall_score = (ats_analysis["ats_score"] * 0.6) + (skills_analysis["match_score"] * 0.4)
    
    # Ensure score is within 0-100 range
    overall_score = max(0, min(100, overall_score))
    
    # Generate detailed feedback
    suggestions = generate_detailed_feedback(ats_analysis, skills_analysis, contact_info, sections)
    
    # Generate overall feedback
    if overall_score >= 80:
        overall_feedback = "Excellent! Your resume is well-optimized for both ATS systems and human reviewers."
    elif overall_score >= 65:
        overall_feedback = "Good resume with some room for improvement. Address the suggestions to make it stronger."
    elif overall_score >= 50:
        overall_feedback = "Fair resume that needs significant improvements to be competitive."
    else:
        overall_feedback = "Your resume needs major revisions to meet industry standards."
    
    # Compile analysis results
    analysis = {
        "job_role": job_role,
        "text_length": len(processed_text),
        "contact_info": contact_info,
        "sections": sections,
        "elements": elements,
        "ats_analysis": ats_analysis,
        "skills_analysis": skills_analysis,
        "overall_score": round(overall_score, 2),
        "overall_feedback": overall_feedback,
        "suggestions": suggestions
    }
    
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