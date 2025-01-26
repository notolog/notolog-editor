# English lexemes common.py
lexemes = {
    "app_title": "Notolog Editor",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "File filter field",

    "menu_action_copy_file_path": "Copy file path",
    "menu_action_rename": "Rename",
    "menu_action_delete": "Delete",
    "menu_action_delete_completely": "Delete completely",
    "menu_action_restore": "Restore",
    "menu_action_create_new_dir": "Create a new directory",

    "dialog_file_rename_title": "Rename file",
    "dialog_file_rename_field_label": "Enter new file name",
    "dialog_file_rename_button_ok": "Rename",
    "dialog_file_rename_warning_exists": "File with the same name already exists",

    "dialog_file_delete_title": "Delete file",
    "dialog_file_delete_text": "Delete file \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Delete file completely",
    "dialog_file_delete_completely_text": "Delete file \"{file_name}\" completely?",
    "dialog_file_delete_error": "Cannot delete file, error occurred",
    "dialog_file_delete_error_not_found": "File not found",

    "dialog_file_restore_title": "Restore file",
    "dialog_file_restore_text": "Restore file \"{file_name}\"?",
    "dialog_file_restore_error": "Cannot restore file, error occurred",
    "dialog_file_restore_warning_exists": "File with the name {file_name} already exists",

    "dialog_create_new_dir_title": "Create a new directory",
    "dialog_create_new_dir_label": "New directory name",
    "dialog_create_new_dir_input_placeholder_text": "Enter directory name",
    "dialog_create_new_dir_button_ok": "Create",
    "dialog_create_new_dir_button_cancel": "Cancel",
    "dialog_create_new_dir_warning_empty_title": "New directory name error",
    "dialog_create_new_dir_warning_empty_text": "Directory name cannot be empty",
    "dialog_create_new_dir_warning_too_long_title": "New directory name error",
    "dialog_create_new_dir_warning_too_long_text": "Directory name is too long; maximum {symbols} characters allowed!",
    "dialog_create_new_dir_error_existed": "Directory already exists",
    "dialog_create_new_dir_error": "Cannot create directory. Ensure the destination directory {base_dir} is writable",

    "dialog_message_box_title": "Message",
    "dialog_message_box_button_ok": "Close",

    "action_new_file_first_line_template_text": "New document",
    "action_open_file_dialog_caption": "Open File",
    "action_save_as_file_dialog_caption": "Save File",

    "dialog_save_empty_file_title": "Save empty file",
    "dialog_save_empty_file_text": "Allow to save the file with an empty content?",

    "dialog_encrypt_file_title": "Encrypt file",
    "dialog_encrypt_file_text": "Encrypt file \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "The file is already encrypted!",
    "dialog_encrypt_file_rewrite_existing_title": "Rewrite existing file",
    "dialog_encrypt_file_rewrite_existing_text": "Rewrite existing file \"{file_path}\"?",

    "dialog_decrypt_file_title": "Decrypt file",
    "dialog_decrypt_file_text": "Decrypt file \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "The file is not encrypted!",
    "dialog_decrypt_file_rewrite_existing_title": "Rewrite existing file",
    "dialog_decrypt_file_rewrite_existing_text": "Rewrite existing file \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "New Password",
    "dialog_encrypt_new_password_label": "Password:",
    "dialog_encrypt_new_password_input_placeholder_text": "Enter New Password",
    "dialog_encrypt_new_password_hint_label": "Hint:",
    "dialog_encrypt_new_password_hint_label_description": "The hint is not encrypted and can be read from the file!"
                                                          "\nAvoid obvious hints that can be easily guessed, such as "
                                                          "birth dates."
                                                          "\nTry to use a reference that is not easily associated with you.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Enter Hint (Optional)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Cancel",
    "dialog_encrypt_new_password_warning_empty_title": "Warning",
    "dialog_encrypt_new_password_warning_empty_text": "The password field cannot be empty!",
    "dialog_encrypt_new_password_warning_too_long_title": "Warning",
    "dialog_encrypt_new_password_warning_too_long_text": "The hint field is too long, maximum {symbols} characters!",

    "dialog_encrypt_password_title": "Enter Password",
    "dialog_encrypt_password_label": "Password:",
    "dialog_encrypt_password_input_placeholder_text": "Enter Password",
    "dialog_encrypt_password_hint_label": "Hint:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Cancel",

    "dialog_encrypt_password_reset_title": "Reset Encryption Password",
    "dialog_encrypt_password_reset_text": "Are you sure you want to reset the current encryption password?",
    "dialog_encrypt_password_reset_button_cancel": "Cancel",
    "dialog_encrypt_password_reset_button_yes": "Yes",

    "dialog_open_link_title": "Link",
    "dialog_open_link_text": "Open link \"{url}\" in a browser?",

    "dialog_reset_settings_title": "Reset settings?",
    "dialog_reset_settings_text":
        "All stored data in settings will be cleared, and the app will restart to apply changes.",

    "dialog_exit_unsaved_title": "Confirm Exit",
    "dialog_exit_unsaved_text": "The opened file '{file_name}' cannot be saved. Continue with exit?",

    "message_app_config_file_access": "Permission denied when accessing the app configuration file at {file_path}. "
        "Set the correct permissions to ensure proper operation.",

    "field_dir_path_dialog_caption": "Select Directory",
    "field_file_path_dialog_caption": "Select File",

    "dialog_select_default_dir_title": "Select Default Folder",
    "dialog_select_default_dir_label": "Select the default folder for notes",
    "dialog_select_default_dir_input_placeholder_text": "Default Notes Folder",
    "dialog_select_default_dir_button_ok": "Select",
    "dialog_select_default_dir_button_cancel": "Cancel",

    "load_file_encryption_password_mismatch": "Encryption password mismatch!",
    "load_file_encryption_password_incorrect": "Incorrect encryption password!",
    "load_file_none_content_error": "The file cannot be loaded.",

    "open_dir_permission_error": "Permission denied when accessing the directory.",
    "open_file_permission_error": "Permission denied when accessing the file.",
    "rename_file_permission_error": "Permission denied when renaming the file.",

    "action_new_file_error_occurred": "Cannot create file; an error occurred.\nCheck file system permissions.",
    "save_active_file_error_occurred": "Cannot save file; an error occurred.",

    "expandable_block_default_title": "More info...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> block open/close tags mismatch",

    "dialog_color_picker_color_copied_to_the_clipboard": "Formatted text has been copied to the clipboard",

    "popup_about_title": "Application Info",
    "popup_about_app_name_description": "Python Markdown Editor",

    "popup_about_version": "Version",
    "popup_about_license": "License",
    "popup_about_website": "Website",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Date",

    "update_helper_new_version_is_available": "A new version {latest_version} of the app is available",
    "update_helper_latest_version_installed": "The latest version of the app is installed",

    "network_connection_error_empty": "Cannot obtain response information",
    "network_connection_error_connection_or_dns":
        "Host not found. There may be an issue with the internet connection or DNS.",
    "network_connection_error_connection_refused":
        "Connection refused. The server might be down, or there may be network issues.",
    "network_connection_error_connection_timed_out": "Connection timed out. There may be network issues.",
    "network_connection_error_connection_404_error":
        "Connection 404 error. The requested page or resource is not found.",
    "network_connection_error_generic_with_status_code": "Request failed with status code: {status_code}",
}
