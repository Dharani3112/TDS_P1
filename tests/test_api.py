import pytest
import httpx
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPI:
    """Test cases for the TDS Virtual TA API."""

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_ask_question_basic(self):
        """Test basic question asking."""
        question_data = {
            "question": "What is the Tools in Data Science course about?"
        }
        response = client.post("/api/ask", json=question_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "answer" in data
        assert "links" in data
        assert isinstance(data["answer"], str)
        assert isinstance(data["links"], list)
        
        # Validate link structure
        for link in data["links"]:
            assert "url" in link
            assert "text" in link
            assert isinstance(link["url"], str)
            assert isinstance(link["text"], str)

    def test_ask_question_with_image(self):
        """Test question asking with image data."""
        # Sample base64 encoded 1x1 pixel image
        sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        question_data = {
            "question": "What does this image show?",
            "image": sample_image
        }
        response = client.post("/api/ask", json=question_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "answer" in data
        assert "links" in data

    def test_docker_vs_podman_question(self):
        """Test the Docker vs Podman question from the evaluation."""
        question_data = {
            "question": "I know Docker but have not used Podman before. Should I use Docker for this course?"
        }
        response = client.post("/api/ask", json=question_data)
        assert response.status_code == 200
        
        data = response.json()
        answer = data["answer"].lower()
        
        # Check if the answer mentions both Docker and Podman
        assert "docker" in answer or "podman" in answer
        
        # Check if there are relevant links
        assert len(data["links"]) > 0

    def test_model_selection_question(self):
        """Test the model selection question from the evaluation."""
        question_data = {
            "question": "The question asks to use gpt-3.5-turbo-0125 model but the ai-proxy provided by Anand sir only supports gpt-4o-mini. So should we just use gpt-4o-mini or use the OpenAI API for gpt3.5 turbo?"
        }
        response = client.post("/api/ask", json=question_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "answer" in data
        assert len(data["links"]) > 0

    def test_unknown_question(self):
        """Test handling of unknown questions."""
        question_data = {
            "question": "When is the TDS Sep 2025 end-term exam?"
        }
        response = client.post("/api/ask", json=question_data)
        assert response.status_code == 200
        
        data = response.json()
        answer = data["answer"].lower()
        
        # Should indicate that the information is not available
        assert any(phrase in answer for phrase in ["don't know", "not available", "not sure", "unknown"])

    def test_invalid_question_format(self):
        """Test invalid question format handling."""
        response = client.post("/api/ask", json={})
        assert response.status_code == 422  # Validation error

    def test_status_endpoint(self):
        """Test the status endpoint."""
        response = client.get("/api/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "operational"

if __name__ == "__main__":
    pytest.main([__file__])
