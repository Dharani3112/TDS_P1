import openai
import base64
import io
import httpx
from typing import List, Optional
from app.core.config import settings
from app.core.models import LinkModel
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Service for handling LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM service with AI Pipe or OpenAI client."""
        # Try AI Pipe first, then fall back to OpenAI
        if settings.aipipe_token:
            logger.info("Using AI Pipe API for LLM functionality")
            self.use_aipipe = True
            self.client = None  # We'll use httpx for AI Pipe
        elif settings.openai_api_key:
            logger.info("Using OpenAI API for LLM functionality")
            self.use_aipipe = False
            openai.api_key = settings.openai_api_key
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        else:
            logger.warning("No AI API configured. LLM functionality will be limited.")
            self.use_aipipe = False
            self.client = None
    
    async def generate_answer(
        self, 
        question: str, 
        context: str, 
        image_data: Optional[str] = None
    ) -> str:
        """
        Generate an answer using LLM based on the question and context.
        
        Args:
            question: The student's question
            context: Relevant context from scraped data
            image_data: Optional base64 encoded image        Returns:
            Generated answer string
        """
        try:
            if self.use_aipipe and settings.aipipe_token:
                return await self._generate_answer_aipipe(question, context, image_data)
            elif self.client:
                return await self._generate_answer_openai(question, context, image_data)
            else:
                return "I'm sorry, but no AI API is configured. Please provide a valid API token to enable AI-powered responses."
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I apologize, but I'm having trouble processing your question right now. Please try again later or contact the course staff for assistance."
    
    async def _generate_answer_aipipe(
        self, 
        question: str, 
        context: str, 
        image_data: Optional[str] = None
    ) -> str:
        """Generate answer using AI Pipe API."""
        try:
            # Prepare the system prompt
            system_prompt = """You are a virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras. 
            Your role is to help students with course-related questions based on the provided context.

            Guidelines:
            - Answer based on the provided context from course materials and discourse discussions
            - Be helpful, accurate, and concise
            - If you don't know something, say so clearly
            - Reference specific course materials when applicable
            - Maintain a friendly but professional tone
            - For technical questions, provide clear explanations
            """
            
            # Prepare the user prompt
            user_prompt = f"""
            Context from course materials and discussions:
            {context}
            
            Student Question: {question}
            
            Please provide a helpful answer based on the context above.
            """
            
            # Prepare the request payload for AI Pipe
            payload = {
                "model": settings.default_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": settings.max_tokens,
                "temperature": settings.temperature
            }
            
            # Handle image if provided (simplified for AI Pipe)
            if image_data:
                payload["messages"][-1]["content"] = [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_data}"}
                    }
                ]
              # Make request to AI Pipe
            async with httpx.AsyncClient() as client:
                # Try the correct AI Pipe endpoint
                response = await client.post(
                    "https://aipipe.org/api/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.aipipe_token}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            logger.error(f"Error with AI Pipe API: {e}")
            raise e
    
    async def _generate_answer_openai(
        self, 
        question: str, 
        context: str, 
        image_data: Optional[str] = None
    ) -> str:
        """Generate answer using OpenAI API (fallback)."""
        try:
            # Prepare the system prompt
            system_prompt = """You are a virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras. 
            Your role is to help students with course-related questions based on the provided context.

            Guidelines:
            - Answer based on the provided context from course materials and discourse discussions
            - Be helpful, accurate, and concise
            - If you don't know something, say so clearly
            - Reference specific course materials when applicable
            - Maintain a friendly but professional tone
            - For technical questions, provide clear explanations
            """
            
            # Prepare the user prompt
            user_prompt = f"""
            Context from course materials and discussions:
            {context}
            
            Student Question: {question}
            
            Please provide a helpful answer based on the context above.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
              # Handle image if provided
            if image_data:
                try:
                    # For now, we'll skip image processing since PIL is not available
                    # In a full implementation, you would process the image here
                    logger.info("Image provided but processing is not available without PIL")
                    # You could add PIL back to requirements.txt if image processing is needed
                except Exception as e:
                    logger.warning(f"Error processing image: {e}")
            
            # Generate response
            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise Exception(f"Failed to generate answer: {str(e)}")
    
    async def extract_relevant_links(
        self, 
        question: str, 
        all_links: List[dict]
    ) -> List[LinkModel]:
        """
        Use LLM to determine which links are most relevant to the question.
        
        Args:
            question: The student's question
            all_links: List of all available links with metadata        Returns:
            List of most relevant LinkModel objects
        """
        try:
            if self.use_aipipe and settings.aipipe_token:
                return await self._extract_relevant_links_aipipe(question, all_links)
            elif self.client:
                return await self._extract_relevant_links_openai(question, all_links)
            else:
                # Return first few links as fallback when no AI is available
                return [
                    LinkModel(url=link['url'], text=link.get('title', link['url']))
                    for link in all_links[:2]
                ]
                
            if not all_links:
                return []
            
            # Prepare links context
            links_context = "\n".join([
                f"- URL: {link['url']}, Title: {link.get('title', 'N/A')}, Content Preview: {link.get('content', 'N/A')[:200]}..."
                for link in all_links[:20]  # Limit to prevent token overflow
            ])
            
            prompt = f"""
            Given the student question and available links, identify the 2-3 most relevant links.
            
            Question: {question}
            
            Available Links:
            {links_context}
            
            Return only the URLs of the most relevant links, one per line, with no additional text.
            """
            
            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1
            )
            
            # Parse response to get URLs
            relevant_urls = [
                url.strip() 
                for url in response.choices[0].message.content.split('\n') 
                if url.strip() and url.strip().startswith('http')
            ]
            
            # Create LinkModel objects
            relevant_links = []
            for link in all_links:
                if link['url'] in relevant_urls:
                    relevant_links.append(LinkModel(
                        url=link['url'],
                        text=link.get('title', link['url'])
                    ))
            
            return relevant_links[:3]  # Limit to 3 links
            
        except Exception as e:
            logger.error(f"Error extracting relevant links: {e}")
            # Return first few links as fallback
            return [
                LinkModel(url=link['url'], text=link.get('title', link['url']))
                for link in all_links[:2]
            ]
