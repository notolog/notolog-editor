# Russian lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "API OpenAI",
    "module_openai_api_url_input_placeholder_text": "URL API",
    "module_openai_api_url_input_accessible_description": "URL API OpenAI",
    "module_openai_api_key_input_placeholder_text": "Ключ API",
    "module_openai_api_key_input_accessible_description": "Ключ API OpenAI",
    "module_openai_api_supported_models_label": "Поддерживаемые модели",
    "module_openai_api_model_names_combo_placeholder_text": "Выберите модель",
    "module_openai_api_model_names_combo_accessible_description": "Выбор поддерживаемых моделей",

    "module_openai_api_base_system_prompt_label": "Системный запрос",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Базовый системный запрос, предшествующий каждому запросу",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Базовый системный запрос, предшествующий каждому запросу. Простой текст.",

    "module_openai_api_base_response_temperature_label": "Температура: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Регулирует случайность вывода модели. Более высокие значения увеличивают креативность; "
        "более низкие значения усиливают детерминизм.",

    "module_openai_api_base_response_max_tokens_label": "Максимальное количество токенов ответа",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Максимальное количество токенов, которые можно получить в ответе, таких как слова и пунктуация, "
        "контролирующее длину результата.",
}
