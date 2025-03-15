# Finnish lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Moduuli llama.cpp",

    "module_llama_cpp_config_label": "Moduuli llama.cpp",
    "module_llama_cpp_config_path_label": "Mallin sijainti",
    "module_llama_cpp_config_path_input_placeholder_text": "Valitse tai syötä mallin polku",
    "module_llama_cpp_config_path_input_accessible_description":
        "Syöttökenttä valitsimella paikallisen mallin polun määrittämiseen. Tukee GGUF-muodossa olevia malleja,\n"
        "binääritiedostomuotoa, joka on optimoitu mallien tallentamiseen GGML:n ja GGML-pohjaisten suorittimien kanssa.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF-tiedostot",

    "module_llama_cpp_config_context_window_label": "Konteksti-ikkunan koko",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Asettaa tokenien määrän, jota malli harkitsee vastauksia tuottaessaan.\n"
        "Hallitsee kuinka paljon aiempaa kontekstia käytetään.",

    "module_llama_cpp_config_chat_formats_label": "Keskustelumuodot",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Valitse keskustelumuoto",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Pudotusvalikko mallikeskustelujen muodon valitsemiseksi.",

    "module_llama_cpp_config_system_prompt_label": "Järjestelmäkehotus",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Syötä järjestelmäkehotuksen teksti",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Tekstikenttä järjestelmäkehotuksien syöttämiseen, jotka ohjaavat mallin vastauksia.",

    "module_llama_cpp_config_response_temperature_label": "Vastauslämpötila: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Säätää mallin vastausten satunnaisuutta. Korkeammat arvot tuottavat monipuolisempia tulosteita,\n"
        "kun taas alhaisemmat arvot johtavat ennustettavampiin vastauksiin.",

    "module_llama_cpp_config_response_max_tokens_label": "Maksimitokenit vastauksessa",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Rajoittaa mallin vastauksissa olevien tokenien määrää aina todelliseen konteksti-ikkunan rajaan asti.\n"
        "Nolla-arvo olettaa konteksti-ikkunan kapasiteetin.",

    "module_llama_cpp_config_prompt_history_size_label": "Kehotushistorian koko",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Hallitsee järjestelmän säilyttämien kehotushistorian merkintöjen määrää viitteitä varten.\n"
        "Nolla-arvo sallii rajattoman määrän merkintöjä."
}
