# LLMAnywhere-Contextual-AI-Assistant

## Overview

AnywhereLLM is a system-wide AI assistant that allows seamless interaction with an AI model across different applications using customizable hotkeys.

## Features

- Context-aware content generation
- Multiple generation modes
- System-wide hotkey integration
- Long-term memory management

## Hotkeys

- Alt+Space: Add content to chat history
- Shift+Space: Generate content using context
- Ctrl+Shift: Clear chat history
- Esc: Stop ongoing text generation
- Ctrl+1: Default mode
- Ctrl+2: Creative mode
- Ctrl+3: Analytical mode
- Ctrl+4: Summarization mode
- Ctrl+5: Code generation mode

## Requirements

- Python 3.8+
- Azure OpenAI API access
- Required libraries:
  - openai
  - keyboard
  - pyperclip
  - threading

## Installation
```bash
Clone the repository
git clone https://github.com/soumyajitjalua1/LLMAnywhere-Contextual-AI-Assistant.git

# Install dependencies
pip install -r requirements.txt
python main.py
```

## Configuration
- Set up  OpenAI credentials in .env
- Configure API endpoint and key


## Usage
```bash
from AnywhereLLM import AnywhereLLM

assistant = AnywhereLLM()
assistant.run()
```

## Generation Modes

- Default: Standard response generation
- Creative: Innovative, out-of-box thinking
- Analytical: Structured, detailed analysis
- Summarization: Concise content summarization
- Code Generation: Programming-focused output

## Contributing

- Fork the repository
- Create feature branch
- Commit changes
- Push to branch
- Create Pull Request

License
- MIT License

