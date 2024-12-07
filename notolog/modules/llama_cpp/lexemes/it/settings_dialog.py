# Italian lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Modulo llama.cpp",

    "module_llama_cpp_config_label": "Modulo llama.cpp",
    "module_llama_cpp_config_path_label": "Posizione del modello",
    "module_llama_cpp_config_path_input_placeholder_text": "Seleziona o inserisci il percorso del modello",
    "module_llama_cpp_config_path_input_accessible_description":
        "Un campo di inserimento con un selettore per specificare il percorso del modello locale. Supporta\n"
        "modelli nel formato GGUF, un formato di file binario ottimizzato per l'archiviazione di modelli\n"
        "utilizzati con GGML e esecutori basati su GGML.",
    "module_llama_cpp_config_path_input_filter_text": "File GGUF",

    "module_llama_cpp_config_context_window_label": "Dimensione della finestra di contesto",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Imposta il numero di token che il modello considera per generare risposte.\n"
        "Controlla quanta contestazione precedente viene utilizzata.",

    "module_llama_cpp_chat_formats_label": "Formati di chat",
    "module_llama_cpp_chat_formats_combo_placeholder_text": "Seleziona un formato di chat",
    "module_llama_cpp_chat_formats_combo_accessible_description":
        "Menu a tendina per selezionare il formato utilizzato per le conversazioni del modello.",

    "module_llama_cpp_config_system_prompt_label": "Prompt del sistema",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Inserisci il testo del prompt del sistema",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Campo di testo per inserire i prompt del sistema che guidano le risposte del modello.",

    "module_llama_cpp_config_response_temperature_label": "Temperatura di risposta: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Regola la casualità delle risposte del modello. Valori più alti producono output più variati,\n"
        "mentre valori più bassi risultano in risposte più prevedibili.",

    "module_llama_cpp_config_response_max_tokens_label": "Token massimi per risposta",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Limita il numero di token nelle risposte del modello fino al limite effettivo della finestra di contesto.\n"
        "Un valore zero assume la capacità della finestra di contesto.",

    "module_llama_cpp_config_prompt_history_size_label": "Dimensione della cronologia dei prompt",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Controlla il numero di voci nella cronologia dei prompt mantenute dal sistema per riferimento.\n"
        "Un valore zero permette voci illimitate."
}
