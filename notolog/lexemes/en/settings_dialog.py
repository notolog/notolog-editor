# English lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Settings",

    "button_close": "Close",

    "tab_general": "General",
    "tab_editor_config": "Editor",
    "tab_viewer_config": "Viewer",
    "tab_ai_config": "AI Config",

    "general_app_config_label": "App config",
    "general_app_language_label": "Language",
    "general_app_language_combo_placeholder_text": "Choose a language",
    "general_app_language_combo_accessible_description": "App's interface language",
    "general_app_theme_label": "Theme",
    "general_app_theme_combo_placeholder_text": "Choose a theme",
    "general_app_theme_combo_accessible_description": "App's interface theme",
    "general_app_main_menu_label": "Main Menu",
    "general_app_main_menu_checkbox": "Show Main Menu",
    "general_app_main_menu_checkbox_accessible_description": "Display the app's main dropdown menu",
    "general_app_font_size_label": "Font Size: {size}pt",
    "general_app_font_size_slider_accessible_description": "Adjust the app's global font size",

    "general_statusbar_label": "Status Bar",
    "general_statusbar_show_global_cursor_position_checkbox": "Show Global Cursor Position",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Display the global cursor position in the status bar",

    "editor_config_label": "Editor Configuration",
    "editor_config_show_line_numbers_checkbox": "Show Line Numbers",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Display line numbers in the editor",

    "viewer_config_label": "Viewer Configuration",
    "viewer_config_process_emojis_checkbox": "Convert Text Emojis to Graphics",
    "viewer_config_process_emojis_checkbox_accessible_description": "Convert text emojis to graphical representations",
    "viewer_config_highlight_todos_checkbox": "Highlight TODOs",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Emphasize TODO tags within the text",
    "viewer_config_open_link_confirmation_checkbox": "Require Confirmation to Open Links",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Ask for confirmation before opening links",
    "viewer_config_save_resources_checkbox": "Auto-save external images to disk",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Automatically saves copies of external images to disk for offline access.",

    "ai_config_inference_module_label": "Inference Module",
    "ai_config_inference_module_names_combo_label": "Active Inference Module",
    "ai_config_inference_module_names_combo_placeholder_text": "Choose Module",
    "ai_config_inference_module_names_combo_accessible_description":
        "Select from available AI inference modules to operate with the AI Assistant.\n"
        "Options include local Large Language Models (LLM) with real-time processing, or API-based functionalities.",

    "ai_config_base_label": "Base Parameters",
    "ai_config_multi_turn_dialogue_checkbox": "Multi-turn dialogue with conversational memory",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Enable multi-turn dialogue that retains the previous prompt for conversational memory.\n"
        "When switched off, only the new message and the system prompt influence the response.",
    "ai_config_convert_to_md_checkbox": "Convert the result to Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description": "Convert the output message into Markdown format.",
}
