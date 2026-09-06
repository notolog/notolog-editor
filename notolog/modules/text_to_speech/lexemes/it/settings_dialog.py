# Italian lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Abilita sintesi vocale",
    "module_text_to_speech_config_setup_label": "Configurazione voce",
    "module_text_to_speech_config_runtime_label": "Motore vocale",
    "module_text_to_speech_config_model_directory_label": "Cartella modelli",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizzatori",
    "module_text_to_speech_config_details_label": "Dettagli",
    "module_text_to_speech_config_model_license_label": "Licenza del modello",
    "module_text_to_speech_config_download_models_button": "Scarica modelli",
    "module_text_to_speech_config_verify_models_button": "Verifica modelli",
    "module_text_to_speech_config_cancel_button": "Annulla",
    "module_text_to_speech_config_stop_button": "Interrompi",
    "module_text_to_speech_config_custom_models_label": "File di modello personalizzati",
    "module_text_to_speech_config_reading_label": "Lettura",
    "module_text_to_speech_config_language_label": "Lingua",
    "module_text_to_speech_config_voice_label": "Voce",
    "module_text_to_speech_config_speed_label": "Velocità",
    "module_text_to_speech_config_announce_headings_label": "Annuncia intestazioni",
    "module_text_to_speech_config_skip_inline_code_label": "Salta codice in linea",
    "module_text_to_speech_config_skip_multiline_code_label": "Salta codice multilinea",
    "module_text_to_speech_config_test_voice_button": "Prova voce",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Seleziona eseguibile…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatico",
    "module_text_to_speech_config_get_runtime_link": "Ottieni motore {version}",
    "module_text_to_speech_config_about_label": "Informazioni su {title}",
    "module_text_to_speech_config_choose_path_label": "Scegli {title}",
    "module_text_to_speech_config_status_checking_runtime": "Verifica motore vocale…",
    "module_text_to_speech_config_status_checking_models": "Verifica file nella cache e download dei modelli mancanti…",
    "module_text_to_speech_config_status_models_verified": "Modelli esistenti verificati. Pronto per leggere.",
    "module_text_to_speech_config_status_models_downloaded": "Modelli scaricati e verificati. Pronto per leggere.",
    "module_text_to_speech_config_status_models_found": "Modelli trovati. Verificali o prova la voce.",
    "module_text_to_speech_config_status_models_missing": "Modelli mancanti. Scarica la voce per iniziare.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Motore richiesto. Seleziona un eseguibile oppure scarica il motore."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Annullato. I download completati sono conservati; riprova per continuare."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Permesso negato. Scegli una cartella modelli scrivibile e controlla l’accesso."
    ),
    "module_text_to_speech_config_error_file_access": "Accesso al file non riuscito: {error}. Vedi Dettagli.",
    "module_text_to_speech_config_progress_elapsed": "{time} trascorsi",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 file completati",
    "module_text_to_speech_config_progress_downloading": "File {number}/3 · Download di {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 file di modello verificati nella cache…",
    "module_text_to_speech_config_progress_verifying": "File {number}/3 · Verifica download…",
    "module_text_to_speech_config_download_role_voice": "modello vocale",
    "module_text_to_speech_config_download_role_codec": "decodificatore audio",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizzatori",
    "module_text_to_speech_config_download_role_model": "modello",
    "module_text_to_speech_config_runtime_required": "Seleziona prima un motore vocale.",
    "module_text_to_speech_config_models_required": "Scarica prima i modelli.",
    "module_text_to_speech_config_enable_required": "Abilita prima la sintesi vocale.",
    "module_text_to_speech_config_status_testing_voice": "Caricamento modelli e preparazione della voce di prova…",
    "module_text_to_speech_config_details_accessible_description": "Mostra o nascondi il registro",
    "module_text_to_speech_config_setup_accessible_description": (
        "Seleziona NeMo-Speech.cpp e scarica MagpieTTS, NanoCodec e i tokenizzatori. I modelli hanno una"
        " licenza separata."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Richiede NeMo-Speech.cpp 0.1.0. Estrai l’archivio e seleziona bin/nemo-speech "
        "(bin/nemo-speech.exe su Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "I modelli vengono scaricati qui. I file esistenti sono verificati e riutilizzati. Richiede curl"
        " e circa 550 MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Sostituisci i percorsi dei modelli o svuota i campi per usare la cartella modelli."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Scegli voce, lingua e velocità. Il codice può essere sostituito da una breve etichetta vocale."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Scegli la lingua del documento; non viene rilevata automaticamente. Predefinita: inglese. "
        "Mandarino e giapponese richiedono un motore compatibile."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Voci MagpieTTS: John, Sofia, Aria, Jason e Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "La velocità di riproduzione modifica anche l’altezza della voce."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Annuncia Chapter, Section, Subsection e Sub-subsection per intestazioni Markdown e HTML di "
        "livello 1–4, poi Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Selezionato: dice «Inline code block». Deselezionato: legge il codice in linea. Il codice "
        "delimitato o rientrato usa l’opzione multilinea."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Selezionato: dice «Multiline code block». Deselezionato: legge il codice delimitato o "
        "rientrato."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Verifica i file esistenti e scarica quelli mancanti o danneggiati."
    ),
    "module_text_to_speech_config_editor_required": "Apri queste impostazioni dall’editor per provare la voce.",
    "module_text_to_speech_config_context_length_label": "Lunghezza contesto",
    "module_text_to_speech_config_context_whole_document": "Intero documento",
    "module_text_to_speech_config_context_characters": "{count} caratteri",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Caratteri massimi per richiesta vocale. A destra: intero documento, con pause ai titoli. "
        "Contesti più ampi richiedono più tempo iniziale e memoria. Restano validi i limiti del motore."
    ),
    "module_text_to_speech_config_cancel_download_title": "Annullare il download?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Chiudendo le impostazioni si annulla il download. I file completati vengono conservati. "
        "Chiudere le impostazioni?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Sono selezionati file di modello personalizzati. I download usano la cartella dei modelli."
    ),
}
