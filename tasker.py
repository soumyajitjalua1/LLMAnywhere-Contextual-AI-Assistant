import openai
import keyboard
import threading
import time
import os  # For opening applications
from openai import AzureOpenAI
# from secrets import api_key, azure_endpoint
api_key='c442268217b54c6cafb83b2c3114f094'
azure_endpoint="https://catg-openai.openai.azure.com/"
from pydantic import BaseModel, Field
from typing import List
import pyperclip


# Define the structure of keys and text
class KeysAndText(BaseModel):
    keys: List[str] = Field(description="Keys to be pressed sequentially.")
    text: str = Field(description="Text to be typed after pressing the keys.")

# Define the structure for a sequence of steps
class Steps(BaseModel):
    steps: List[KeysAndText] = Field(description="List of steps to execute the task.")

# Azure OpenAI Client
client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,  
            api_version="2024-08-01-preview"
        )

def get_response(prompt):
    completion =client.beta.chat.completions.parse(
                model="gpt4ostructuredoutput",
                messages=[{"role": "user", "content": prompt}],
                response_format=Steps
            )
    return completion
class TaskExecutor:
    def __init__(self):
        # API Configuration
        
        self.model_name = "gpt4ostructuredoutput"

    def _generate_task_steps(self, task_description):
        """Use LLM to generate structured steps for a given task."""
        prompt = f"""
            Generate a sequence of steps to perform the following task on a Windows 11 machine using keyboard inputs and text typing. 
            Each step should specify the keys to press and optional text to type. 
            Return the response as a JSON object matching this structure

            Here are some examples of tasks and the corresponding sequences of steps:

            Example 1:
            Task: Open Google Chrome and search for "OpenAI GPT"
            Response:
            {{
                "steps": [
                    {{"keys": ["win+s"], "text": "chrome"}}, 
                    {{"keys": ["enter"], "text": ""}},
                    {{"keys": [], "text": "OpenAI GPT"}}, 
                    {{"keys": ["enter"], "text": ""}}
                ]
            }}

            Example 2:
            Task: Open Command Prompt and navigate to 'C:\\Users'
            Response:
            {{
                "steps": [
                    {{"keys": ["win+s"], "text": "cmd"}}, 
                    {{"keys": ["enter"], "text": ""}}, 
                    {{"keys": ["alt", "space"], "text": ""}},
                    {{"keys": ["x"], "text": ""}},
                    {{"keys": ["cd"], "text": "C:\\Users"}}, 
                    {{"keys": ["enter"], "text": ""}}
                ]
            }}

            Example 3:
            Task: Open Microsoft Word and type "Hello, this is a test."
            Response:
            {{
                "steps": [
                    {{"keys": ["win+s"], "text": "word"}}, 
                    {{"keys": ["enter"], "text": ""}}, 
                    {{"keys": [], "text": "Hello, this is a test."}}
                ]
            }}
            use the + symbol to represent key combinations, e.g., "ctrl+alt+t"

            think step by step and generate steps for the following task:
            Task: {task_description}
        """

        try:
            completion=get_response(prompt)
            parsed_steps = completion.choices[0].message.parsed
            print(parsed_steps)
            return parsed_steps.steps
        except Exception as e:
            return f"Error generating task instructions: {str(e)}"

    def execute_task(self, task_description):
        """Execute a sequence of steps for the given task."""
        steps = self._generate_task_steps(task_description)
        if isinstance(steps, str):  # Error case
            print(steps)
            return

        print(f"Executing task: {task_description}")
        for step in steps:
            # Press the keys sequentially
            for key in step.keys:
                keyboard.press_and_release(key)
                time.sleep(2)  # Delay for system to process the keypress
            
            # Type the text if available
            if step.text:
                time.sleep(3)  # Slight delay before typing
                keyboard.write(step.text)
                time.sleep(2)

        print("Task completed.")

    def run(self):
        """Hotkey for executing tasks."""
        # Hotkey to execute tasks
        keyboard.add_hotkey('ctrl+alt+t', lambda: self.execute_task(pyperclip.paste()))

        # Keep the script running
        keyboard.wait()

def main():
    executor = TaskExecutor()
    print("Task Executor Started. Use hotkeys to interact.")
    executor.run()

if __name__ == "__main__":
    main()
