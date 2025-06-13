<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# TDS Virtual TA Project - Copilot Instructions

## Project Overview
This is a Virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras. The project uses FastAPI, web scraping, and LLM integration to answer student questions.

## Key Technologies
- **Backend**: Python 3.11+ with FastAPI
- **LLM**: OpenAI GPT models
- **Web Scraping**: BeautifulSoup, Requests
- **Database**: MongoDB (optional)
- **Deployment**: Docker, Docker Compose

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Include docstrings for all classes and functions
- Use async/await for I/O operations
- Handle exceptions gracefully with proper logging

## API Response Format
All API responses must follow this exact JSON schema:
```json
{
  "answer": "string",
  "links": [
    {
      "url": "string",
      "text": "string"
    }
  ]
}
```

## Key Files
- `app/main.py`: FastAPI application entry point
- `app/api/endpoints.py`: API route definitions
- `app/services/qa_service.py`: Main question answering logic
- `app/services/llm_service.py`: OpenAI integration
- `app/services/scraper.py`: Web scraping utilities
- `app/core/models.py`: Pydantic data models
- `app/core/config.py`: Configuration management

## Testing Requirements
- Ensure API responses match the required JSON schema
- Test with the promptfoo evaluation framework
- Handle edge cases like unknown questions gracefully
- Validate image processing functionality

## Security Considerations
- Validate all input data
- Sanitize scraped content
- Use environment variables for sensitive data
- Implement proper error handling without exposing internals

## Performance Requirements
- API responses must be within 30 seconds
- Implement efficient knowledge base search
- Use caching where appropriate
- Optimize LLM token usage
