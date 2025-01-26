import openai
import keyboard
import pyperclip
import threading
import time
from openai import AzureOpenAI
from tasker import api_key, azure_endpoint
from typing import List


client = AzureOpenAI(
            api_key=api_key,  
            azure_endpoint=azure_endpoint,
            api_version="2024-02-15-preview" 
        )

class AnywhereLLM:
    '''
    AnywhereLLM: A context-aware AI assistant that can be used system-wide with advanced features:
    
    Hotkeys:
    - Alt+Space: Add content to chat history
    - Shift+Space: Generate content using chat history context
    - Ctrl+Shift: Clear chat history
    - Esc: Stop ongoing text generation
    
    Features:
    - Long-term memory management
    - Context-aware content generation
    - Multiple generation modes
    - Customizable API integration
    - Writing interruption support
    '''

    def __init__(self, 
                 add_content_hotkey='alt+space',
                 generate_hotkey='shift+space',
                 clear_memory_hotkey='ctrl+shift',
                 stop_writing_hotkey='esc'):
        # API Configuration
        openai.api_key = api_key
        openai.base_url = azure_endpoint
        
        # Azure OpenAI Client
        
        self.model_name = "gpt4ostructuredoutput"
        
        # Memory and State Management
        self.typed_strings = []
        self.long_term_memory = []
        self.generation_modes = {
            'default': self._default_generation,
            'creative': self._creative_generation,
            'analytical': self._analytical_generation,
            'summarize': self._summarization_generation,
            'code': self._code_generation
        }
        self.current_mode = 'default'
        
        # Hotkey Configuration
        self.add_content_hotkey = add_content_hotkey
        self.generate_hotkey = generate_hotkey
        self.clear_memory_hotkey = clear_memory_hotkey
        self.stop_writing_hotkey = stop_writing_hotkey
        
        # Writing Control
        self.is_writing = False
        self.stop_writing = False

    def _get_context_prompt(self):
        """Generate a comprehensive context prompt."""
        chat_prompt = "Context for AI assistance:\n"
        
        # Long-term memory context
        if self.long_term_memory:
            chat_prompt += "Previous conversation summary:\n"
            for memory in self.long_term_memory:
                chat_prompt += f"- {memory}\n"
        
        # Current task context
        if self.typed_strings:
            task = self.typed_strings[-1]
            chat_prompt += f"\nCurrent Task: {task}\n"
            
            # Additional context from previous inputs
            if len(self.typed_strings) > 1:
                chat_prompt += "Additional Context:\n"
                for text in self.typed_strings[:-1]:
                    chat_prompt += f"- {text}\n"
        
        return chat_prompt

    def _default_generation(self, prompt):
        """Default content generation method."""
        return self._generate_content(prompt)

    def _creative_generation(self, prompt):
        """Creative content generation with more diverse output."""
        creative_prompt = f"Provide a highly creative and innovative response to the following:\n{prompt}\n\n" \
                          f"Approach this with maximum creativity, thinking outside the box."
        return self._generate_content(creative_prompt)

    def _analytical_generation(self, prompt):
        """Analytical content generation with structured approach."""
        analytical_prompt = f"Provide a comprehensive, structured analytical response to:\n{prompt}\n\n" \
                            f"Break down the task systematically. Use clear reasoning and provide detailed insights."
        return self._generate_content(analytical_prompt)

    def _summarization_generation(self, prompt):
        """Summarization generation method."""
        summary_prompt = f"Summarize the following content concisely and accurately:\n{prompt}\n\n" \
                         f"Focus on key points, main ideas, and essential information."
        return self._generate_content(summary_prompt)

    def _generate_content(self, prompt):
        """Core content generation method."""
        try:
            completion = client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error in generation: {str(e)}"

    def generate(self):
        """Generate content with writing control."""
        if not self.typed_strings:
            keyboard.write("No task to process")
            return

        # Reset writing control flags
        self.stop_writing = False
        self.is_writing = True

        # Prepare context
        context_prompt = self._get_context_prompt()
        
        # Generate content using current mode
        generation_method = self.generation_modes.get(self.current_mode, self._default_generation)
        result = generation_method(context_prompt)


        # Threaded writing with interruption support
        def write_content():
            try:
                for char in result:
                    if self.stop_writing:
                        break
                    keyboard.write(char, delay=0.001)
                    time.sleep(0.01)  # Slight delay to make writing visible
            finally:
                self.is_writing = False

        writing_thread = threading.Thread(target=write_content)
        writing_thread.start()

        # Summarize and update memory
        # self.summarize(result)
        self.typed_strings.clear()

    def _code_generation(self, prompt):
        """Specialized code generation method with advanced prompting."""
        code_generation_prompt = f"""
        You are an expert code generation assistant. Generate high-quality, production-ready code based on the following context and requirements:

        Context and Task:
        {prompt}

        Code Generation Guidelines:
        1. Write clean, readable, and well-documented code
        2. Follow best practices for the target programming language
        3. Include type hints and docstrings
        4. Handle potential edge cases
        5. Optimize for readability and maintainability
        6. Use modern language features
        7. Include brief comments explaining complex logic

        Generate the code with these principles in mind:
        """
        
        # Use the existing generation method with the specialized prompt
        return self._generate_content(code_generation_prompt)

    def summarize(self, text, max_words=50):
        """Summarize text for long-term memory."""
        summary_prompt = f"Summarize the following text in maximum {max_words} words for long-term memory:\n{text}"
        
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": summary_prompt},
                ],
            )
            summary = completion.choices[0].message.content
            self.long_term_memory.append(summary)
            print(f"Summarized text: {summary}")
        except Exception as e:
            print(f"Summarization error: {e}")

    def change_generation_mode(self, mode):
        """Change the current generation mode."""
        if mode in self.generation_modes:
            self.current_mode = mode
            print(f"Generation mode changed to: {mode}")
        else:
            print(f"Invalid mode. Available modes: {list(self.generation_modes.keys())}")

    def run(self):
        """Set up hotkeys and start the application."""
        # Content addition hotkey
        keyboard.add_hotkey(self.add_content_hotkey, 
                            lambda: self.typed_strings.append(pyperclip.paste()))
        
        
        # Content generation hotkey
        keyboard.add_hotkey(self.generate_hotkey, self.generate)
        
        # Memory clearing hotkey
        keyboard.add_hotkey(self.clear_memory_hotkey, 
                            lambda: self.long_term_memory.clear())
        
        # Stop writing hotkey
        keyboard.add_hotkey(self.stop_writing_hotkey, 
                            lambda: setattr(self, 'stop_writing', True) 
                            if self.is_writing else None)
        
        # Mode change hotkeys
        keyboard.add_hotkey('ctrl+1', lambda: self.change_generation_mode('default'))
        keyboard.add_hotkey('ctrl+2', lambda: self.change_generation_mode('creative'))
        keyboard.add_hotkey('ctrl+3', lambda: self.change_generation_mode('analytical'))
        keyboard.add_hotkey('ctrl+4', lambda: self.change_generation_mode('summarize'))
        keyboard.add_hotkey('ctrl+5', lambda: self.change_generation_mode('code'))

        # Keep the script running
        keyboard.wait()

def main():
    assistant = AnywhereLLM()
    print("AnywhereLLM Started. Use hotkeys to interact.")
    assistant.run()

if __name__ == "__main__":
    main()