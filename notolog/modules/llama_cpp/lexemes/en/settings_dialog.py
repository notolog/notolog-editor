# English lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Module llama.cpp",

    "module_llama_cpp_config_label": "Module llama.cpp",
    "module_llama_cpp_config_path_label": "Model Location",
    "module_llama_cpp_config_path_input_placeholder_text": "Select or enter the model path",
    "module_llama_cpp_config_path_input_accessible_description":
        "An input field with a selector to specify the local model's path. Supports models in GGUF format,\n"
        "a binary file format optimized for storing models used with GGML and GGML-based executors.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF Files",

    "module_llama_cpp_config_context_window_label": "Context Window Size",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Sets the number of tokens the model considers for generating responses. "
        "Controls how much prior context is used.",

    "module_llama_cpp_chat_formats_label": "Chat Formats",
    "module_llama_cpp_chat_formats_combo_placeholder_text": "Select a chat format",
    "module_llama_cpp_chat_formats_combo_accessible_description":
        "Dropdown menu to select the format used for model conversations.",

    "module_llama_cpp_config_system_prompt_label": "System Prompt",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Enter system prompt text",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Text field for entering system prompts that guide model responses.",

    "module_llama_cpp_config_response_temperature_label": "Response Temperature: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Adjusts the randomness of the model's responses. Higher values produce more varied outputs,\n"
        "while lower values result in more predictable responses.",

    "module_llama_cpp_config_response_max_tokens_label": "Max Tokens per Response",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Limits the number of tokens in the model's responses up to the actual context window limit.\n"
        "A zero value assumes the capacity of the context window.",

    "module_llama_cpp_config_prompt_history_size_label": "Size of the Prompt History",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Controls the number of entries in the prompt history retained by the system for reference.\n"
        "A zero value allows for unlimited entries."
}
