# Spanish lexemes settings_dialog.py
lexemes = {
    # Configuración
    "window_title": "Configuración",

    "button_close": "Cerrar",

    "tab_general": "General",
    "tab_editor_config": "Editor",
    "tab_viewer_config": "Visor",
    "tab_ai_config": "Configuración IA",

    "general_app_config_label": "Configuración de la app",
    "general_app_language_label": "Idioma",
    "general_app_language_combo_placeholder_text": "Elegir un idioma",
    "general_app_language_combo_accessible_description": "Idioma de la interfaz de la app",
    "general_app_theme_label": "Tema",
    "general_app_theme_combo_placeholder_text": "Elegir un tema",
    "general_app_theme_combo_accessible_description": "Tema de la interfaz de la app",
    "general_app_default_path_label": "Carpeta predeterminada para notas",
    "general_app_default_path_input_accessible_description": "Especifique la carpeta predeterminada donde se "
                                                             "almacenarán las notas",
    "general_app_default_path_input_placeholder_text": "Seleccione o ingrese una ruta de carpeta",
    "general_app_elements_visibility_label": "Administrar la visibilidad de los elementos",
    "general_app_main_menu_label": "Menú Principal",
    "general_app_main_menu_checkbox": "Mostrar menú principal",
    "general_app_main_menu_checkbox_accessible_description": "Mostrar el menú desplegable principal de la aplicación",
    "general_app_font_size_label": "Tamaño de fuente: {size}pt",
    "general_app_font_size_slider_accessible_description": "Ajustar el tamaño de fuente global de la aplicación",

    "general_statusbar_label": "Barra de estado",
    "general_statusbar_show_global_cursor_position_checkbox": "Mostrar la posición global del cursor",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Mostrar la posición global del cursor en la barra de estado",

    "editor_config_label": "Configuración del editor",
    "editor_config_show_line_numbers_checkbox": "Mostrar números de línea",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Mostrar números de línea en el editor",

    "viewer_config_label": "Configuración del visor",
    "viewer_config_process_emojis_checkbox": "Convertir emojis de texto en gráficos",
    "viewer_config_process_emojis_checkbox_accessible_description":
        "Convertir emojis de texto en representaciones gráficas",
    "viewer_config_highlight_todos_checkbox": "Resaltar TODOs",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Resaltar etiquetas TODO en el texto",
    "viewer_config_open_link_confirmation_checkbox": "Requerir confirmación para abrir enlaces",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Solicitar confirmación antes de abrir enlaces",
    "viewer_config_save_resources_checkbox": "Guardar automáticamente imágenes externas en el disco",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Guarda automáticamente copias de imágenes externas en el disco para acceso sin conexión.",

    "ai_config_inference_module_label": "Módulo de inferencia",
    "ai_config_inference_module_names_combo_label": "Módulo de inferencia activo",
    "ai_config_inference_module_names_combo_placeholder_text": "Elegir módulo",
    "ai_config_inference_module_names_combo_accessible_description":
        "Seleccione de los módulos de inferencia de IA disponibles para operar con el Asistente de IA.\n"
        "Las opciones incluyen modelos de lenguaje de gran tamaño (LLM) con procesamiento en tiempo real,\n"
        "o funcionalidades basadas en API.",

    "ai_config_base_label": "Parámetros básicos",
    "ai_config_multi_turn_dialogue_checkbox": "Diálogo de múltiples turnos con memoria conversacional",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Habilite un diálogo de múltiples turnos que conserve la última indicación para memoria conversacional.\n"
        "Cuando está desactivado, solo el nuevo mensaje y la indicación del sistema influyen en la respuesta.",
    "ai_config_convert_to_md_checkbox": "Convertir el resultado a Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Convierta el mensaje de salida al formato Markdown.",
}
