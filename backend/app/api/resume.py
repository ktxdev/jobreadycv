from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.schema.resume import Resume
from app.reports.resume_pdf import create_resume_pdf

router = APIRouter()

@router.post("/api/v1/resume", response_model=Resume)
async def create_resume(request: Resume):
    output_path = '/tmp/resume.pdf'

    create_resume_pdf(request, output_path)

    return FileResponse(output_path, media_type='application/pdf', filename="resume.pdf")