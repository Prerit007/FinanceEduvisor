# FinanceEduvisor

A modular, LlamaIndex-powered financial education and guidance system that combines educational content with personalized financial advice.

## Overview

FinanceEduvisor is an intelligent assistant that can:
- Answer educational questions about financial concepts, terms, and principles
- Provide general financial guidance based on user profiles
- Route queries to appropriate specialized agents (Teacher or Guide)
- Maintain context-aware conversations for better user experience

## Features

- **Dual-Mode Operation**: 
  - Educational Mode: Explains financial concepts, terms, and principles
  - Guidance Mode: Provides personalized financial advice based on user profiles

- **Intelligent Routing**: Automatically determines whether a query requires educational content or financial guidance

- **Context-Aware Conversations**: Maintains conversation history for more natural interactions

- **Knowledge Base Integration**: Uses curated knowledge bases for both educational content and financial guidance

## Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FinanceEduvisor.git
cd FinanceEduvisor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Google API key:
GOOGLE_API_KEY=your_api_key_here

## Required Libraries

The following libraries are required to run the system:

```bash
pip install llama-index
pip install google-generativeai
pip install python-docx
pip install sentence-transformers
pip install python-dotenv
```

## Project Structure

```bash
FinanceEduvisor/
├── main.py              # Main application entry point
├── agents.py            # Agent definitions and configurations
├── kb_handler.py        # Knowledge base management
├── tools.py             # Tool definitions for the agents
├── prompts.py           # System prompts and templates
├── kb_path/            # Knowledge base for financial guidance
├── kb_path1/           # Knowledge base for educational content
└── requirements.txt     # Project dependencies
```

## Usage

1. Ensure your knowledge bases are properly set up:
   - Place educational content in `kb_path1/`
   - Place financial guidance content in `kb_path/`

2. Run the application:
```bash
python main.py
```

3. Interact with the system:
   - Ask educational questions about finance
   - Seek financial guidance
   - Type 'exit' or 'quit' to end the session

## Example Queries

Educational Mode:
- "What is a P/E ratio?"
- "Explain the concept of diversification"
- "How do bonds work?"

Guidance Mode:
- "How should I start investing?"
- "What's a good portfolio for retirement?"
- "How can I manage my investment risk?"

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- LlamaIndex for the powerful indexing and querying capabilities
- Google's Gemini for the language model capabilities
- Sentence Transformers for the embedding model


