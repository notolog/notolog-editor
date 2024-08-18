# Dutch lexemes common.py
lexemes = {
    "app_title": "Notolog Editor",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Bestandsfilterveld",

    "menu_action_copy_file_path": "Kopieer bestandspad",
    "menu_action_rename": "Hernoemen",
    "menu_action_delete": "Verwijderen",
    "menu_action_delete_completely": "Volledig verwijderen",
    "menu_action_restore": "Herstellen",
    "menu_action_create_new_dir": "Maak een nieuwe map",

    "dialog_file_rename_title": "Bestand hernoemen",
    "dialog_file_rename_field_label": "Voer nieuwe bestandsnaam in",
    "dialog_file_rename_button_ok": "Hernoemen",
    "dialog_file_rename_warning_exists": "Bestand met dezelfde naam bestaat al",

    "dialog_file_delete_title": "Bestand verwijderen",
    "dialog_file_delete_text": "Bestand \"{file_name}\" verwijderen?",
    "dialog_file_delete_completely_title": "Bestand volledig verwijderen",
    "dialog_file_delete_completely_text": "Bestand \"{file_name}\" volledig verwijderen?",
    "dialog_file_delete_error": "Kan bestand niet verwijderen, er is een fout opgetreden",
    "dialog_file_delete_error_not_found": "Bestand niet gevonden",

    "dialog_file_restore_title": "Bestand herstellen",
    "dialog_file_restore_text": "Bestand \"{file_name}\" herstellen?",
    "dialog_file_restore_error": "Kan bestand niet herstellen, er is een fout opgetreden",
    "dialog_file_restore_warning_exists": "Bestand met de naam {file_name} bestaat al",

    "dialog_create_new_dir_title": "Maak een nieuwe map",
    "dialog_create_new_dir_label": "Nieuwe mapnaam",
    "dialog_create_new_dir_input_placeholder_text": "Voer mapnaam in",
    "dialog_create_new_dir_button_ok": "Maak",
    "dialog_create_new_dir_button_cancel": "Annuleer",
    "dialog_create_new_dir_warning_empty_title": "Nieuwe mapnaam fout",
    "dialog_create_new_dir_warning_empty_text": "Mapnaam mag niet leeg zijn",
    "dialog_create_new_dir_warning_too_long_title": "Nieuwe mapnaam fout",
    "dialog_create_new_dir_warning_too_long_text": "Mapnaam is te lang; maximaal {symbols} tekens toegestaan!",
    "dialog_create_new_dir_error_existed": "Map bestaat al",
    "dialog_create_new_dir_error": "Kan map niet maken. Zorg ervoor dat de doelmap {base_dir} beschrijfbaar is",

    "dialog_message_box_title": "Bericht",
    "dialog_message_box_button_ok": "Sluiten",

    "action_new_file_first_line_template_text": "Nieuw document",
    "action_open_file_dialog_caption": "Bestand openen",
    "action_save_as_file_dialog_caption": "Bestand opslaan",

    "dialog_save_empty_file_title": "Leeg bestand opslaan",
    "dialog_save_empty_file_text": "Toestaan om het bestand met lege inhoud op te slaan?",

    "dialog_encrypt_file_title": "Bestand versleutelen",
    "dialog_encrypt_file_text": "Bestand \"{file_name}\" versleutelen?",
    "encrypt_file_warning_file_is_already_encrypted": "Het bestand is al versleuteld!",
    "dialog_encrypt_file_rewrite_existing_title": "Bestaand bestand overschrijven",
    "dialog_encrypt_file_rewrite_existing_text": "Bestaand bestand \"{file_path}\" overschrijven?",

    "dialog_decrypt_file_title": "Bestand ontsleutelen",
    "dialog_decrypt_file_text": "Bestand \"{file_name}\" ontsleutelen?",
    "decrypt_file_warning_file_is_not_encrypted": "Het bestand is niet versleuteld!",
    "dialog_decrypt_file_rewrite_existing_title": "Bestaand bestand herschrijven",
    "dialog_decrypt_file_rewrite_existing_text": "Bestaand bestand \"{file_path}\" herschrijven?",

    "dialog_encrypt_new_password_title": "Nieuw wachtwoord",
    "dialog_encrypt_new_password_label": "Wachtwoord:",
    "dialog_encrypt_new_password_input_placeholder_text": "Nieuw wachtwoord invoeren",
    "dialog_encrypt_new_password_hint_label": "Hint:",
    "dialog_encrypt_new_password_hint_label_description":
        "De hint is niet versleuteld en kan uit het bestand worden gelezen!"
        "\nVermijd voor de hand liggende hints die gemakkelijk geraden kunnen worden, zoals geboortedata."
        "\nProbeer een referentie te gebruiken die niet gemakkelijk met u in verband wordt gebracht.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Hint invoeren (optioneel)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Annuleren",
    "dialog_encrypt_new_password_warning_empty_title": "Waarschuwing",
    "dialog_encrypt_new_password_warning_empty_text": "Het wachtwoordveld mag niet leeg zijn!",
    "dialog_encrypt_new_password_warning_too_long_title": "Waarschuwing",
    "dialog_encrypt_new_password_warning_too_long_text": "Het hintveld is te lang, maximaal {symbols} tekens!",

    "dialog_encrypt_password_title": "Wachtwoord invoeren",
    "dialog_encrypt_password_label": "Wachtwoord:",
    "dialog_encrypt_password_input_placeholder_text": "Wachtwoord invoeren",
    "dialog_encrypt_password_hint_label": "Hint:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Annuleren",

    "dialog_encrypt_password_reset_title": "Versleutelingswachtwoord resetten",
    "dialog_encrypt_password_reset_text": "Weet u zeker dat u het huidige versleutelingswachtwoord wilt resetten?",
    "dialog_encrypt_password_reset_button_cancel": "Annuleren",
    "dialog_encrypt_password_reset_button_yes": "Ja",

    "dialog_open_link_title": "Link",
    "dialog_open_link_text": "Link \"{url}\" openen in een browser?",

    "dialog_reset_settings_title": "Instellingen resetten?",
    "dialog_reset_settings_text":
        "Alle opgeslagen gegevens in de instellingen worden gewist, en de app wordt opnieuw opgestart om wijzigingen "
        "toe te passen.",

    "field_dir_path_line_edit": "Selecteer map",

    "load_file_encryption_password_mismatch": "Versleutelingswachtwoord komt niet overeen!",
    "load_file_encryption_password_incorrect": "Onjuist versleutelingswachtwoord!",
    "load_file_none_content_error": "Bestand kan niet worden geladen.",

    "save_active_file_error_occurred": "Kan bestand niet opslaan, er is een fout opgetreden",

    "expandable_block_default_title": "Meer info...",
    "expandable_block_open_close_tags_mismatch_warning": "Mismatch in <details> blok openen/sluiten tags",

    "dialog_color_picker_color_copied_to_the_clipboard": "Geformatteerde tekst is naar het klembord gekopieerd",

    "popup_about_title": "Applicatie-info",
    "popup_about_app_name_description": "Python Markdown Editor",

    "popup_about_version": "Versie",
    "popup_about_license": "Licentie",
    "popup_about_website": "Website",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Datum",

    "update_helper_new_version_is_available": "Een nieuwe versie '{latest_version}' van de app is beschikbaar",
    "update_helper_latest_version_installed": "De nieuwste versie van de app is geïnstalleerd",

    "network_connection_error_empty": "Kan geen responsinformatie verkrijgen",
    "network_connection_error_connection_or_dns":
        "Host niet gevonden. Er kan een probleem zijn met de internetverbinding of DNS.",
    "network_connection_error_connection_refused":
        "Verbinding geweigerd. De server kan uit zijn, of er kunnen netwerkproblemen zijn.",
    "network_connection_error_connection_timed_out": "Verbindingstijd verstreken. Er kunnen netwerkproblemen zijn.",
    "network_connection_error_connection_404_error":
        "404 fout bij verbinding. De gevraagde pagina of bron is niet gevonden.",
    "network_connection_error_generic_with_status_code": "Verzoek mislukt met statuscode: {status_code}",
}
