# English lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Settings",

    "button_close": "Close",

    "tab_general": "General",
    "tab_workspace": "Workspace",
    "tab_ai_config": "AI Config",

    "general_app_config_label": "App config",
    "general_app_language_label": "Language",
    "general_app_language_combo_placeholder_text": "Choose a language",
    "general_app_language_combo_accessible_description": "App's interface language",
    "general_app_theme_label": "Theme",
    "general_app_theme_combo_placeholder_text": "Choose a theme",
    "general_app_theme_combo_accessible_description": "App's interface theme",
    "general_app_default_path_label": "Default folder for notes",
    "general_app_default_path_input_accessible_description": "Specify the default folder where notes will be stored",
    "general_app_default_path_input_placeholder_text": "Select or enter a folder path",
    "general_app_elements_visibility_label": "Manage elements visibility",
    "general_app_main_menu_label": "Main Menu",
    "general_app_main_menu_checkbox": "Show Main Menu",
    "general_app_main_menu_checkbox_accessible_description": "Display the app's main dropdown menu",
    "general_app_font_size_label": "Font Size: {size}pt",
    "general_app_font_size_slider_accessible_description": "Adjust the app's global font size",

    "general_file_deletion_label": "File deletion",
    "general_reversible_file_deletion_checkbox": "Delete files reversibly",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Move deleted files to the Notolog litter bin by adding a .del extension",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Show Global Cursor Position",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Display the global cursor position in the status bar",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Show Navigation Arrows",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Show navigation arrows in the status bar.",

    "workspace_editor_mode_label": "Editor mode",
    "workspace_editor_mode_show_line_numbers_checkbox": "Show Line Numbers",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Display line numbers in the editor",

    "workspace_view_mode_label": "View mode",
    "workspace_view_mode_process_emojis_checkbox": "Convert Text Emojis to Graphics",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "Convert text emojis to graphical representations",
    "workspace_view_mode_highlight_todos_checkbox": "Highlight TODOs",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Emphasize TODO tags within the text",
    "workspace_view_mode_open_link_confirmation_checkbox": "Require Confirmation to Open Links",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Ask for confirmation before opening links",
    "workspace_view_mode_save_resources_checkbox": "Auto-save external images to disk",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Bottom bar",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Show CPU and memory graphs",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Display CPU and memory usage graphs and their separator in the bottom bar",
    "workspace_bottom_bar_system_load_interval_ms_label": "Graph refresh interval",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Set how often CPU and memory usage is read, in milliseconds",
}
