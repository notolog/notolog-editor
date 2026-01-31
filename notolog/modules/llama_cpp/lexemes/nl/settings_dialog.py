# Dutch lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Module llama.cpp",

    "module_llama_cpp_config_label": "Module llama.cpp",
    "module_llama_cpp_config_path_label": "Modellocatie",
    "module_llama_cpp_config_path_input_placeholder_text": "Selecteer of voer het modelpad in",
    "module_llama_cpp_config_path_input_accessible_description":
        "Een invoerveld met een selector om het pad van het lokale model op te geven.\n"
        "Ondersteunt modellen in GGUF-formaat, een binair bestandsformaat geoptimaliseerd\n"
        "voor het opslaan van modellen gebruikt met GGML en GGML-gebaseerde uitvoerders.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF-bestanden",

    "module_llama_cpp_config_context_window_label": "Grootte van het contextvenster",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Stelt het aantal tokens in dat het model overweegt bij het genereren van reacties.\n"
        "Beheert hoeveel voorgaande context wordt gebruikt.",

    "module_llama_cpp_config_chat_formats_label": "Chatformaten",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Selecteer een chatformaat",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Dropdownmenu om het formaat te selecteren dat gebruikt wordt voor modelgesprekken.",

    "module_llama_cpp_config_gpu_layers_label": "GPU-lagen",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "Aantal modellagen om naar de GPU te offloaden.\n"
        "Auto: Automatische detectie (GPU op Apple Silicon, CPU elders).\n"
        "-1: Alle lagen naar GPU offloaden.\n"
        "0: Alleen CPU-modus (aanbevolen voor Intel Macs).\n"
        "1-999: Gedeeltelijke GPU-offloading (geavanceerd).",

    "module_llama_cpp_config_system_prompt_label": "Systeemprompt",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Voer de tekst voor de systeemprompt in",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Tekstveld voor het invoeren van systeemprompts die modelreacties sturen.",

    "module_llama_cpp_config_response_temperature_label": "Respons Temperatuur: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Past de willekeurigheid van de modelreacties aan. Hogere waarden produceren gevarieerdere outputs,\n"
        "terwijl lagere waarden leiden tot voorspelbaardere reacties.",

    "module_llama_cpp_config_response_max_tokens_label": "Maximale Tokens per Reactie",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Beperkt het aantal tokens in de reacties van het model tot aan de daadwerkelijke limiet van het contextvenster.\n"
        "Een waarde van nul neemt de capaciteit van het contextvenster aan.",

    "module_llama_cpp_config_prompt_history_size_label": "Grootte van de Promptgeschiedenis",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Beheert het aantal invoeringen in de promptgeschiedenis die door het systeem worden bewaard voor referentie.\n"
        "Een waarde van nul staat een onbeperkt aantal invoeringen toe."
}
