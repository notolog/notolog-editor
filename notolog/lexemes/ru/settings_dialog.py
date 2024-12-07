# Russian lexemes settings_dialog.py
lexemes = {
    # Настройки
    "window_title": "Настройки",

    "button_close": "Закрыть",

    "tab_general": "Общие",
    "tab_editor_config": "Редактор",
    "tab_viewer_config": "Просмотрщик",
    "tab_ai_config": "Настройки ИИ",

    "general_app_config_label": "Настройки приложения",
    "general_app_language_label": "Язык",
    "general_app_language_combo_placeholder_text": "Выбрать язык",
    "general_app_language_combo_accessible_description": "Язык интерфейса приложения",
    "general_app_theme_label": "Тема",
    "general_app_theme_combo_placeholder_text": "Выбрать тему",
    "general_app_theme_combo_accessible_description": "Тема интерфейса приложения",
    "general_app_main_menu_label": "Главное меню",
    "general_app_main_menu_checkbox": "Показать главное меню",
    "general_app_main_menu_checkbox_accessible_description": "Показать основное выпадающее меню приложения",
    "general_app_font_size_label": "Размер шрифта: {size}pt",
    "general_app_font_size_slider_accessible_description": "Настроить глобальный размер шрифта приложения",

    "general_statusbar_label": "Строка состояния",
    "general_statusbar_show_global_cursor_position_checkbox": "Показать глобальное положение курсора",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Отображать глобальное положение курсора в строке состояния",

    "editor_config_label": "Настройки редактора",
    "editor_config_show_line_numbers_checkbox": "Показать номера строк",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Отображать номера строк в редакторе",

    "viewer_config_label": "Настройки просмотрщика",
    "viewer_config_process_emojis_checkbox": "Преобразовать текстовые эмодзи в графику",
    "viewer_config_process_emojis_checkbox_accessible_description":
        "Преобразовать текстовые эмодзи в графические изображения",
    "viewer_config_highlight_todos_checkbox": "Выделить задачи TODO",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Выделять задачи TODO в тексте",
    "viewer_config_open_link_confirmation_checkbox": "Требовать подтверждение перед открытием ссылок",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Запрашивать подтверждение перед открытием ссылок",
    "viewer_config_save_resources_checkbox": "Автосохранение внешних изображений на диск",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Автоматически сохраняет копии внешних изображений на диск для доступа без подключения к интернету.",

    "ai_config_inference_module_label": "Модуль вывода",
    "ai_config_inference_module_names_combo_label": "Активный модуль вывода",
    "ai_config_inference_module_names_combo_placeholder_text": "Выбрать модуль",
    "ai_config_inference_module_names_combo_accessible_description":
        "Выберите из доступных модулей ИИ-инференции для работы с AI Assistant. Варианты включают локальные\n"
        "большие языковые модели (LLM) с обработкой в реальном времени или функциональность на базе API.",

    "ai_config_base_label": "Базовые параметры",
    "ai_config_multi_turn_dialogue_checkbox": "Многошаговый чат-диалог с памятью",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Включите многошаговый чат-диалог, который сохраняет последний запрос для памяти.\n"
        "Когда выключено, только новое сообщение и системный промпт влияют на ответ.",
    "ai_config_convert_to_md_checkbox": "Конвертировать результат в Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Преобразуйте выходное сообщение в формат Markdown.",
}
