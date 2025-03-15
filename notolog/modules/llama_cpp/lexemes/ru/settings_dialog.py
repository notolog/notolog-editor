# Russian lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Модуль llama.cpp",

    "module_llama_cpp_config_label": "Модуль llama.cpp",
    "module_llama_cpp_config_path_label": "Расположение модели",
    "module_llama_cpp_config_path_input_placeholder_text": "Выберите или введите путь к модели",
    "module_llama_cpp_config_path_input_accessible_description":
        "Поле ввода с селектором для указания пути локальной модели. Поддерживает модели в формате GGUF,\n"
        "бинарный формат файла, оптимизированный для хранения моделей, используемых с GGML и основанными на GGML "
        "исполнителями.",
    "module_llama_cpp_config_path_input_filter_text": "Файлы GGUF",

    "module_llama_cpp_config_context_window_label": "Размер окна контекста",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Устанавливает количество токенов, которые модель учитывает при генерации ответов.\n"
        "Контролирует, сколько предыдущего контекста используется.",

    "module_llama_cpp_config_chat_formats_label": "Форматы чата",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Выберите формат чата",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Выпадающее меню для выбора формата, используемого для разговоров модели.",

    "module_llama_cpp_config_system_prompt_label": "Системный промпт",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Введите текст системного промпта",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Текстовое поле для ввода системного промпта, который направляет ответы модели.",

    "module_llama_cpp_config_response_temperature_label": "Температура ответа: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Регулирует случайность ответов модели. Высокие значения создают более разнообразные результаты,\n"
        "в то время как низкие значения приводят к более предсказуемым ответам.",

    "module_llama_cpp_config_response_max_tokens_label": "Максимальное количество токенов на ответ",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Ограничивает количество токенов в ответах модели до фактического предела окна контекста.\n"
        "Нулевое значение предполагает емкость окна контекста.",

    "module_llama_cpp_config_prompt_history_size_label": "Размер истории",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Контролирует количество записей в истории сохраняемых системой.\n"
        "Нулевое значение позволяет неограниченное количество записей."
}
