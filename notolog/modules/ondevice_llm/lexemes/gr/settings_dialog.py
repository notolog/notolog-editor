# Greek lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM στη Συσκευή",

    "module_ondevice_llm_config_label": "Μοντέλο LLM στη Συσκευή",
    "module_ondevice_llm_config_path_label": "Τοποθεσία Μοντέλου ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Διαδρομή προς τον κατάλογο του μοντέλου",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Ένα πεδίο εισόδου με επιλογέα για να καθορίσετε την τοποθεσία του καταλόγου του μοντέλου όπου βρίσκονται\n"
        "τα αρχεία ONNX. Τα υποστηριζόμενα μοντέλα είναι σε μορφή ONNX, το οποίο αντιπροσωπεύει το Open Neural\n"
        "Network Exchange, ένα ανοιχτό πρότυπο για τα φορμάτ των μοντέλων μηχανικής μάθησης.",

    "module_ondevice_llm_config_response_temperature_label": "Θερμοκρασία: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Ρυθμίζει την τυχαιότητα των απαντήσεων του μοντέλου. Υψηλότερες τιμές παράγουν πιο ποικίλες εξόδους,\n"
        "ενώ χαμηλότερες τιμές καθιστούν τις απαντήσεις πιο προβλέψιμες.",

    "module_ondevice_llm_config_response_max_tokens_label": "Μέγιστος Αριθμός Tokens Ανά Απάντηση",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Ορίζει τον μέγιστο αριθμό των tokens που μπορούν να ληφθούν σε μία απάντηση, όπως λέξεις και σημεία στίξης,\n"
        "ελέγχοντας το μήκος της απόκρισης.",

    "module_ondevice_llm_config_prompt_history_size_label": "Μέγεθος Ιστορικού Προτροπών",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Ελέγχει τον αριθμό των καταχωρήσεων στο ιστορικό προτροπών που διατηρεί το σύστημα για αναφορά.\n"
        "Μια τιμή μηδέν επιτρέπει απεριόριστες καταχωρήσεις."
}
