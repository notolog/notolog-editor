# Russian lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM на устройстве",

    "module_ondevice_llm_config_label": "Модель LLM на устройстве",
    "module_ondevice_llm_config_path_label": "Расположение модели ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Путь к директории модели",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Поле ввода с селектором для указания пути к директории модели, где находятся файлы ONNX.\n"
        "Поддерживаемые модели находятся в формате ONNX, что означает Open Neural Network Exchange, открытый стандарт\n"
        "формата для моделей машинного обучения.",

    "module_ondevice_llm_config_response_temperature_label": "Температура: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Регулирует случайность ответов модели. Высокие значения создают более разнообразные результаты,\n"
        "в то время как низкие значения делают ответы более предсказуемыми.",

    "module_ondevice_llm_config_response_max_tokens_label": "Максимальное количество токенов на ответ",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Устанавливает максимальное количество токенов, которые можно получить в ответе, включая слова и пунктуацию,\n"
        "контролируя длину вывода.",

    "module_ondevice_llm_config_prompt_history_size_label": "Размер истории команд",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Контролирует количество записей в истории команд, которые система сохраняет для справки.\n"
        "Значение ноль позволяет неограниченное количество записей."
}
