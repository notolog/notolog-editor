# German lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM auf dem Gerät",

    "module_ondevice_llm_config_label": "LLM-Modell auf dem Gerät",
    "module_ondevice_llm_config_path_label": "ONNX Modellstandort",
    "module_ondevice_llm_config_path_input_placeholder_text": "Pfad zum Modellverzeichnis",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Ein Eingabefeld mit einem Selektor, um den Pfad zum Modellverzeichnis anzugeben, wo sich die ONNX-Dateien\n"
        "befinden. Unterstützte Modelle sind im ONNX-Format, welches für Open Neural Network Exchange steht,\n"
        "einem offenen Standard für Formate von maschinellem Lernmodellen.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatur: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Passt die Zufälligkeit der Modellantworten an. Höhere Werte erzeugen vielfältigere Ausgaben,\n"
        "während niedrigere Werte die Antworten vorhersehbarer machen.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maximale Anzahl von Antwort-Tokens",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Legt die maximale Anzahl von Tokens fest, die in einer Antwort erhalten werden können,\n"
        "einschließlich Wörter und Zeichensetzung, und steuert die Länge der Ausgabe.",

    "module_ondevice_llm_config_execution_provider_label": "Hardwarebeschleunigung",
    "module_ondevice_llm_config_execution_provider_placeholder": "Anbieter auswählen",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Wählen Sie den Hardwarebeschleunigungsanbieter für die Modellinferenz. Optionen umfassen:\n"
        "CPU (Standard), CUDA (NVIDIA GPUs), DirectML (Windows), TensorRT, OpenVINO (Intel), QNN (Qualcomm), CoreML (Apple).\n"
        "Hinweis: Nicht-CPU-Anbieter erfordern spezifische ONNX Runtime-Pakete (z.B. onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Größe des Prompt-Verlaufs",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Regelt die Anzahl der Einträge im Prompt-Verlauf, die das System zur Referenz behält.\n"
        "Ein Wert von Null erlaubt unbegrenzte Einträge."
}
