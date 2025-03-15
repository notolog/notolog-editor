# Italian lexemes common.py
lexemes = {
    "app_title": "Editor Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_input_placeholder_text": "Filtro rapido",
    "tree_filter_input_accessible_desc": "Filtra file e directory per nome",

    "menu_action_copy_file_path": "Copia il percorso del file",
    "menu_action_rename": "Rinomina",
    "menu_action_delete": "Elimina",
    "menu_action_delete_completely": "Elimina completamente",
    "menu_action_restore": "Ripristina",
    "menu_action_create_new_dir": "Crea una nuova directory",

    "dialog_file_rename_title": "Rinomina file",
    "dialog_file_rename_field_label": "Inserisci nuovo nome file",
    "dialog_file_rename_button_ok": "Rinomina",
    "dialog_file_rename_warning_exists": "Esiste già un file con lo stesso nome",

    "dialog_file_delete_title": "Elimina file",
    "dialog_file_delete_text": "Eliminare il file \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Elimina file definitivamente",
    "dialog_file_delete_completely_text": "Eliminare definitivamente il file \"{file_name}\"?",
    "dialog_file_delete_error": "Impossibile eliminare il file, si è verificato un errore",
    "dialog_file_delete_error_not_found": "File non trovato",

    "dialog_file_restore_title": "Ripristina file",
    "dialog_file_restore_text": "Ripristinare il file \"{file_name}\"?",
    "dialog_file_restore_error": "Impossibile ripristinare il file, si è verificato un errore",
    "dialog_file_restore_warning_exists": "Esiste già un file con il nome {file_name}",

    "dialog_create_new_dir_title": "Crea una nuova directory",
    "dialog_create_new_dir_label": "Nome della nuova directory",
    "dialog_create_new_dir_input_placeholder_text": "Inserisci il nome della directory",
    "dialog_create_new_dir_button_ok": "Crea",
    "dialog_create_new_dir_button_cancel": "Annulla",
    "dialog_create_new_dir_warning_empty_title": "Errore nel nome della nuova directory",
    "dialog_create_new_dir_warning_empty_text": "Il nome della directory non può essere vuoto",
    "dialog_create_new_dir_warning_too_long_title": "Errore nel nome della nuova directory",
    "dialog_create_new_dir_warning_too_long_text": "Il nome della directory è troppo lungo; massimo "
                                                   "{symbols} caratteri consentiti!",
    "dialog_create_new_dir_error_existed": "La directory esiste già",
    "dialog_create_new_dir_error": "Impossibile creare la directory. Assicurati che la directory di destinazione "
                                   "{base_dir} sia scrivibile",

    "dialog_message_box_title": "Messaggio",
    "dialog_message_box_button_ok": "Chiudi",

    "action_new_file_first_line_template_text": "Nuovo documento",
    "action_open_file_dialog_caption": "Apri file",
    "action_save_as_file_dialog_caption": "Salva file",

    "dialog_save_empty_file_title": "Salva file vuoto",
    "dialog_save_empty_file_text": "Consentire di salvare il file senza contenuto?",

    "dialog_encrypt_file_title": "Cripta file",
    "dialog_encrypt_file_text": "Criptare il file \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "Il file è già criptato!",
    "dialog_encrypt_file_rewrite_existing_title": "Sovrascrivi file esistente",
    "dialog_encrypt_file_rewrite_existing_text": "Sovrascrivere il file esistente \"{file_path}\"?",

    "dialog_decrypt_file_title": "Decripta file",
    "dialog_decrypt_file_text": "Decriptare il file \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "Il file non è criptato!",
    "dialog_decrypt_file_rewrite_existing_title": "Sovrascrivi file esistente",
    "dialog_decrypt_file_rewrite_existing_text": "Sovrascrivere il file esistente \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Nuova password",
    "dialog_encrypt_new_password_label": "Password:",
    "dialog_encrypt_new_password_input_placeholder_text": "Inserisci la nuova password",
    "dialog_encrypt_new_password_hint_label": "Suggerimento:",
    "dialog_encrypt_new_password_hint_label_description":
        "Il suggerimento non è criptato e può essere letto dal file!"
        "\nNon utilizzare suggerimenti ovvi che possono essere indovinati, come"
        "\nla data di nascita, ecc. Prova a usare un riferimento.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Inserisci un suggerimento (opzionale)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Annulla",
    "dialog_encrypt_new_password_warning_empty_title": "Avviso",
    "dialog_encrypt_new_password_warning_empty_text": "Il campo della password non può essere vuoto!",
    "dialog_encrypt_new_password_warning_too_long_title": "Avviso",
    "dialog_encrypt_new_password_warning_too_long_text":
        "Il campo del suggerimento è troppo lungo, massimo {symbols} caratteri!",

    "dialog_encrypt_password_title": "Inserisci password",
    "dialog_encrypt_password_label": "Password:",
    "dialog_encrypt_password_input_placeholder_text": "Inserisci password",
    "dialog_encrypt_password_hint_label": "Suggerimento:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Annulla",

    "dialog_encrypt_password_reset_title": "Reimposta password di criptazione",
    "dialog_encrypt_password_reset_text": "Sei sicuro di voler reimpostare la password di criptazione attuale?",
    "dialog_encrypt_password_reset_button_cancel": "Annulla",
    "dialog_encrypt_password_reset_button_yes": "Sì",

    "dialog_open_link_title": "Link",
    "dialog_open_link_text": "Aprire il link \"{url}\" nel browser?",

    "dialog_reset_settings_title": "Reimposta impostazioni?",
    "dialog_reset_settings_text":
        "Tutti i dati memorizzati nelle impostazioni verranno cancellati, e l'app verrà riavviata per applicare "
        "le modifiche.",

    "dialog_exit_unsaved_title": "Conferma Uscita",
    "dialog_exit_unsaved_text": "Il file aperto '{file_name}' non può essere salvato. Continuare con l'uscita?",

    "message_app_config_file_access": "Permesso negato durante l'accesso al file di configurazione dell'applicazione in "
                                      "{file_path}. Imposta i permessi corretti per garantire un funzionamento adeguato.",

    "field_dir_path_dialog_caption": "Seleziona Directory",
    "field_file_path_dialog_caption": "Seleziona File",

    "dialog_select_default_dir_title": "Seleziona cartella predefinita",
    "dialog_select_default_dir_label": "Seleziona la cartella predefinita per le note",
    "dialog_select_default_dir_input_placeholder_text": "Cartella predefinita delle note",
    "dialog_select_default_dir_button_ok": "Seleziona",
    "dialog_select_default_dir_button_cancel": "Annulla",

    "load_file_encryption_password_mismatch": "La password di crittografia non corrisponde!",
    "load_file_encryption_password_incorrect": "Password di crittografia errata!",
    "load_file_none_content_error": "Impossibile caricare il file.",

    "open_dir_permission_error": "Permesso negato per accedere alla directory.",
    "open_file_permission_error": "Permesso negato durante l'accesso al file.",
    "rename_file_permission_error": "Permesso negato durante la rinomina del file.",

    "action_new_file_error_occurred": "Impossibile creare il file; si è verificato un errore."
                                      "\nControllare le autorizzazioni del file system.",
    "save_active_file_error_occurred": "Impossibile salvare il file; si è verificato un errore.",

    "expandable_block_default_title": "Ulteriori informazioni...",
    "expandable_block_open_close_tags_mismatch_warning":
        "Incompatibilità delle tag di apertura/chiusura del blocco <details>",

    "dialog_color_picker_color_copied_to_the_clipboard": "Il testo formattato è stato copiato negli appunti",

    "popup_about_title": "Informazioni sull'Applicazione",
    "popup_about_app_name_description": "Editor Markdown Python",

    "popup_about_version": "Versione",
    "popup_about_license": "Licenza",
    "popup_about_website": "Sito Web",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Data",

    "update_helper_new_version_is_available": "Nuova versione {latest_version} dell'app disponibile",
    "update_helper_latest_version_installed": "L'ultima versione dell'app è installata",

    "network_connection_error_empty": "Impossibile ottenere informazioni sulla risposta",
    "network_connection_error_connection_or_dns":
        "Host non trovato. Potrebbe esserci un problema con la connessione internet o il DNS.",
    "network_connection_error_connection_refused":
        "Connessione rifiutata. Il server potrebbe essere non operativo o ci sono problemi di rete.",
    "network_connection_error_connection_timed_out": "Connessione scaduta. Potrebbero esserci problemi di rete.",
    "network_connection_error_connection_404_error":
        "Errore di connessione 404. La pagina o risorsa richiesta non è stata trovata.",
    "network_connection_error_generic_with_status_code": "Richiesta fallita con codice di stato: {status_code}",
}
