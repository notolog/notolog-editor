# Russian lexemes settings_dialog.py
lexemes = {
    # Настройки
    "window_title": "Настройки",

    "button_close": "Закрыть",

    "tab_general": "Общие",
    "tab_workspace": "Рабочая область",
    "tab_ai_config": "Настройки ИИ",

    "general_app_config_label": "Настройки приложения",
    "general_app_language_label": "Язык",
    "general_app_language_combo_placeholder_text": "Выбрать язык",
    "general_app_language_combo_accessible_description": "Язык интерфейса приложения",
    "general_app_theme_label": "Тема",
    "general_app_theme_combo_placeholder_text": "Выбрать тему",
    "general_app_theme_combo_accessible_description": "Тема интерфейса приложения",
    "general_app_default_path_label": "Папка по умолчанию для заметок",
    "general_app_default_path_input_accessible_description": "Укажите папку по умолчанию, в которой будут храниться заметки",
    "general_app_default_path_input_placeholder_text": "Выберите или введите путь к папке",
    "general_app_elements_visibility_label": "Управление видимостью элементов",
    "general_app_main_menu_label": "Главное меню",
    "general_app_main_menu_checkbox": "Показать главное меню",
    "general_app_main_menu_checkbox_accessible_description": "Показать основное выпадающее меню приложения",
    "general_app_font_size_label": "Размер шрифта: {size}pt",
    "general_app_font_size_slider_accessible_description": "Настроить глобальный размер шрифта приложения",

    "general_file_deletion_label": "Удаление файлов",
    "general_reversible_file_deletion_checkbox": "Удалять файлы с возможностью восстановления",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Перемещать удалённые файлы в корзину Notolog, добавляя расширение .del",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Показать глобальное положение курсора",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Отображать глобальное положение курсора в строке состояния",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Показать стрелки навигации",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Отображение стрелок навигации в строке состояния",

    "workspace_editor_mode_label": "Режим редактора",
    "workspace_editor_mode_show_line_numbers_checkbox": "Показать номера строк",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Отображать номера строк в редакторе",

    "workspace_view_mode_label": "Режим просмотра",
    "workspace_view_mode_process_emojis_checkbox": "Преобразовать текстовые эмодзи в графику",
    "workspace_view_mode_process_emojis_checkbox_accessible_description":
        "Преобразовать текстовые эмодзи в графические изображения",
    "workspace_view_mode_highlight_todos_checkbox": "Выделить задачи TODO",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Выделять задачи TODO в тексте",
    "workspace_view_mode_open_link_confirmation_checkbox": "Требовать подтверждение перед открытием ссылок",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Запрашивать подтверждение перед открытием ссылок",
    "workspace_view_mode_save_resources_checkbox": "Автосохранение внешних изображений на диск",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Нижняя панель",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Показывать графики ЦП и памяти",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Показывать графики загрузки ЦП и памяти с разделителем на нижней панели",
    "workspace_bottom_bar_system_load_interval_ms_label": "Интервал обновления графиков",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Задать интервал чтения загрузки ЦП и памяти в миллисекундах",
}
