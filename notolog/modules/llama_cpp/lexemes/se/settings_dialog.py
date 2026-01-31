# Swedish lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Modul llama.cpp",

    "module_llama_cpp_config_label": "Modul llama.cpp",
    "module_llama_cpp_config_path_label": "Modellplats",
    "module_llama_cpp_config_path_input_placeholder_text": "Välj eller ange modellens sökväg",
    "module_llama_cpp_config_path_input_accessible_description":
        "Ett inmatningsfält med en väljare för att specificera sökvägen för den lokala modellen.\n"
        "Stöder modeller i GGUF-format, ett binärt filformat optimerat för att lagra\n"
        "modeller som används med GGML och GGML-baserade verkställare.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF-filer",

    "module_llama_cpp_config_context_window_label": "Kontextfönstrets storlek",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Anger antalet tokens som modellen överväger för att generera svar.\n"
        "Kontrollerar hur mycket tidigare kontext som används.",

    "module_llama_cpp_config_chat_formats_label": "Chatformat",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Välj ett chattformat",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Dropdown-menyn för att välja formatet som används för modellsamtal.",

    "module_llama_cpp_config_gpu_layers_label": "GPU-lager",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "Antal modelllager att avlasta till GPU.\n"
        "Auto: Automatisk detektering (GPU på Apple Silicon, CPU annars).\n"
        "-1: Avlasta alla lager till GPU.\n"
        "0: Endast CPU-läge (rekommenderas för Intel Macs).\n"
        "1-999: Delvis GPU-avlastning (avancerat).",

    "module_llama_cpp_config_system_prompt_label": "Systemprompt",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Ange text för systemprompten",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Textfält för att ange systemprompter som styr modellens svar.",

    "module_llama_cpp_config_response_temperature_label": "Svarstemperatur: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Justerar modellens svars slumpmässighet. Högre värden producerar mer varierade utdata,\n"
        "medan lägre värden resulterar i mer förutsägbara svar.",

    "module_llama_cpp_config_response_max_tokens_label": "Maximalt antal tokens per svar",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Begränsar antalet tokens i modellens svar till den faktiska gränsen för kontextfönstret.\n"
        "Ett värde på noll antar kapaciteten för kontextfönstret.",

    "module_llama_cpp_config_prompt_history_size_label": "Storleken på promptens historia",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Kontrollerar antalet poster i promptens historik som systemet behåller för referens.\n"
        "Ett värde på noll tillåter obegränsat antal poster."
}
