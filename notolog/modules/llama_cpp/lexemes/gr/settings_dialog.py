# Greek lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Μονάδα llama.cpp",

    "module_llama_cpp_config_label": "Μονάδα llama.cpp",
    "module_llama_cpp_config_path_label": "Τοποθεσία Μοντέλου",
    "module_llama_cpp_config_path_input_placeholder_text": "Επιλέξτε ή εισάγετε τη διαδρομή του μοντέλου",
    "module_llama_cpp_config_path_input_accessible_description":
        "Ένα πεδίο εισόδου με επιλογέα για να καθορίσετε την τοποθεσία του τοπικού μοντέλου.\n"
        "Υποστηρίζει μοντέλα σε μορφή GGUF, μια δυαδική μορφή αρχείου βελτιστοποιημένη για την\n"
        "αποθήκευση μοντέλων που χρησιμοποιούνται με GGML και εκτελεστές βασισμένους σε GGML.",
    "module_llama_cpp_config_path_input_filter_text": "Αρχεία GGUF",

    "module_llama_cpp_config_context_window_label": "Μέγεθος Παραθύρου Πλαισίου",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Καθορίζει τον αριθμό των tokens που λαμβάνει υπόψη το μοντέλο για τη δημιουργία απαντήσεων.\n"
        "Ελέγχει πόσο προηγούμενο πλαίσιο χρησιμοποιείται.",

    "module_llama_cpp_config_chat_formats_label": "Μορφές Συνομιλίας",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Επιλέξτε μια μορφή συνομιλίας",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Μενού dropdown για την επιλογή της μορφής που χρησιμοποιείται για τις συνομιλίες μοντέλων.",

    "module_llama_cpp_config_system_prompt_label": "Προτροπή Συστήματος",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Εισάγετε κείμενο προτροπής συστήματος",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Πεδίο κειμένου για την εισαγωγή προτροπών συστήματος που καθοδηγούν τις απαντήσεις του μοντέλου.",

    "module_llama_cpp_config_response_temperature_label": "Θερμοκρασία Απάντησης: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Ρυθμίζει την τυχαιότητα των απαντήσεων του μοντέλου. Υψηλότερες τιμές παράγουν πιο ποικίλες εξόδους,\n"
        "ενώ χαμηλότερες τιμές οδηγούν σε πιο προβλέψιμες απαντήσεις.",

    "module_llama_cpp_config_response_max_tokens_label": "Μέγιστοι Tokens ανά Απάντηση",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Περιορίζει τον αριθμό των tokens στις απαντήσεις του μοντέλου μέχρι το πραγματικό όριο του παραθύρου πλαισίου.\n"
        "Μηδενική τιμή υποθέτει τη χωρητικότητα του παραθύρου πλαισίου.",

    "module_llama_cpp_config_prompt_history_size_label": "Μέγεθος Ιστορικού Προτροπών",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Ελέγχει τον αριθμό των καταχωρήσεων στο ιστορικό προτροπών που διατηρούνται από το σύστημα για αναφορά.\n"
        "Μηδενική τιμή επιτρέπει απεριόριστες καταχωρήσεις."
}
