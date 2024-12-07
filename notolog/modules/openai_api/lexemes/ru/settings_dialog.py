# Russian lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "API OpenAI",

    "module_openai_api_label": "API OpenAI",
    "module_openai_api_url_label": "URL API",
    "module_openai_api_url_input_placeholder_text": "URL API",
    "module_openai_api_url_input_accessible_description":
        "URL API OpenAI — это адрес конечной точки API, который может изменяться в зависимости от сервиса и версии.\n"
        "AI Assistant использует ту, что предназначена для функций чатов или завершения текста.\n"
        "Обратитесь к официальной документации OpenAI API, чтобы получить текущий URL.",
    "module_openai_api_key_label": "Ключ API",
    "module_openai_api_key_input_placeholder_text": "Ключ API",
    "module_openai_api_key_input_accessible_description":
        "Ключ API OpenAI — это секретный токен, используемый для аутентификации запросов к конечной точке API.",
    "module_openai_api_supported_models_label": "Поддерживаемые модели",
    "module_openai_api_model_names_combo_placeholder_text": "Выбрать модель",
    "module_openai_api_model_names_combo_accessible_description":
        "Выберите из поддерживаемых моделей для чат-бесед.",

    "module_openai_api_base_system_prompt_label": "Системный промпт",
    "module_openai_api_base_system_prompt_edit_placeholder_text":
        "Базовый системный промпт, предшествующий каждому запросу",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Базовый системный промпт, который предшествует каждому запросу.\n"
        "Обычно это простой текст с инструкциями или характеристиками роли.",

    "module_openai_api_base_response_temperature_label": "Температура: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Регулирует случайность ответов модели. Высокие значения создают более разнообразные результаты, "
        "в то время как низкие значения делают ответы более предсказуемыми.",

    "module_openai_api_base_response_max_tokens_label": "Максимальное количество токенов на ответ",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Максимальное количество токенов, которые можно получить в ответ, таких как слова и пунктуация, "
        "контролируя длину вывода.",

    "module_openai_api_config_prompt_history_size_label": "Размер истории промптов",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Контролирует количество записей в истории промптов, которые система сохраняет для справки.\n"
        "Значение ноль позволяет неограниченное количество записей."
}
