# Swedish lexemes common.py
lexemes = {
    "app_title": "Notolog Redigerare",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Filterfält för filer",

    "menu_action_rename": "Byt namn",
    "menu_action_delete": "Radera",
    "menu_action_delete_completely": "Radera helt",
    "menu_action_restore": "Återställ",

    "dialog_file_rename_title": "Byt namn på fil",
    "dialog_file_rename_field_label": "Ange nytt filnamn",
    "dialog_file_rename_button_ok": "Byt namn",
    "dialog_file_rename_warning_exists": "En fil med samma namn finns redan",

    "dialog_file_delete_title": "Radera fil",
    "dialog_file_delete_text": "Vill du radera filen \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Radera filen helt",
    "dialog_file_delete_completely_text": "Vill du radera filen \"{file_name}\" helt?",
    "dialog_file_delete_error": "Kan inte radera filen, ett fel inträffade",
    "dialog_file_delete_error_not_found": "Filen hittades inte",

    "dialog_file_restore_title": "Återställ fil",
    "dialog_file_restore_text": "Återställ filen \"{file_name}\"?",
    "dialog_file_restore_error": "Kan inte återställa filen, ett fel inträffade",
    "dialog_file_restore_warning_exists": "En fil med namnet {file_name} finns redan",

    "dialog_message_box_title": "Meddelande",
    "dialog_message_box_button_ok": "Stäng",

    "action_new_file_first_line_template_text": "Nytt dokument",
    "action_open_file_dialog_caption": "Öppna fil",
    "action_save_as_file_dialog_caption": "Spara fil",

    "dialog_save_empty_file_title": "Spara tom fil",
    "dialog_save_empty_file_text": "Tillåt att spara filen med tomt innehåll?",

    "dialog_encrypt_file_title": "Kryptera fil",
    "dialog_encrypt_file_text": "Kryptera filen \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "Filen är redan krypterad!",
    "dialog_encrypt_file_rewrite_existing_title": "Skriv över befintlig fil",
    "dialog_encrypt_file_rewrite_existing_text": "Skriv över den befintliga filen \"{file_path}\"?",

    "dialog_decrypt_file_title": "Dekryptera fil",
    "dialog_decrypt_file_text": "Dekryptera filen \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "Filen är inte krypterad!",
    "dialog_decrypt_file_rewrite_existing_title": "Skriv över befintlig fil",
    "dialog_decrypt_file_rewrite_existing_text": "Skriv över den befintliga filen \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Nytt lösenord",
    "dialog_encrypt_new_password_label": "Lösenord:",
    "dialog_encrypt_new_password_input_placeholder_text": "Ange nytt lösenord",
    "dialog_encrypt_new_password_hint_label": "Ledtråd:",
    "dialog_encrypt_new_password_hint_label_description": "Ledtråden är inte krypterad och kan läsas från filen!"
                                                          "\nUndvik uppenbara ledtrådar som kan gissas lätt, såsom "
                                                          "födelsedatum."
                                                          "\nFörsök använda en referens som inte lätt kan kopplas till dig.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Ange ledtråd (valfritt)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Avbryt",
    "dialog_encrypt_new_password_warning_empty_title": "Varning",
    "dialog_encrypt_new_password_warning_empty_text": "Lösenordsfältet får inte vara tomt!",
    "dialog_encrypt_new_password_warning_too_long_title": "Varning",
    "dialog_encrypt_new_password_warning_too_long_text": "Ledtrådsfältet är för långt, max {symbols} tecken!",

    "dialog_encrypt_password_title": "Ange lösenord",
    "dialog_encrypt_password_label": "Lösenord:",
    "dialog_encrypt_password_input_placeholder_text": "Ange lösenord",
    "dialog_encrypt_password_hint_label": "Ledtråd:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Avbryt",

    "dialog_encrypt_password_reset_title": "Återställ krypteringslösenord",
    "dialog_encrypt_password_reset_text": "Är du säker på att du vill återställa det nuvarande krypteringslösenordet?",
    "dialog_encrypt_password_reset_button_cancel": "Avbryt",
    "dialog_encrypt_password_reset_button_yes": "Ja",

    "dialog_open_link_title": "Länk",
    "dialog_open_link_text": "Öppna länken \"{url}\" i en webbläsare?",

    "load_file_encryption_password_mismatch": "Krypteringslösenordet stämmer inte!",
    "load_file_encryption_password_incorrect": "Fel krypteringslösenord!",
    "load_file_none_content_error": "Filen kan inte laddas.",

    "save_active_file_error_occurred": "Kan inte spara filen, ett fel inträffade",

    "expandable_block_default_title": "Mer information...",

    "dialog_color_picker_color_copied_to_the_clipboard": "Formaterad text har kopierats till urklipp",

    "popup_about_title": "Om programmet",
    "popup_about_app_name_description": "Python Markdown-redigerare",

    "popup_about_version": "Version",
    "popup_about_license": "Licens",
    "popup_about_website": "Webbplats",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Datum",

    "update_helper_new_version_is_available": "En ny version '{latest_version}' av appen är tillgänglig",
    "update_helper_latest_version_installed": "Den senaste versionen av appen är installerad",

    "network_connection_error_empty": "Kan inte hämta svarsinformation",
    "network_connection_error_connection_or_dns":
        "Värden hittades inte. Det kan vara ett problem med internetanslutningen eller DNS.",
    "network_connection_error_connection_refused":
        "Anslutningen nekades. Servern kan vara nere, eller så kan det finnas nätverksproblem.",
    "network_connection_error_connection_timed_out": "Anslutningen löpte ut i tid. Det kan finnas nätverksproblem.",
    "network_connection_error_connection_404_error":
        "404-fel vid anslutning. Den begärda sidan eller resursen hittades inte.",
    "network_connection_error_generic_with_status_code": "Förfrågan misslyckades med statuskod: {status_code}",
}
