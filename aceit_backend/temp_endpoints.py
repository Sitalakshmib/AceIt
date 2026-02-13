
@router.post("/generate-content")
async def generate_resume_content(request: ResumeCreationRequest):
    """
    Generate structured resume content using AI for the user to review.
    Does NOT generate the file yet.
    """
    try:
        # Convert request to dict
        user_data = {
            "personal_info": request.personal_info.dict(),
            "education": [e.dict() for e in request.education],
            "skills": request.skills,
            "projects": [p.dict() for p in request.projects],
            "experience": [e.dict() for e in request.experience] if request.experience else [],
            "certifications": request.certifications or [],
            "target_role": request.target_role or "software_developer",
            "references": [r.dict() for r in request.references] if request.references else []
        }
        
        # KEY FIX: Generate content based on request data, NOT just passing empty dicts if optional
        # The AI needs the raw inputs to smooth them out
        
        ai_content = generate_resume_content_with_ai(
            user_data, 
            user_data["target_role"],
            request.professional_profile.dict(),
            request.template_type
        )
        
        return {"content": ai_content, "user_data": user_data}
        
    except Exception as e:
        print(f"[ERROR] Content generation failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download-resume")
async def download_resume_file(request: ResumeDownloadRequest):
    """
    Generate and download the final DOCX file using confirmed content.
    """
    try:
        # Create Word document
        resume_file = create_word_resume(request.user_data, request.ai_content, request.template_type)
        
        # Generate filename
        filename = f"{request.user_data['personal_info']['name'].replace(' ', '_')}_Resume.docx"
        
        return StreamingResponse(
            resume_file,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"[ERROR] file generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
