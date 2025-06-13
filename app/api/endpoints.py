from fastapi import APIRouter, HTTPException, UploadFile, File
from app.core.models import QuestionRequest, QuestionResponse
from app.services.qa_service import QAService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize QA service
qa_service = QAService()

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Process a student question and return an answer with relevant links.
    
    Args:
        request: QuestionRequest containing the question and optional image
        
    Returns:
        QuestionResponse with answer and relevant links
    """
    try:
        logger.info(f"Received question: {request.question[:100]}...")
        
        # Process the question
        response = await qa_service.answer_question(
            question=request.question,
            image_data=request.image
        )
        
        logger.info(f"Generated response with {len(response.links)} links")
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

@router.get("/status")
async def get_status():
    """Get the status of the QA service."""
    try:
        status = await qa_service.get_status()
        return {"status": "operational", "details": status}
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return {"status": "error", "details": str(e)}
