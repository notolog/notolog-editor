# Swedish lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Inställningar",

    "button_close": "Stäng",

    "tab_general": "Allmänt",
    "tab_workspace": "Arbetsyta",
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

    "general_file_deletion_label": "Filborttagning",
    "general_reversible_file_deletion_checkbox": "Ta bort filer återställningsbart",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Flytta borttagna filer till Notologs papperskorg genom att lägga till filändelsen .del",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Visa global muspekareposition",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Visa den globala muspekarepositionen i statusfältet",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Visa navigeringspilar",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description": "Visa navigeringspilar i statusfältet",

    "workspace_editor_mode_label": "Redigeringsläge",
    "workspace_editor_mode_show_line_numbers_checkbox": "Visa radnummer",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Visa radnummer i redigeraren",

    "workspace_view_mode_label": "Visningsläge",
    "workspace_view_mode_process_emojis_checkbox": "Konvertera textemojis till grafik",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "Konvertera textemojis till grafiska representationer",
    "workspace_view_mode_highlight_todos_checkbox": "Markera TODOs",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Markera TODO-taggar i texten",
    "workspace_view_mode_open_link_confirmation_checkbox": "Kräv bekräftelse för att öppna länkar",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Begär bekräftelse innan länkar öppnas",
    "workspace_view_mode_save_resources_checkbox": "Spara automatiskt externa bilder på disk",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Nedre fält",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Visa CPU- och minnesdiagram",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Visa CPU- och minnesanvändning samt avgränsaren i det nedre fältet",
    "workspace_bottom_bar_system_load_interval_ms_label": "Uppdateringsintervall för grafer",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Ange hur ofta CPU- och minnesanvändning läses, i millisekunder",
}
