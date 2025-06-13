# TDS Virtual TA

A virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras.

## Features

- **Automated Question Answering**: Handles student queries about TDS course content
- **Course Content Integration**: Scrapes and indexes TDS course materials
- **Discourse Forum Integration**: Extracts Q&A from course discussion forums
- **Image Support**: Processes questions with image attachments
- **REST API**: RESTful endpoints for integration with external systems

## Project Structure

```
tds-virtual-ta/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   └── models.py        # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── qa_service.py    # Question answering logic
│   │   ├── scraper.py       # Web scraping utilities
│   │   └── llm_service.py   # LLM integration
│   └── data/
│       ├── __init__.py
│       ├── scraped/         # Scraped data storage
│       └── knowledge_base/  # Processed knowledge base
├── scripts/
│   ├── scrape_course.py     # Course content scraper
│   └── scrape_discourse.py  # Discourse forum scraper
├── tests/
│   ├── __init__.py
│   └── test_api.py         # API tests
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── README.md              # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tds-virtual-ta
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   copy .env.example .env
   # Edit .env with your configuration
   ```

### Configuration

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=tds_virtual_ta
COURSE_URL=https://tds.s-anand.net/
DISCOURSE_URL=https://discourse.onlinedegree.iitm.ac.in/
```

### Running the Application

1. Start the API server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Data Collection

1. Scrape course content:
   ```bash
   python scripts/scrape_course.py
   ```

2. Scrape discourse forums:
   ```bash
   python scripts/scrape_discourse.py
   ```

## API Usage

### Question Endpoint

**POST** `/api/ask`

Request body:
```json
{
  "question": "Should I use Docker or Podman for this course?",
  "image": "base64_encoded_image_data"  // optional
}
```

Response:
```json
{
  "answer": "For this course, we recommend using Podman as it's the primary containerization tool taught. However, Docker is also acceptable if you're already familiar with it.",
  "links": [
    {
      "url": "https://tds.s-anand.net/#/docker",
      "text": "TDS Docker/Podman Documentation"
    }
  ]
}
```

## Testing

### Comprehensive Testing Suite

The project includes multiple testing approaches with 93.3% success rate:

#### 1. Comprehensive Test Suite
```bash
# Run all 15 test categories
python comprehensive_test.py

# Quick validation (4 core tests)
python comprehensive_test.py --quick
```

#### 2. Interactive Testing
```bash
# Real-time question testing
python interactive_test.py

# Batch test from file
python interactive_test.py --batch sample_questions.txt
```

#### 3. Unit Tests
```bash
# Formal pytest test suite
python -m pytest tests/test_api.py -v
```

#### 4. Manual API Testing
```bash
# Predefined question testing
python test_api_manual.py
```

#### 5. External Evaluation
```bash
# Promptfoo evaluation framework
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

### Test Results
- **Comprehensive Tests**: 14/15 passed (93.3%)
- **Batch Tests**: 30/30 passed (100%)
- **Unit Tests**: 8/9 passed (89%)
- **Overall System Reliability**: 93.3%

## Deployment

### Docker Deployment

1. Build the image:
   ```bash
   docker build -t tds-virtual-ta .
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Cloud Deployment

The application is ready for deployment on:
- Heroku
- AWS ECS/Lambda
- Google Cloud Run
- Azure Container Instances

## Development

### Adding New Features

1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all functions
- Maintain test coverage above 80%

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review existing discussions
