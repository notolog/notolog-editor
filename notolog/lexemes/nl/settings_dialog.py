# Dutch lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Instellingen",

    "button_close": "Sluiten",

    "tab_general": "Algemeen",
    "tab_workspace": "Werkruimte",
    "tab_ai_config": "AI Configuratie",

    "general_app_config_label": "App configuratie",
    "general_app_language_label": "Taal",
    "general_app_language_combo_placeholder_text": "Kies een taal",
    "general_app_language_combo_accessible_description": "Interface taal van de app",
    "general_app_theme_label": "Thema",
    "general_app_theme_combo_placeholder_text": "Kies een thema",
    "general_app_theme_combo_accessible_description": "Interface thema van de app",
    "general_app_default_path_label": "Standaardmap voor notities",
    "general_app_default_path_input_accessible_description": "Specificeer de standaardmap waar de notities worden opgeslagen",
    "general_app_default_path_input_placeholder_text": "Selecteer of voer een mappad in",
    "general_app_elements_visibility_label": "Beheer zichtbaarheid van elementen",
    "general_app_main_menu_label": "Hoofdmenu",
    "general_app_main_menu_checkbox": "Toon hoofdmenu",
    "general_app_main_menu_checkbox_accessible_description": "Toon het hoofddropdownmenu van de app",
    "general_app_font_size_label": "Lettergrootte: {size}pt",
    "general_app_font_size_slider_accessible_description": "Pas de globale lettergrootte van de app aan",

    "general_file_deletion_label": "Bestanden verwijderen",
    "general_reversible_file_deletion_checkbox": "Bestanden omkeerbaar verwijderen",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Verplaats verwijderde bestanden naar de Notolog-prullenbak door een .del-extensie toe te voegen",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Toon globale cursorpositie",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Toon de globale cursorpositie in de statusbalk",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Navigatiepijlen weergeven",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Navigatiepijlen weergeven in de statusbalk",

    "workspace_editor_mode_label": "Editormodus",
    "workspace_editor_mode_show_line_numbers_checkbox": "Toon regelnummers",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Toon regelnummers in de editor",

    "workspace_view_mode_label": "Weergavemodus",
    "workspace_view_mode_process_emojis_checkbox": "Zet tekstemoji's om naar grafische afbeeldingen",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "Zet tekstemoji's om naar grafische afbeeldingen",
    "workspace_view_mode_highlight_todos_checkbox": "Markeer TODO's",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Benadruk TODO-tags binnen de tekst",
    "workspace_view_mode_open_link_confirmation_checkbox": "Bevestiging vereist om links te openen",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Vraag om bevestiging voordat links worden geopend",
    "workspace_view_mode_save_resources_checkbox": "Auto-save externe afbeeldingen naar schijf",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Onderste balk",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "CPU- en geheugengrafieken tonen",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "CPU- en geheugengebruik met scheidingslijn in de onderste balk tonen",
    "workspace_bottom_bar_system_load_interval_ms_label": "Vernieuwingsinterval grafieken",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Instellen hoe vaak CPU- en geheugengebruik wordt gelezen, in milliseconden",
}
