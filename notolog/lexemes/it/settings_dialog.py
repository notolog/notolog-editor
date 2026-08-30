# Italian lexemes settings_dialog.py
lexemes = {
    # Impostazioni
    "window_title": "Impostazioni",

    "button_close": "Chiudi",

    "tab_general": "Generale",
    "tab_workspace": "Area di lavoro",
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

    "general_file_deletion_label": "Eliminazione dei file",
    "general_reversible_file_deletion_checkbox": "Elimina i file in modo reversibile",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Sposta i file eliminati nel cestino di Notolog aggiungendo un'estensione .del",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Mostra la Posizione Globale del Cursore",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Visualizza la posizione globale del cursore nella barra di stato",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Mostra frecce di navigazione",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Mostra le frecce di navigazione nella barra di stato",

    "workspace_editor_mode_label": "Modalità editor",
    "workspace_editor_mode_show_line_numbers_checkbox": "Mostra Numeri di Riga",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Visualizza i numeri di riga nell'editor",

    "workspace_view_mode_label": "Modalità visualizzazione",
    "workspace_view_mode_process_emojis_checkbox": "Converti Emoji di Testo in Grafica",
    "workspace_view_mode_process_emojis_checkbox_accessible_description":
        "Converti le emoji di testo in rappresentazioni grafiche",
    "workspace_view_mode_highlight_todos_checkbox": "Evidenzia TODO",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Evidenzia le etichette TODO nel testo",
    "workspace_view_mode_open_link_confirmation_checkbox": "Richiedi Conferma per Aprire i Link",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Richiedi conferma prima di aprire i link",
    "workspace_view_mode_save_resources_checkbox": "Salva automaticamente le immagini esterne sul disco",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
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
    "workspace_bottom_bar_label": "Barra inferiore",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Mostra grafici CPU e memoria",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Mostra i grafici CPU e memoria e il relativo separatore nella barra inferiore",
    "workspace_bottom_bar_system_load_interval_ms_label": "Intervallo di aggiornamento dei grafici",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Imposta ogni quanti millisecondi leggere l'utilizzo di CPU e memoria",
}
