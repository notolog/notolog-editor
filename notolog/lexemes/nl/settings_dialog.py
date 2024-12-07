# Dutch lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Instellingen",

    "button_close": "Sluiten",

    "tab_general": "Algemeen",
    "tab_editor_config": "Editor",
    "tab_viewer_config": "Viewer",
    "tab_ai_config": "AI Configuratie",

    "general_app_config_label": "App configuratie",
    "general_app_language_label": "Taal",
    "general_app_language_combo_placeholder_text": "Kies een taal",
    "general_app_language_combo_accessible_description": "Interface taal van de app",
    "general_app_theme_label": "Thema",
    "general_app_theme_combo_placeholder_text": "Kies een thema",
    "general_app_theme_combo_accessible_description": "Interface thema van de app",
    "general_app_main_menu_label": "Hoofdmenu",
    "general_app_main_menu_checkbox": "Toon hoofdmenu",
    "general_app_main_menu_checkbox_accessible_description": "Toon het hoofddropdownmenu van de app",
    "general_app_font_size_label": "Lettergrootte: {size}pt",
    "general_app_font_size_slider_accessible_description": "Pas de globale lettergrootte van de app aan",

    "general_statusbar_label": "Statusbalk",
    "general_statusbar_show_global_cursor_position_checkbox": "Toon globale cursorpositie",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Toon de globale cursorpositie in de statusbalk",

    "editor_config_label": "Editor Configuratie",
    "editor_config_show_line_numbers_checkbox": "Toon regelnummers",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Toon regelnummers in de editor",

    "viewer_config_label": "Viewer Configuratie",
    "viewer_config_process_emojis_checkbox": "Zet tekstemoji's om naar grafische afbeeldingen",
    "viewer_config_process_emojis_checkbox_accessible_description": "Zet tekstemoji's om naar grafische afbeeldingen",
    "viewer_config_highlight_todos_checkbox": "Markeer TODO's",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Benadruk TODO-tags binnen de tekst",
    "viewer_config_open_link_confirmation_checkbox": "Bevestiging vereist om links te openen",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Vraag om bevestiging voordat links worden geopend",
    "viewer_config_save_resources_checkbox": "Auto-save externe afbeeldingen naar schijf",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Sla automatisch kopieën van externe afbeeldingen op schijf op voor offline toegang.",

    "ai_config_inference_module_label": "Inferentiemodule",
    "ai_config_inference_module_names_combo_label": "Actieve Inferentiemodule",
    "ai_config_inference_module_names_combo_placeholder_text": "Kies een module",
    "ai_config_inference_module_names_combo_accessible_description":
        "Selecteer uit beschikbare AI-inferentiemodules om te werken met de AI-assistent.\n"
        "Opties omvatten grote taalmodellen (LLM) met realtime verwerking of API-gebaseerde functionaliteiten.",

    "ai_config_base_label": "Basisparameters",
    "ai_config_multi_turn_dialogue_checkbox": "Meerdere gespreksbeurten met geheugen",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Schakel een dialoog in met meerdere gespreksbeurten die de vorige prompt bewaart voor gespreksgeheugen.\n"
        "Als het is uitgeschakeld, beïnvloeden alleen het nieuwe bericht en de systeemprompt de reactie.",
    "ai_config_convert_to_md_checkbox": "Converteer het resultaat naar Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Converteer het uitvoerbericht naar Markdown-indeling.",
}
