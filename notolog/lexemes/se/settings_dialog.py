# Swedish lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Inställningar",

    "button_close": "Stäng",

    "tab_general": "Allmänt",
    "tab_editor_config": "Redigerare",
    "tab_viewer_config": "Visare",
    "tab_ai_config": "AI-konfiguration",

    "general_app_config_label": "Appkonfiguration",
    "general_app_language_label": "Språk",
    "general_app_language_combo_placeholder_text": "Välj ett språk",
    "general_app_language_combo_accessible_description": "Appens gränssnittsspråk",
    "general_app_theme_label": "Tema",
    "general_app_theme_combo_placeholder_text": "Välj ett tema",
    "general_app_theme_combo_accessible_description": "Appens gränssnittstema",
    "general_app_default_path_label": "Standardmapp för anteckningar",
    "general_app_default_path_input_accessible_description": "Ange standardmappen där anteckningar ska sparas",
    "general_app_default_path_input_placeholder_text": "Välj eller ange en mappsökväg",
    "general_app_elements_visibility_label": "Hantera elementens synlighet",
    "general_app_main_menu_label": "Huvudmeny",
    "general_app_main_menu_checkbox": "Visa huvudmeny",
    "general_app_main_menu_checkbox_accessible_description": "Visa appens huvuddropdownmeny",
    "general_app_font_size_label": "Teckenstorlek: {size}pt",
    "general_app_font_size_slider_accessible_description": "Justera appens globala teckenstorlek",

    "general_statusbar_label": "Statusfält",
    "general_statusbar_show_global_cursor_position_checkbox": "Visa global muspekareposition",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Visa den globala muspekarepositionen i statusfältet",

    "editor_config_label": "Redigerarkonfiguration",
    "editor_config_show_line_numbers_checkbox": "Visa radnummer",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Visa radnummer i redigeraren",

    "viewer_config_label": "Visarkonfiguration",
    "viewer_config_process_emojis_checkbox": "Konvertera textemojis till grafik",
    "viewer_config_process_emojis_checkbox_accessible_description": "Konvertera textemojis till grafiska representationer",
    "viewer_config_highlight_todos_checkbox": "Markera TODOs",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Markera TODO-taggar i texten",
    "viewer_config_open_link_confirmation_checkbox": "Kräv bekräftelse för att öppna länkar",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Begär bekräftelse innan länkar öppnas",
    "viewer_config_save_resources_checkbox": "Spara automatiskt externa bilder på disk",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Sparar automatiskt kopior av externa bilder på disken för offline-åtkomst",

    "ai_config_inference_module_label": "Inferensmodul",
    "ai_config_inference_module_names_combo_label": "Aktiv inferensmodul",
    "ai_config_inference_module_names_combo_placeholder_text": "Välj modul",
    "ai_config_inference_module_names_combo_accessible_description":
        "Välj bland tillgängliga AI-inferensmoduler för att arbeta med AI-assistenten.\n"
        "Alternativen inkluderar stora språkmodeller (LLM) med realtidsbearbetning eller API-baserade funktioner.",

    "ai_config_base_label": "Grundparametrar",
    "ai_config_multi_turn_dialogue_checkbox": "Fleromgångsdialog med samtalsminne",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Aktivera en fleromgångsdialog som bevarar den senaste inmatningen för samtalsminne.\n"
        "När den är avstängd påverkar endast det nya meddelandet och systemuppmaningen svaret.",
    "ai_config_convert_to_md_checkbox": "Konvertera resultatet till Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Konvertera utgångsmeddelandet till Markdown-format.",
}
