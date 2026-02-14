import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_resume_download():
    url = f"{BASE_URL}/resume/download-resume"
    
    # Construct a valid payload matching ResumeUserData model
    payload = {
        "user_data": {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "linkedin": "linkedin.com/in/johndoe",
                "github": "github.com/johndoe"
            },
            "education": [
                {
                    "degree": "B.Tech Computer Science",
                    "institution": "Tech University",
                    "year": "2024",
                    "gpa": "3.8"
                }
            ],
            "skills": ["Python", "JavaScript", "React", "FastAPI"],
            "projects": [
                {
                    "title": "Resume Builder",
                    "description": "Built an AI-powered resume builder",
                    "technologies": "Python, React"
                }
            ],
            "experience": [
                {
                    "role": "Software Intern",
                    "company": "Tech Corp",
                    "duration": "Summer 2023",
                    "responsibilities": "Developed backend APIs"
                }
            ],
            "certifications": ["AWS Certified Cloud Practitioner"],
            "target_role": "Backend Developer",
            "references": [],
            "professional_profile": {
                "current_status": "Student",
                "years_of_experience": 0,
                "career_goal": "To become a backend developer",
                "preferred_domain": "Web Development"
            },
            "template_type": "modern"
        },
        "generated_content": {
            "summary": "Motivated CS student...",
            "experience": [],
            "projects": []
        },
        "template_type": "modern",
        "style_options": {
            "font_family": "Arial",
            "header_alignment": "left"
        }
    }
    
    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")
            print(f"Content-Type: {content_type}")
            
            if "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type or \
               "application/octet-stream" in content_type:
                
                filename = "test_resume.docx"
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filename)
                print(f"Success! Downloaded {filename} ({file_size} bytes)")
                
                # Verify file header (PK zip signature for docx)
                with open(filename, "rb") as f:
                    header = f.read(4)
                    if header == b'PK\x03\x04':
                        print("File verification passed: Valid ZIP/DOCX header found.")
                        return True
                    else:
                        print(f"File verification failed: Invalid header {header}")
                        return False
            else:
                print(f"Unexpected Content-Type: {content_type}")
                return False
        else:
            print(f"Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Exception during test: {e}")
        return False

if __name__ == "__main__":
    success = test_resume_download()
    if success:
        print("TEST PASSED")
        exit(0)
    else:
        print("TEST FAILED")
        exit(1)
