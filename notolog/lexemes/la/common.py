# Lexica Communia Latine common.py
lexemes = {
    "app_title": "Editorium Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Locus filtrationis fasciculorum",

    "menu_action_copy_file_path": "Via fasciculi exemplum",
    "menu_action_rename": "Nomen Mutare",
    "menu_action_delete": "Delere",
    "menu_action_delete_completely": "Delere prorsus",
    "menu_action_restore": "Restituere",
    "menu_action_create_new_dir": "Crea novum directory",

    "dialog_file_rename_title": "Fasciculum renominare",
    "dialog_file_rename_field_label": "Nomen novum fasciculi ingredi",
    "dialog_file_rename_button_ok": "Renominare",
    "dialog_file_rename_warning_exists": "Liber eodem nomine iam existit",

    "dialog_file_delete_title": "Fasciculum delere",
    "dialog_file_delete_text": "Fasciculum \"{file_name}\" delere?",
    "dialog_file_delete_completely_title": "Delere tabulatum prorsus",
    "dialog_file_delete_completely_text": "Delere prorsus tabulatum \"{file_name}\"?",
    "dialog_file_delete_error": "Fasciculum delere non potest, error accidit",
    "dialog_file_delete_error_not_found": "Fasciculus non inventus",

    "dialog_file_restore_title": "Liber Restituere",
    "dialog_file_restore_text": "Liber \"{file_name}\" restituere?",
    "dialog_file_restore_error": "Liber restituere non potest, error accidit",
    "dialog_file_restore_warning_exists": "Liber nomine {file_name} iam existit",

    "dialog_create_new_dir_title": "Crea novum directory",
    "dialog_create_new_dir_label": "Novum nomen directory",
    "dialog_create_new_dir_input_placeholder_text": "Inserere nomen directory",
    "dialog_create_new_dir_button_ok": "Crea",
    "dialog_create_new_dir_button_cancel": "Cancel",
    "dialog_create_new_dir_warning_empty_title": "Novum nomen directory error",
    "dialog_create_new_dir_warning_empty_text": "Nomen directory vacuum esse non potest",
    "dialog_create_new_dir_warning_too_long_title": "Novum nomen directory error",
    "dialog_create_new_dir_warning_too_long_text": "Nomen directory nimis longum est; maxime "
                                                   "{symbols} litterarum permissum est!",
    "dialog_create_new_dir_error_existed": "Directory iam existit",
    "dialog_create_new_dir_error": "Fieri non potest directory creare. Fac ut directory destinatum "
                                   "{base_dir} scribibile sit",

    "dialog_message_box_title": "Nuntius",
    "dialog_message_box_button_ok": "Claudere",

    "action_new_file_first_line_template_text": "Documentum novum",
    "action_open_file_dialog_caption": "Fasciculum aperire",
    "action_save_as_file_dialog_caption": "Fasciculum salvare",

    "dialog_save_empty_file_title": "Serva File Vacuus",
    "dialog_save_empty_file_text": "Permittere servare file sine contento?",

    "dialog_encrypt_file_title": "Fasciculum codicare",
    "dialog_encrypt_file_text": "Fasciculum \"{file_name}\" codicare?",
    "encrypt_file_warning_file_is_already_encrypted": "Fasciculus iam codicatus est!",
    "dialog_encrypt_file_rewrite_existing_title": "Fasciculum exsistentem rescribere",
    "dialog_encrypt_file_rewrite_existing_text": "Fasciculum exsistentem \"{file_path}\" rescribere?",

    "dialog_decrypt_file_title": "Fasciculum decodicare",
    "dialog_decrypt_file_text": "Fasciculum \"{file_name}\" decodicare?",
    "decrypt_file_warning_file_is_not_encrypted": "Fasciculus non est codicatus!",
    "dialog_decrypt_file_rewrite_existing_title": "Fasciculum exsistentem rescribere",
    "dialog_decrypt_file_rewrite_existing_text": "Fasciculum exsistentem \"{file_path}\" rescribere?",

    "dialog_encrypt_new_password_title": "Novum Signum",
    "dialog_encrypt_new_password_label": "Signum:",
    "dialog_encrypt_new_password_input_placeholder_text": "Novum signum ingredere",
    "dialog_encrypt_new_password_hint_label": "Monitum:",
    "dialog_encrypt_new_password_hint_label_description":
        "Monitum non est cryptatum et legi potest ex archivo!"
        "\nNoli uti monitis perspicuis quae facile divinari possunt, ut"
        "\nnatale diem vel similia. Conare uti referentia non facile associata.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Ingredere monitum (non necessarium)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Cancellare",
    "dialog_encrypt_new_password_warning_empty_title": "Monitio",
    "dialog_encrypt_new_password_warning_empty_text": "Area signi vacua esse non potest!",
    "dialog_encrypt_new_password_warning_too_long_title": "Monitio",
    "dialog_encrypt_new_password_warning_too_long_text": "Area moniti nimis longa est, maximum {symbols} signa!",

    "dialog_encrypt_password_title": "Ingredere Signum",
    "dialog_encrypt_password_label": "Signum:",
    "dialog_encrypt_password_input_placeholder_text": "Signum ingredere",
    "dialog_encrypt_password_hint_label": "Monitum:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Cancellare",

    "dialog_encrypt_password_reset_title": "Signum Cryptatum Reset",
    "dialog_encrypt_password_reset_text": "Certusne es te velle currentem signum cryptatum reset?",
    "dialog_encrypt_password_reset_button_cancel": "Cancellare",
    "dialog_encrypt_password_reset_button_yes": "Ita",

    "dialog_open_link_title": "Vinculum",
    "dialog_open_link_text": "Vinculum \"{url}\" in navigatro aperire?",

    "dialog_reset_settings_title": "Reddere ad initium?",
    "dialog_reset_settings_text":
        "Omnia in configurationibus data delebuntur, et app ad mutationes applicandas restituetur.",

    "dialog_exit_unsaved_title": "Confirma Exitus",
    "dialog_exit_unsaved_text": "Apertum lima '{file_name}' servari non potest. Exitus procedere?",

    "message_app_config_file_access": "Permissio negata cum accedere ad configurationem applicationis limam in {file_path}. "
                                      "Constitue rectas permissiones ut operationem debitam asseguras.",

    "field_dir_path_dialog_caption": "Directory Select",
    "field_file_path_dialog_caption": "File Select",

    "load_file_encryption_password_mismatch": "Signi codicis discrepantia!",
    "load_file_encryption_password_incorrect": "Signum codicis incorrectum!",
    "load_file_none_content_error": "Fasciculum onerare non potest.",

    "action_new_file_error_occurred": "Filem creare non potest; error occurrit.\nPermissiones systematis file inspice.",
    "save_active_file_error_occurred": "Filem servare non potest; error occurrit.",

    "expandable_block_default_title": "Amplius info...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> claudit/aperit block adsigna discongruitas",

    "dialog_color_picker_color_copied_to_the_clipboard": "Textus formatus in tabulam appensionis est copiatus",

    "popup_about_title": "De Applicatione",
    "popup_about_app_name_description": "Editor Markdown Pythonis",

    "popup_about_version": "Versio",
    "popup_about_license": "Licentia",
    "popup_about_website": "Situs",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Dies",

    "update_helper_new_version_is_available": "Nova versio {latest_version} applicationis praesto est",
    "update_helper_latest_version_installed": "Ultima versio applicationis installata est",

    "network_connection_error_empty": "Informationes responsi obtineri non possunt",
    "network_connection_error_connection_or_dns":
        "Hospes non inventus est. Problema cum nexu interretiali aut DNS esse potest.",
    "network_connection_error_connection_refused":
        "Coniunctio recusata est. Servus deorsum ire potest, vel sunt problemae retis.",
    "network_connection_error_connection_timed_out": "Tempus coniunctionis excedit. Problemae retis esse possunt.",
    "network_connection_error_connection_404_error":
        "Error coniunctionis 404. Pagina vel res quaesita non inventa est.",
    "network_connection_error_generic_with_status_code": "Postulatio defecit cum statu codice: {status_code}",
}
