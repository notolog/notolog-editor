# Dutch lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "On Device LLM",

    "module_ondevice_llm_config_label": "On Device LLM Model",
    "module_ondevice_llm_config_path_label": "ONNX Model Locatie",
    "module_ondevice_llm_config_path_input_placeholder_text": "Pad naar de modeldirectory",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Een invoerveld met een selector om het pad naar de modeldirectory te specificeren waar ONNX-bestanden zich\n"
        "bevinden. Ondersteunde modellen zijn in het ONNX-formaat, wat staat voor Open Neural Network Exchange,\n"
        "een open standaard formaat voor machineleermodellen.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatuur: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Past de willekeurigheid van de modelreacties aan. Hogere waarden produceren gevarieerdere outputs,\n"
        "terwijl lagere waarden reacties voorspelbaarder maken.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maximale Respons Tokens",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Stelt het maximale aantal tokens in dat in een reactie ontvangen kan worden, zoals woorden en interpunctie,\n"
        "en beheert de lengte van de output.",

    "module_ondevice_llm_config_execution_provider_label": "Hardwareversnelling",
    "module_ondevice_llm_config_execution_provider_placeholder": "Selecteer provider",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Selecteer de hardwareversnellingsprovider voor modelinferentie. Opties zijn:\n"
        "CPU (standaard), CUDA (NVIDIA GPU's), DirectML (Windows), TensorRT, OpenVINO (Intel), "
        "QNN (Qualcomm), CoreML (Apple).\n"
        "Opmerking: Niet-CPU providers vereisen specifieke ONNX Runtime-pakketten "
        "(bijv. onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Grootte van de Promptgeschiedenis",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Regelt het aantal invoeren in de promptgeschiedenis dat het systeem bewaart voor referentie.\n"
        "Een waarde van nul staat een onbeperkt aantal invoeren toe."
}
