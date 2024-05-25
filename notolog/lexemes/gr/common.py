# Greek lexemes common.py
lexemes = {
    "app_title": "Επεξεργαστής Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Πεδίο φίλτρου αρχείου",

    "menu_action_rename": "Μετονομασία",
    "menu_action_delete": "Διαγραφή",
    "menu_action_delete_completely": "Ολοκληρωτική διαγραφή",
    "menu_action_restore": "Επαναφορά",

    "dialog_file_rename_title": "Μετονομασία αρχείου",
    "dialog_file_rename_field_label": "Εισάγετε νέο όνομα αρχείου",
    "dialog_file_rename_button_ok": "Μετονομάστε",
    "dialog_file_rename_warning_exists": "Ένα αρχείο με το ίδιο όνομα υπάρχει ήδη",

    "dialog_file_delete_title": "Διαγραφή αρχείου",
    "dialog_file_delete_text": "Διαγραφή του αρχείου \"{file_name}\";",
    "dialog_file_delete_completely_title": "Ολοκληρωτική διαγραφή αρχείου",
    "dialog_file_delete_completely_text": "Ολοκληρωτική διαγραφή του αρχείου \"{file_name}\";",
    "dialog_file_delete_error": "Αδυναμία διαγραφής αρχείου, συνέβη σφάλμα",
    "dialog_file_delete_error_not_found": "Το αρχείο δεν βρέθηκε",

    "dialog_file_restore_title": "Επαναφορά αρχείου",
    "dialog_file_restore_text": "Επαναφορά του αρχείου \"{file_name}\";",
    "dialog_file_restore_error": "Αδυναμία επαναφοράς αρχείου, συνέβη σφάλμα",
    "dialog_file_restore_warning_exists": "Ένα αρχείο με το όνομα {file_name} υπάρχει ήδη",

    "dialog_message_box_title": "Μήνυμα",
    "dialog_message_box_button_ok": "Κλείσιμο",

    "action_new_file_first_line_template_text": "Νέο έγγραφο",
    "action_open_file_dialog_caption": "Άνοιγμα Αρχείου",
    "action_save_as_file_dialog_caption": "Αποθήκευση Αρχείου",

    "dialog_save_empty_file_title": "Αποθήκευση κενού αρχείου",
    "dialog_save_empty_file_text": "Να επιτραπεί η αποθήκευση του αρχείου χωρίς περιεχόμενο;",

    "dialog_encrypt_file_title": "Κρυπτογράφηση αρχείου",
    "dialog_encrypt_file_text": "Κρυπτογράφηση του αρχείου \"{file_name}\";",
    "encrypt_file_warning_file_is_already_encrypted": "Το αρχείο είναι ήδη κρυπτογραφημένο!",
    "dialog_encrypt_file_rewrite_existing_title": "Επανεγγραφή υπάρχοντος αρχείου",
    "dialog_encrypt_file_rewrite_existing_text": "Επανεγγραφή υπάρχοντος αρχείου \"{file_path}\";",

    "dialog_decrypt_file_title": "Αποκρυπτογράφηση αρχείου",
    "dialog_decrypt_file_text": "Αποκρυπτογράφηση του αρχείου \"{file_name}\";",
    "decrypt_file_warning_file_is_not_encrypted": "Το αρχείο δεν είναι κρυπτογραφημένο!",
    "dialog_decrypt_file_rewrite_existing_title": "Επανεγγραφή υπάρχοντος αρχείου",
    "dialog_decrypt_file_rewrite_existing_text": "Επανεγγραφή υπάρχοντος αρχείου \"{file_path}\";",

    "dialog_encrypt_new_password_title": "Νέος Κωδικός",
    "dialog_encrypt_new_password_label": "Κωδικός:",
    "dialog_encrypt_new_password_input_placeholder_text": "Εισάγετε νέο κωδικό",
    "dialog_encrypt_new_password_hint_label": "Υπόδειξη:",
    "dialog_encrypt_new_password_hint_label_description":
        "Η υπόδειξη δεν είναι κρυπτογραφημένη και μπορεί να διαβαστεί "
        "από το αρχείο!\nΑποφύγετε προφανείς υποδείξεις που μπορεί να "
        "μαντευτούν εύκολα, όπως ημερομηνίες γέννησης.\nΠροσπαθήστε "
        "να χρησιμοποιήσετε μια αναφορά που δεν συνδέεται εύκολα με εσάς.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Εισάγετε υπόδειξη (προαιρετικά)",
    "dialog_encrypt_new_password_button_ok": "Εντάξει",
    "dialog_encrypt_new_password_button_cancel": "Ακύρωση",
    "dialog_encrypt_new_password_warning_empty_title": "Προειδοποίηση",
    "dialog_encrypt_new_password_warning_empty_text": "Το πεδίο του κωδικού δεν μπορεί να είναι άδειο!",
    "dialog_encrypt_new_password_warning_too_long_title": "Προειδοποίηση",
    "dialog_encrypt_new_password_warning_too_long_text":
        "Το πεδίο της υπόδειξης είναι πολύ μακρύ, μέγιστο {symbols} χαρακτήρες!",

    "dialog_encrypt_password_title": "Εισαγωγή Κωδικού",
    "dialog_encrypt_password_label": "Κωδικός:",
    "dialog_encrypt_password_input_placeholder_text": "Εισάγετε κωδικό",
    "dialog_encrypt_password_hint_label": "Υπόδειξη:",
    "dialog_encrypt_password_button_ok": "Εντάξει",
    "dialog_encrypt_password_button_cancel": "Ακύρωση",

    "dialog_encrypt_password_reset_title": "Επαναφορά Κωδικού Κρυπτογράφησης",
    "dialog_encrypt_password_reset_text":
        "Είστε σίγουροι ότι θέλετε να επαναφέρετε τον τρέχοντα κωδικό κρυπτογράφησης;",
    "dialog_encrypt_password_reset_button_cancel": "Ακύρωση",
    "dialog_encrypt_password_reset_button_yes": "Ναι",

    "dialog_open_link_title": "Σύνδεσμος",
    "dialog_open_link_text": "Άνοιγμα συνδέσμου \"{url}\" σε πρόγραμμα περιήγησης;",

    "load_file_encryption_password_mismatch": "Αναντιστοιχία κωδικού κρυπτογράφησης!",
    "load_file_encryption_password_incorrect": "Λάθος κωδικός κρυπτογράφησης!",
    "load_file_none_content_error": "Το αρχείο δεν μπορεί να φορτωθεί.",

    "save_active_file_error_occurred": "Αδυναμία αποθήκευσης αρχείου, συνέβη σφάλμα",

    "expandable_block_default_title": "Περισσότερες πληροφορίες...",

    "dialog_color_picker_color_copied_to_the_clipboard": "Το μορφοποιημένο κείμενο έχει αντιγραφεί στο πρόχειρο",

    "popup_about_title": "Πληροφορίες Εφαρμογής",
    "popup_about_app_name_description": "Επεξεργαστής Markdown της Python",

    "popup_about_version": "Έκδοση",
    "popup_about_license": "Άδεια",
    "popup_about_website": "Ιστοσελίδα",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Ημερομηνία",

    "update_helper_new_version_is_available": "Μια νέα έκδοση '{latest_version}' της εφαρμογής είναι διαθέσιμη",
    "update_helper_latest_version_installed": "Η τελευταία έκδοση της εφαρμογής είναι εγκατεστημένη",

    "network_connection_error_empty": "Δεν είναι δυνατή η λήψη πληροφοριών απόκρισης",
    "network_connection_error_connection_or_dns":
        "Ο ξενιστής δεν βρέθηκε. Μπορεί να υπάρχει ένα ζήτημα με τη σύνδεση στο διαδίκτυο ή DNS.",
    "network_connection_error_connection_refused":
        "Η σύνδεση απορρίφθηκε. Μπορεί ο διακομιστής να είναι κάτω, ή μπορεί να υπάρχουν ζητήματα δικτύου.",
    "network_connection_error_connection_timed_out": "Η σύνδεση έληξε. Μπορεί να υπάρχουν ζητήματα δικτύου.",
    "network_connection_error_connection_404_error":
        "Σφάλμα 404 σύνδεσης. Η ζητούμενη σελίδα ή πόρος δεν βρέθηκε.",
    "network_connection_error_generic_with_status_code": "Η αίτηση απέτυχε με κωδικό κατάστασης: {status_code}",
}
