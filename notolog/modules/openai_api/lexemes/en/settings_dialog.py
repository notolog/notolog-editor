# English lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API URL",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description":
        "The OpenAI API URL is the address to the API endpoint, which may vary depending on the service and version.\n"
        "The AI Assistant uses the one for conversational chat functionality or text completions.\n"
        "Refer to the official OpenAI API documentation to obtain the current URL.",
    "module_openai_api_key_label": "API Key",
    "module_openai_api_key_input_placeholder_text": "API Key",
    "module_openai_api_key_input_accessible_description":
        "The OpenAI API Key is a secret token used for authenticating requests to the API endpoint.",
    "module_openai_api_supported_models_label": "Supported Models",
    "module_openai_api_model_names_combo_placeholder_text": "Choose a Model",
    "module_openai_api_model_names_combo_accessible_description":
        "Select from supported models for chat conversations.",

    "module_openai_api_base_system_prompt_label": "System Prompt",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Base system prompt that precedes each request",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "A base system prompt that precedes each request.\n"
        "Usually, it is plain text with instructions or role characteristics.",

    "module_openai_api_base_response_temperature_label": "Temperature: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Adjusts the randomness of the model's responses. Higher values produce more varied outputs, "
        "while lower values make responses more predictable.",

    "module_openai_api_base_response_max_tokens_label": "Maximum Response Tokens",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Maximum number of tokens to receive in response, such as words and punctuation, "
        "controlling the length of the output.",

    "module_openai_api_config_prompt_history_size_label": "Prompt History Size",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Controls the number of entries in the prompt history that the system retains for reference.\n"
        "A zero value allows for unlimited entries."
}
