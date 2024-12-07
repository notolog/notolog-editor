# Greek lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "URL του API",
    "module_openai_api_url_input_placeholder_text": "URL του API",
    "module_openai_api_url_input_accessible_description":
        "Το URL του API της OpenAI είναι η διεύθυνση του τελικού σημείου του API, το οποίο μπορεί να διαφέρει\n"
        "ανάλογα με την υπηρεσία και την έκδοση. Ο Βοηθός AI χρησιμοποιεί αυτό για συνομιλίες ή συμπληρώσεις κειμένου.\n"
        "Ανατρέξτε στην επίσημη τεκμηρίωση του API της OpenAI για να αποκτήσετε το τρέχον URL.",
    "module_openai_api_key_label": "Κλειδί API",
    "module_openai_api_key_input_placeholder_text": "Κλειδί API",
    "module_openai_api_key_input_accessible_description":
        "Το κλειδί API της OpenAI είναι ένα μυστικό διακριτικό που χρησιμοποιείται για τον έλεγχο ταυτότητας αιτημάτων\n"
        "στο τελικό σημείο του API.",
    "module_openai_api_supported_models_label": "Υποστηριζόμενα Μοντέλα",
    "module_openai_api_model_names_combo_placeholder_text": "Επιλέξτε ένα Μοντέλο",
    "module_openai_api_model_names_combo_accessible_description":
        "Επιλέξτε από τα υποστηριζόμενα μοντέλα για συζητήσεις συνομιλίας.",

    "module_openai_api_base_system_prompt_label": "Σύστημα Προτροπής",
    "module_openai_api_base_system_prompt_edit_placeholder_text":
        "Βασική προτροπή συστήματος που προηγείται κάθε αιτήματος",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Βασική προτροπή συστήματος που προηγείται κάθε αιτήματος.\n"
        "Συνήθως απλό κείμενο με οδηγίες ή χαρακτηριστικά ρόλου.",

    "module_openai_api_base_response_temperature_label": "Θερμοκρασία: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Ρυθμίζει την τυχαιότητα των αποκρίσεων του μοντέλου. Υψηλότερες τιμές παράγουν πιο ποικίλες εξόδους, "
        "ενώ χαμηλότερες τιμές καθιστούν τις αποκρίσεις πιο προβλέψιμες.",

    "module_openai_api_base_response_max_tokens_label": "Μέγιστος αριθμός tokens ανά απόκριση",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Ο μέγιστος αριθμός tokens που λαμβάνονται σε μια απόκριση, όπως λέξεις και στίξη, "
        "διαχειρίζοντας το μήκος της εξόδου.",

    "module_openai_api_config_prompt_history_size_label": "Μέγεθος Ιστορικού Προτροπών",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Ελέγχει τον αριθμό των καταχωρήσεων στο ιστορικό προτροπών που διατηρεί το σύστημα για αναφορά.\n"
        "Μια τιμή μηδέν επιτρέπει απεριόριστες καταχωρήσεις."
}
