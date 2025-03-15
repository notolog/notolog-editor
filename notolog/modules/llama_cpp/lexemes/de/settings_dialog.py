# German lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Modul llama.cpp",

    "module_llama_cpp_config_label": "Modul llama.cpp",
    "module_llama_cpp_config_path_label": "Modellstandort",
    "module_llama_cpp_config_path_input_placeholder_text": "Modellpfad auswählen oder eingeben",
    "module_llama_cpp_config_path_input_accessible_description":
        "Ein Eingabefeld mit einem Selektor, um den Pfad des lokalen Modells anzugeben.\n"
        "Unterstützt Modelle im GGUF-Format, ein binäres Dateiformat,\n"
        "optimiert zur Speicherung von Modellen, die mit GGML und GGML-basierten Ausführern verwendet werden.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF-Dateien",

    "module_llama_cpp_config_context_window_label": "Kontextfenstergröße",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Legt die Anzahl der Tokens fest, die das Modell für die Erzeugung von Antworten berücksichtigt.\n"
        "Steuert, wie viel vorheriger Kontext verwendet wird.",

    "module_llama_cpp_config_chat_formats_label": "Chat-Formate",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Chat-Format auswählen",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Dropdown-Menü zur Auswahl des Formats, das für Modellgespräche verwendet wird.",

    "module_llama_cpp_config_system_prompt_label": "Systemaufforderung",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Systemaufforderungstext eingeben",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Textfeld für das Eingeben von Systemaufforderungen, die die Modellantworten leiten.",

    "module_llama_cpp_config_response_temperature_label": "Antworttemperatur: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Passt die Zufälligkeit der Modellantworten an. Höhere Werte erzeugen variablere Ausgaben,\n"
        "während niedrigere Werte zu vorhersehbareren Antworten führen.",

    "module_llama_cpp_config_response_max_tokens_label": "Maximale Tokenanzahl pro Antwort",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Begrenzt die Anzahl der Tokens in den Modellantworten bis zur tatsächlichen Grenze des Kontextfensters.\n"
        "Ein Wert von null nimmt die Kapazität des Kontextfensters an.",

    "module_llama_cpp_config_prompt_history_size_label": "Größe des Aufforderungsverlaufs",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Steuer die Anzahl der Einträge im Aufforderungsverlauf, die vom System zur Referenz aufbewahrt werden.\n"
        "Ein Wert von null erlaubt eine unbegrenzte Anzahl von Einträgen."
}
