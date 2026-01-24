# Italian lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM su Dispositivo",

    "module_ondevice_llm_config_label": "Modello LLM su Dispositivo",
    "module_ondevice_llm_config_path_label": "Posizione del Modello ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Percorso della directory del modello",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Un campo di input con un selettore per specificare il percorso della directory del modello dove si trovano\n"
        "i file ONNX. I modelli supportati sono nel formato ONNX, che sta per Open Neural Network Exchange,\n"
        "uno standard aperto per i formati dei modelli di apprendimento automatico.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatura: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Regola la casualità delle risposte del modello. Valori più alti producono output più variati,\n"
        "mentre valori più bassi rendono le risposte più prevedibili.",

    "module_ondevice_llm_config_response_max_tokens_label": "Massimo di Token per Risposta",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Imposta il numero massimo di token da ricevere in una risposta, come parole e punteggiatura,\n"
        "controllando la lunghezza dell'output.",

    "module_ondevice_llm_config_execution_provider_label": "Accelerazione Hardware",
    "module_ondevice_llm_config_execution_provider_placeholder": "Seleziona provider",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Seleziona il provider di accelerazione hardware per l'inferenza del modello. "
        "Le opzioni includono:\n"
        "CPU (predefinito), CUDA (GPU NVIDIA), DirectML (Windows), TensorRT, OpenVINO (Intel), "
        "QNN (Qualcomm), CoreML (Apple).\n"
        "Nota: I provider non-CPU richiedono pacchetti ONNX Runtime specifici "
        "(es: onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Dimensione della Cronologia dei Prompt",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Controlla il numero di voci nella cronologia dei prompt che il sistema conserva per riferimento.\n"
        "Un valore zero consente un numero illimitato di voci."
}
