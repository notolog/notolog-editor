# German lexemes common.py
lexemes = {
    "app_title": "Notolog Editor",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Dateifilterfeld",

    "menu_action_copy_file_path": "Dateipfad kopieren",
    "menu_action_rename": "Umbenennen",
    "menu_action_delete": "Löschen",
    "menu_action_delete_completely": "Vollständig löschen",
    "menu_action_restore": "Wiederherstellen",
    "menu_action_create_new_dir": "Neues Verzeichnis erstellen",

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

    "dialog_create_new_dir_title": "Neues Verzeichnis erstellen",
    "dialog_create_new_dir_label": "Neuer Verzeichnisname",
    "dialog_create_new_dir_input_placeholder_text": "Verzeichnisnamen eingeben",
    "dialog_create_new_dir_button_ok": "Erstellen",
    "dialog_create_new_dir_button_cancel": "Abbrechen",
    "dialog_create_new_dir_warning_empty_title": "Fehler bei neuem Verzeichnisnamen",
    "dialog_create_new_dir_warning_empty_text": "Der Verzeichnisname darf nicht leer sein",
    "dialog_create_new_dir_warning_too_long_title": "Fehler bei neuem Verzeichnisnamen",
    "dialog_create_new_dir_warning_too_long_text": "Der Verzeichnisname ist zu lang; maximal "
                                                   "{symbols} Zeichen erlaubt!",
    "dialog_create_new_dir_error_existed": "Verzeichnis existiert bereits",
    "dialog_create_new_dir_error": "Verzeichnis kann nicht erstellt werden. Stellen Sie sicher, "
                                   "dass das Zielverzeichnis {base_dir} beschreibbar ist",

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

    "dialog_exit_unsaved_title": "Beenden Bestätigen",
    "dialog_exit_unsaved_text": "Die geöffnete Datei '{file_name}' kann nicht gespeichert werden. Trotzdem beenden?",

    "message_app_config_file_access": "Zugriff verweigert beim Zugriff auf die Anwendungskonfigurationsdatei unter "
                                      "{file_path}. Setzen Sie die richtigen Berechtigungen, um einen ordnungsgemäßen "
                                      "Betrieb zu gewährleisten.",

    "field_dir_path_dialog_caption": "Verzeichnis auswählen",
    "field_file_path_dialog_caption": "Datei auswählen",

    "dialog_select_default_dir_title": "Standardordner auswählen",
    "dialog_select_default_dir_label": "Wählen Sie den Standardordner für Notizen",
    "dialog_select_default_dir_input_placeholder_text": "Standardnotizenordner",
    "dialog_select_default_dir_button_ok": "Auswählen",
    "dialog_select_default_dir_button_cancel": "Abbrechen",

    "load_file_encryption_password_mismatch": "Verschlüsselungs-Passwort stimmt nicht überein!",
    "load_file_encryption_password_incorrect": "Falsches Verschlüsselungs-Passwort!",
    "load_file_none_content_error": "Die Datei kann nicht geladen werden.",

    "open_dir_permission_error": "Zugriff auf das Verzeichnis verweigert.",
    "open_file_permission_error": "Zugriff auf die Datei verweigert.",
    "rename_file_permission_error": "Umbenennen der Datei verweigert.",

    "action_new_file_error_occurred": "Datei kann nicht erstellt werden; ein Fehler ist aufgetreten."
                                      "\nÜberprüfen Sie die Dateisystemberechtigungen.",
    "save_active_file_error_occurred": "Datei kann nicht gespeichert werden; ein Fehler ist aufgetreten.",

    "expandable_block_default_title": "Weitere Informationen...",
    "expandable_block_open_close_tags_mismatch_warning": "Fehlerhafte <details>-Block Öffnen/Schließen-Tags",

    "dialog_color_picker_color_copied_to_the_clipboard": "Formatierter Text wurde in die Zwischenablage kopiert",

    "popup_about_title": "Anwendungsinfo",
    "popup_about_app_name_description": "Python Markdown-Editor",

    "popup_about_version": "Version",
    "popup_about_license": "Lizenz",
    "popup_about_website": "Webseite",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Datum",

    "update_helper_new_version_is_available": "Eine neue Version {latest_version} der App ist verfügbar",
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
