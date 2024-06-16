# German lexemes common.py
lexemes = {
    "app_title": "Notolog Editor",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Dateifilterfeld",

    "menu_action_rename": "Umbenennen",
    "menu_action_delete": "Löschen",
    "menu_action_delete_completely": "Vollständig löschen",
    "menu_action_restore": "Wiederherstellen",

    "dialog_file_rename_title": "Datei umbenennen",
    "dialog_file_rename_field_label": "Neuen Dateinamen eingeben",
    "dialog_file_rename_button_ok": "Umbenennen",
    "dialog_file_rename_warning_exists": "Eine Datei mit demselben Namen existiert bereits",

    "dialog_file_delete_title": "Datei löschen",
    "dialog_file_delete_text": "Datei \"{file_name}\" löschen?",
    "dialog_file_delete_completely_title": "Datei endgültig löschen",
    "dialog_file_delete_completely_text": "Datei \"{file_name}\" endgültig löschen?",
    "dialog_file_delete_error": "Datei kann nicht gelöscht werden, ein Fehler ist aufgetreten",
    "dialog_file_delete_error_not_found": "Datei nicht gefunden",

    "dialog_file_restore_title": "Datei wiederherstellen",
    "dialog_file_restore_text": "Datei \"{file_name}\" wiederherstellen?",
    "dialog_file_restore_error": "Die Datei kann nicht wiederhergestellt werden, ein Fehler ist aufgetreten",
    "dialog_file_restore_warning_exists": "Eine Datei mit dem Namen {file_name} existiert bereits",

    "dialog_message_box_title": "Nachricht",
    "dialog_message_box_button_ok": "Schließen",

    "action_new_file_first_line_template_text": "Neues Dokument",
    "action_open_file_dialog_caption": "Datei öffnen",
    "action_save_as_file_dialog_caption": "Datei speichern",

    "dialog_save_empty_file_title": "Leere Datei speichern",
    "dialog_save_empty_file_text": "Das Speichern der Datei ohne Inhalt erlauben?",

    "dialog_encrypt_file_title": "Datei verschlüsseln",
    "dialog_encrypt_file_text": "Datei \"{file_name}\" verschlüsseln?",
    "encrypt_file_warning_file_is_already_encrypted": "Die Datei ist bereits verschlüsselt!",
    "dialog_encrypt_file_rewrite_existing_title": "Vorhandene Datei überschreiben",
    "dialog_encrypt_file_rewrite_existing_text": "Vorhandene Datei \"{file_path}\" überschreiben?",

    "dialog_decrypt_file_title": "Datei entschlüsseln",
    "dialog_decrypt_file_text": "Datei \"{file_name}\" entschlüsseln?",
    "decrypt_file_warning_file_is_not_encrypted": "Die Datei ist nicht verschlüsselt!",
    "dialog_decrypt_file_rewrite_existing_title": "Vorhandene Datei überschreiben",
    "dialog_decrypt_file_rewrite_existing_text": "Vorhandene Datei \"{file_path}\" überschreiben?",

    "dialog_encrypt_new_password_title": "Neues Passwort",
    "dialog_encrypt_new_password_label": "Passwort:",
    "dialog_encrypt_new_password_input_placeholder_text": "Neues Passwort eingeben",
    "dialog_encrypt_new_password_hint_label": "Hinweis:",
    "dialog_encrypt_new_password_hint_label_description":
        "Der Hinweis ist nicht verschlüsselt und kann aus der Datei gelesen werden! "
        "\nVerwenden Sie keine offensichtlichen Hinweise, die leicht erraten werden können, wie Geburtsdaten. "
        "\nVersuchen Sie, eine Referenz zu verwenden, die nicht leicht mit Ihnen in Verbindung gebracht werden kann.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Hinweis eingeben (optional)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Abbrechen",
    "dialog_encrypt_new_password_warning_empty_title": "Warnung",
    "dialog_encrypt_new_password_warning_empty_text": "Das Passwortfeld darf nicht leer sein!",
    "dialog_encrypt_new_password_warning_too_long_title": "Warnung",
    "dialog_encrypt_new_password_warning_too_long_text": "Das Hinweisfeld ist zu lang, maximal {symbols} Zeichen!",

    "dialog_encrypt_password_title": "Passwort eingeben",
    "dialog_encrypt_password_label": "Passwort:",
    "dialog_encrypt_password_input_placeholder_text": "Passwort eingeben",
    "dialog_encrypt_password_hint_label": "Hinweis:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Abbrechen",

    "dialog_encrypt_password_reset_title": "Verschlüsselungspasswort zurücksetzen",
    "dialog_encrypt_password_reset_text":
        "Sind Sie sicher, dass Sie das aktuelle Verschlüsselungspasswort zurücksetzen möchten?",
    "dialog_encrypt_password_reset_button_cancel": "Abbrechen",
    "dialog_encrypt_password_reset_button_yes": "Ja",

    "dialog_open_link_title": "Link",
    "dialog_open_link_text": "Link \"{url}\" in einem Browser öffnen?",

    "dialog_reset_settings_title": "Einstellungen zurücksetzen?",
    "dialog_reset_settings_text":
        "Alle gespeicherten Daten in den Einstellungen werden gelöscht, und die App wird neu gestartet, "
        "um die Änderungen anzuwenden.",

    "field_dir_path_line_edit": "Verzeichnis auswählen",

    "load_file_encryption_password_mismatch": "Verschlüsselungspasswort stimmt nicht überein!",
    "load_file_encryption_password_incorrect": "Falsches Verschlüsselungspasswort!",
    "load_file_none_content_error": "Datei kann nicht geladen werden.",

    "save_active_file_error_occurred": "Datei kann nicht gespeichert werden, ein Fehler ist aufgetreten",

    "expandable_block_default_title": "Weitere Informationen...",

    "dialog_color_picker_color_copied_to_the_clipboard": "Formatierter Text wurde in die Zwischenablage kopiert",

    "popup_about_title": "Anwendungsinfo",
    "popup_about_app_name_description": "Python Markdown-Editor",

    "popup_about_version": "Version",
    "popup_about_license": "Lizenz",
    "popup_about_website": "Webseite",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Datum",

    "update_helper_new_version_is_available": "Eine neue Version '{latest_version}' der App ist verfügbar",
    "update_helper_latest_version_installed": "Die neueste Version der App ist installiert",

    "network_connection_error_empty": "Antwortinformationen können nicht abgerufen werden",
    "network_connection_error_connection_or_dns":
        "Host nicht gefunden. Es könnte ein Problem mit der Internetverbindung oder DNS geben.",
    "network_connection_error_connection_refused":
        "Verbindung abgelehnt. Der Server könnte ausgefallen sein oder es gibt Netzwerkprobleme.",
    "network_connection_error_connection_timed_out": "Verbindung abgelaufen. Es könnte Netzwerkprobleme geben.",
    "network_connection_error_connection_404_error":
        "Verbindungsfehler 404. Die angeforderte Seite oder Ressource wurde nicht gefunden.",
    "network_connection_error_generic_with_status_code": "Anfrage fehlgeschlagen mit Statuscode: {status_code}",
}
