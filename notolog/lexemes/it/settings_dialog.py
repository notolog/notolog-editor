# Italian lexemes settings_dialog.py
lexemes = {
    # Impostazioni
    "window_title": "Impostazioni",

    "button_close": "Chiudi",

    "tab_general": "Generale",
    "tab_editor_config": "Editore",
    "tab_viewer_config": "Visualizzatore",
    "tab_ai_config": "Configurazione IA",

    "general_app_config_label": "Configurazione dell'app",
    "general_app_language_label": "Lingua",
    "general_app_language_combo_placeholder_text": "Scegli una lingua",
    "general_app_language_combo_accessible_description": "Lingua dell'interfaccia dell'app",
    "general_app_theme_label": "Tema",
    "general_app_theme_combo_placeholder_text": "Scegli un tema",
    "general_app_theme_combo_accessible_description": "Tema dell'interfaccia dell'app",
    "general_app_default_path_label": "Cartella predefinita per le note",
    "general_app_default_path_input_accessible_description": "Specifica la cartella predefinita in cui verranno "
                                                             "memorizzate le note",
    "general_app_default_path_input_placeholder_text": "Seleziona o inserisci un percorso di cartella",
    "general_app_elements_visibility_label": "Gestisci la visibilità degli elementi",
    "general_app_main_menu_label": "Menu Principale",
    "general_app_main_menu_checkbox": "Mostra il menu principale",
    "general_app_main_menu_checkbox_accessible_description": "Visualizza il menu a discesa principale dell'app",
    "general_app_font_size_label": "Dimensione del carattere: {size}pt",
    "general_app_font_size_slider_accessible_description": "Regola la dimensione del carattere globale dell'app",

    "general_statusbar_label": "Barra di Stato",
    "general_statusbar_show_global_cursor_position_checkbox": "Mostra la Posizione Globale del Cursore",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Visualizza la posizione globale del cursore nella barra di stato",
    "general_statusbar_show_navigation_arrows_checkbox": "Mostra frecce di navigazione",
    "general_statusbar_show_navigation_arrows_checkbox_accessible_description":
        "Mostra le frecce di navigazione nella barra di stato",

    "editor_config_label": "Configurazione Editor",
    "editor_config_show_line_numbers_checkbox": "Mostra Numeri di Riga",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Visualizza i numeri di riga nell'editor",

    "viewer_config_label": "Configurazione Visualizzatore",
    "viewer_config_process_emojis_checkbox": "Converti Emoji di Testo in Grafica",
    "viewer_config_process_emojis_checkbox_accessible_description":
        "Converti le emoji di testo in rappresentazioni grafiche",
    "viewer_config_highlight_todos_checkbox": "Evidenzia TODO",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Evidenzia le etichette TODO nel testo",
    "viewer_config_open_link_confirmation_checkbox": "Richiedi Conferma per Aprire i Link",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Richiedi conferma prima di aprire i link",
    "viewer_config_save_resources_checkbox": "Salva automaticamente le immagini esterne sul disco",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Salva automaticamente copie delle immagini esterne sul disco per l'accesso offline.",

    "ai_config_inference_module_label": "Modulo di Inferenza",
    "ai_config_inference_module_names_combo_label": "Modulo di Inferenza Attivo",
    "ai_config_inference_module_names_combo_placeholder_text": "Scegli Modulo",
    "ai_config_inference_module_names_combo_accessible_description":
        "Seleziona tra i moduli di inferenza AI disponibili per operare con l'Assistente AI.\n"
        "Le opzioni includono modelli di linguaggio di grandi dimensioni (LLM) con elaborazione in tempo reale,\n"
        "o funzionalità basate su API.",

    "ai_config_base_label": "Parametri di base",
    "ai_config_multi_turn_dialogue_checkbox": "Dialogo multi-turno con memoria conversazionale",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Abilita un dialogo multi-turno che conserva il prompt precedente per la memoria conversazionale.\n"
        "Quando disattivato, solo il nuovo messaggio e il prompt di sistema influenzano la risposta.",
    "ai_config_convert_to_md_checkbox": "Converti il risultato in Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Converte il messaggio di output in formato Markdown.",
}
