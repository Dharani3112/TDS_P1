# 🤖 TDS Virtual Teaching Assistant

An intelligent, AI-powered Virtual Teaching Assistant designed specifically for the Tools in Data Science (TDS) course. This system provides instant, contextual responses to student questions with comprehensive course integration and multimodal support.

## 🚀 Key Features

✨ **Intelligent AI Responses** - Powered by Google's Gemini 2.0 Flash for accurate, context-aware answers  
🔍 **Advanced Semantic Search** - Lightning-fast retrieval from 309 pre-computed course content embeddings  
📸 **Multimodal Support** - Analyze and respond to both text questions and uploaded images/screenshots  
🔗 **Smart Course Integration** - Automatic linking to relevant course materials and discussion threads  
⚡ **Optimized Performance** - Sub-2-second response times with efficient caching mechanisms  

## 🛠️ Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed and a valid Gemini API key.

### Installation & Setup

1. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Your API Key**
   ```bash
   # Windows (PowerShell/CMD)
   set GEMINI_API_KEY=your_gemini_api_key_here
   
   # Linux/macOS (Bash/Zsh)
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Launch the Virtual TA Server**
   ```bash
   python virtual_ta.py
   ```

4. **Verify Installation (Optional)**
   ```bash
   python test_virtual_ta_api.py
   ```

## 📡 API Reference

### Endpoint
**POST** `http://localhost:5000/api/`

### Request Format
```json
{
  "question": "How does the GPT model work in natural language processing?",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..." // Optional base64-encoded image
}
```

### Response Format
```json
{
  "answer": "The GPT (Generative Pre-trained Transformer) model is a transformer-based language model that...",
  "links": [
    {
      "text": "Introduction to Large Language Models",
      "url": "https://discourse.tds-course.com/topic/12345"
    },
    {
      "text": "Week 8 - Transformer Architectures",
      "url": "https://course-materials.tds.edu/week8/transformers.pdf"
    }
  ],
  "search_results_count": 6
}
```

## ✅ Quality Assurance

Our comprehensive testing suite validates system reliability across diverse scenarios:

- **✅ Technical Concept Explanations** - Accurate responses about machine learning models and algorithms
- **✅ Assessment Information** - Precise details about grading criteria and evaluation methods  
- **✅ Tool Recommendations** - Expert guidance on development tools and best practices
- **✅ Temporal Query Handling** - Smart responses to time-sensitive questions about future events
- **✅ Comprehensive Integration** - Seamless linking to relevant course resources and discussions

## 🏗️ System Architecture

### Core Components
- **🌐 Flask Web Framework** - Robust HTTP API with RESTful endpoints
- **🧠 Google Gemini 2.0 Flash** - Advanced language model for text generation and image analysis
- **🔍 Text Embedding 004** - State-of-the-art semantic search capabilities
- **📊 NumPy Computing Engine** - High-performance similarity calculations and vector operations
- **💾 Intelligent Caching** - Pre-computed embeddings for instantaneous content retrieval

### Performance Optimization
- **Memory-Efficient Storage** - Compressed embedding cache for minimal memory footprint
- **Lazy Loading** - Dynamic resource loading to reduce startup time
- **Vectorized Operations** - Optimized mathematical computations for semantic search

## 📈 Content Database

### Comprehensive Course Coverage
- **💬 165 Discourse Topics** - Complete student discussions and Q&A threads
- **📚 143 Course Materials** - Official lectures, assignments, and documentation
- **🔢 309 Semantic Embeddings** - High-dimensional vectors (768 dimensions each) for precise content matching
- **⚡ 1.8MB Cache System** - Optimized storage for instant application startup and query processing

---

*Built with ❤️ for the TDS community - Empowering students with intelligent, accessible learning support.*