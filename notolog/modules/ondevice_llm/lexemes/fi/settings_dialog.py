# Finnish lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "Laitteessa LLM",

    "module_ondevice_llm_config_label": "Laitteessa LLM Malli",
    "module_ondevice_llm_config_path_label": "ONNX-mallin sijainti",
    "module_ondevice_llm_config_path_input_placeholder_text": "Polku mallihakemistoon",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Syöttökenttä valitsimella, joka määrittää polun mallihakemistoon, jossa ONNX-tiedostot sijaitsevat.\n"
        "Tuetut mallit ovat ONNX-muodossa, joka tarkoittaa Open Neural Network Exchange - avointa standardia\n"
        "koneoppimismallien formaatille.",

    "module_ondevice_llm_config_response_temperature_label": "Lämpötila: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Säätää mallin vastausten satunnaisuutta. Korkeammat arvot tuottavat monimuotoisempia tulosteita,\n"
        "kun taas matalammat arvot tekevät vastauksista ennustettavampia.",

    "module_ondevice_llm_config_response_max_tokens_label": "Enimmäismäärä vastausmerkkejä",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Määrittää vastaanotettavien merkkien enimmäismäärän vastauksessa, kuten sanat ja välimerkit,\n"
        "hallitsemalla tulosteen pituutta.",

    "module_ondevice_llm_config_prompt_history_size_label": "Kehotushistorian koko",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Hallitsee järjestelmän säilyttämien kehotushistorian merkintöjen määrää viitteitä varten.\n"
        "Nolla-arvo sallii rajattomat merkinnät."
}
