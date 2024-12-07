# Swedish lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM på Enhet",

    "module_ondevice_llm_config_label": "LLM-modell på Enhet",
    "module_ondevice_llm_config_path_label": "Plats för ONNX-modellen",
    "module_ondevice_llm_config_path_input_placeholder_text": "Sökväg till modellkatalogen",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Ett inmatningsfält med en väljare för att specificera sökvägen till modellkatalogen där ONNX-filerna finns.\n"
        "Stödda modeller är i ONNX-format, vilket står för Open Neural Network Exchange, en öppen standard\n"
        "för format på maskininlärningsmodeller.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatur: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Justerar slumpmässigheten i modellens svar. Högre värden producerar mer varierade utdata,\n"
        "medan lägre värden resulterar i mer förutsägbara svar.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maximalt antal tokens per svar",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Anger det maximala antalet tokens som kan tas emot i ett svar, inklusive ord och skiljetecken,\n"
        "och kontrollerar utdatans längd.",

    "module_ondevice_llm_config_prompt_history_size_label": "Storlek på prompt-historik",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Kontrollerar antalet poster i prompt-historiken som systemet behåller för referens.\n"
        "Ett värde på noll tillåter obegränsat antal poster."
}
