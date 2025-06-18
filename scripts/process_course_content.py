#!/usr/bin/env python3
"""
Process Tools in Data Science course content into a structured knowledge base.
This script processes markdown files from the course repository to create
searchable content for the Virtual TA.
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CourseContentProcessor:
    def __init__(self, course_dir: str = "tools-in-data-science-public"):
        self.course_dir = Path(course_dir)
        self.output_dir = Path("scripts/processed_course")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize data structures
        self.topics = []
        self.code_examples = []
        self.tutorials = []
        self.tools_info = []
        self.project_info = []
        
    def clean_markdown_content(self, content: str) -> str:
        """Clean markdown content by removing excessive whitespace and formatting."""
        # Remove multiple consecutive newlines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        # Remove leading/trailing whitespace
        content = content.strip()
        # Normalize whitespace
        content = re.sub(r'[ \t]+', ' ', content)
        return content
    
    def extract_code_blocks(self, content: str, filename: str) -> List[Dict[str, Any]]:
        """Extract code blocks from markdown content."""
        code_blocks = []
        
        # Pattern to match code blocks with language specification
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for i, (language, code) in enumerate(matches):
            code_blocks.append({
                "id": f"{filename}_code_{i}",
                "language": language or "unknown",
                "code": code.strip(),
                "source_file": filename
            })
        
        return code_blocks
    
    def extract_context_around_code(self, content: str, code: str) -> str:
        """Extract context around a code block."""
        # Find the position of the code block
        code_pos = content.find(code)
        if code_pos == -1:
            return ""
        
        # Extract surrounding text (up to 200 chars before and after)
        start = max(0, code_pos - 200)
        end = min(len(content), code_pos + len(code) + 200)
        context = content[start:end]
        
        # Clean up the context
        context = re.sub(r'```\w*\n.*\n```', '[CODE_BLOCK]', context, flags=re.DOTALL)
        return context.strip()
    
    def extract_headings_and_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extract headings and their content sections."""
        sections = []
        # This is a simplified implementation. A more robust solution would use a markdown parsing library.
        # For now, we'll just split by headings.
        lines = content.split('\n')
        current_heading = None
        current_content = []

        for line in lines:
            if line.startswith('#'):
                if current_heading:
                    sections.append({"heading": current_heading, "content": '\n'.join(current_content)})
                current_heading = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_heading:
            sections.append({"heading": current_heading, "content": '\n'.join(current_content)})

        return sections
    
    def categorize_content(self, filename: str, content: str) -> str:
        """Categorize content based on filename and content."""
        if "tutorial" in filename.lower():
            return "tutorial"
        if "project" in filename.lower():
            return "project"
        if "tool" in filename.lower():
            return "tool"
        return "general"
    
    def extract_tools_and_libraries(self, content: str) -> List[str]:
        """Extract tools and libraries mentioned in the content."""
        # This is a simplified implementation. A more robust solution would use a predefined list of tools and libraries.
        tools = re.findall(r'\[(.*?)\]\(http.*')', content)
        return list(set(tools))
    
    def process_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Process a single markdown file."""
        try:
            content = filepath.read_text(encoding='utf-8')
            cleaned_content = self.clean_markdown_content(content)
            
            file_info = {
                "filename": filepath.name,
                "path": str(filepath),
                "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
                "category": self.categorize_content(filepath.name, cleaned_content),
                "content": cleaned_content,
                "headings": self.extract_headings_and_sections(cleaned_content),
                "tools": self.extract_tools_and_libraries(cleaned_content),
                "code_blocks": self.extract_code_blocks(content, filepath.name)
            }
            
            return file_info
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")
            return None
    
    def process_all_files(self):
        """Process all markdown files in the course directory."""
        logger.info(f"Starting to process files in {self.course_dir}")
        for filepath in self.course_dir.rglob("*.md"):
            file_info = self.process_file(filepath)
            if file_info:
                self.topics.append(file_info)
                if file_info['category'] == 'tutorial':
                    self.tutorials.append(file_info)
                elif file_info['category'] == 'project':
                    self.project_info.append(file_info)
                elif file_info['category'] == 'tool':
                    self.tools_info.append(file_info)
                
                self.code_examples.extend(file_info['code_blocks'])
        logger.info(f"Finished processing {len(self.topics)} files.")
    
    def create_search_indices(self):
        """Create search indices for the processed data."""
        # This is a placeholder for creating search indices, e.g., using Whoosh or Elasticsearch.
        logger.info("Creating search indices...")
        pass
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Generate statistics about the processed content."""
        return {
            "total_topics": len(self.topics),
            "total_code_examples": len(self.code_examples),
            "total_tutorials": len(self.tutorials),
            "total_tools_info": len(self.tools_info),
            "total_project_info": len(self.project_info)
        }
    
    def save_processed_data(self):
        """Save the processed data to JSON files."""
        logger.info(f"Saving processed data to {self.output_dir}")
        with open(self.output_dir / "course_content.json", "w", encoding="utf-8") as f:
            json.dump(self.topics, f, indent=2)
        
        with open(self.output_dir / "code_examples.json", "w", encoding="utf-8") as f:
            json.dump(self.code_examples, f, indent=2)
            
        with open(self.output_dir / "statistics.json", "w", encoding="utf-8") as f:
            json.dump(self.generate_statistics(), f, indent=2)
        logger.info("Successfully saved processed data.")

def main():
    """Main function to process course content."""
    processor = CourseContentProcessor()
    
    # Check if course directory exists
    if not processor.course_dir.exists():
        logger.error(f"Course directory not found: {processor.course_dir}")
        logger.info("Please clone the course repository into the project directory.")
        return
    
    try:
        processor.process_all_files()
        processor.create_search_indices()
        processor.save_processed_data()
        logger.info("Course content processing completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()