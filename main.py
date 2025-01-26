from LLMAnywhere import AnywhereLLM

assistant = AnywhereLLM(
    add_content_hotkey='alt+space',
    generate_hotkey='shift+space',
    clear_memory_hotkey='ctrl+shift'
)
assistant.run()


