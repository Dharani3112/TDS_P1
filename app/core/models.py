from typing import List, Optional
from pydantic import BaseModel, Field

class LinkModel(BaseModel):
    """Model for reference links in responses."""
    url: str = Field(..., description="The URL of the reference link")
    text: str = Field(..., description="Descriptive text for the link")

class QuestionRequest(BaseModel):
    """Model for incoming question requests."""
    question: str = Field(..., description="The student's question")
    image: Optional[str] = Field(None, description="Base64 encoded image data")

class QuestionResponse(BaseModel):
    """Model for question responses."""
    answer: str = Field(..., description="The answer to the student's question")
    links: List[LinkModel] = Field(..., description="Relevant reference links")

class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

class ScrapedContent(BaseModel):
    """Model for scraped content storage."""
    url: str
    title: str
    content: str
    scraped_at: str
    source_type: str  # 'course' or 'discourse'
