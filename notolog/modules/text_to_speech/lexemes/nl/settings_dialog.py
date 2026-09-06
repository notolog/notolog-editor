# Dutch lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Tekst-naar-spraak inschakelen",
    "module_text_to_speech_config_setup_label": "Stem instellen",
    "module_text_to_speech_config_runtime_label": "Spraakruntime",
    "module_text_to_speech_config_model_directory_label": "Modelmap",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizers",
    "module_text_to_speech_config_details_label": "Details",
    "module_text_to_speech_config_model_license_label": "Modellicentie",
    "module_text_to_speech_config_download_models_button": "Modellen downloaden",
    "module_text_to_speech_config_verify_models_button": "Modellen controleren",
    "module_text_to_speech_config_cancel_button": "Annuleren",
    "module_text_to_speech_config_stop_button": "Stoppen",
    "module_text_to_speech_config_custom_models_label": "Aangepaste modelbestanden",
    "module_text_to_speech_config_reading_label": "Voorlezen",
    "module_text_to_speech_config_language_label": "Taal",
    "module_text_to_speech_config_voice_label": "Stem",
    "module_text_to_speech_config_speed_label": "Snelheid",
    "module_text_to_speech_config_announce_headings_label": "Koppen aankondigen",
    "module_text_to_speech_config_skip_inline_code_label": "Inlinecode overslaan",
    "module_text_to_speech_config_skip_multiline_code_label": "Meerregelige code overslaan",
    "module_text_to_speech_config_test_voice_button": "Stem testen",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Uitvoerbaar bestand kiezen…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatisch",
    "module_text_to_speech_config_get_runtime_link": "Runtime {version} ophalen",
    "module_text_to_speech_config_about_label": "Over {title}",
    "module_text_to_speech_config_choose_path_label": "{title} kiezen",
    "module_text_to_speech_config_status_checking_runtime": "Spraakruntime controleren…",
    "module_text_to_speech_config_status_checking_models": "Cache controleren en ontbrekende modellen downloaden…",
    "module_text_to_speech_config_status_models_verified": "Bestaande modellen gecontroleerd. Klaar om voor te lezen.",
    "module_text_to_speech_config_status_models_downloaded": (
        "Modellen gedownload en gecontroleerd. Klaar om voor te lezen."
    ),
    "module_text_to_speech_config_status_models_found": "Modellen gevonden. Controleer ze of test de stem.",
    "module_text_to_speech_config_status_models_missing": "Modellen nodig. Download de stem om te beginnen.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Runtime vereist. Kies een uitvoerbaar bestand of haal de runtime op."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Geannuleerd. Voltooide downloads blijven bewaard; probeer opnieuw."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Toegang geweigerd. Kies een beschrijfbare modelmap en controleer de toegang."
    ),
    "module_text_to_speech_config_error_file_access": "Bestandstoegang mislukt: {error}. Zie Details.",
    "module_text_to_speech_config_progress_elapsed": "{time} verstreken",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 bestanden voltooid",
    "module_text_to_speech_config_progress_downloading": "Bestand {number}/3 · {role} downloaden · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 modelbestanden in cache gecontroleerd…",
    "module_text_to_speech_config_progress_verifying": "Bestand {number}/3 · Download controleren…",
    "module_text_to_speech_config_download_role_voice": "spraakmodel",
    "module_text_to_speech_config_download_role_codec": "audiodecoder",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizers",
    "module_text_to_speech_config_download_role_model": "model",
    "module_text_to_speech_config_runtime_required": "Kies eerst een spraakruntime.",
    "module_text_to_speech_config_models_required": "Download eerst de modellen.",
    "module_text_to_speech_config_enable_required": "Schakel eerst tekst-naar-spraak in.",
    "module_text_to_speech_config_status_testing_voice": "Modellen laden en teststem voorbereiden…",
    "module_text_to_speech_config_details_accessible_description": "Bewerkingslog tonen of verbergen",
    "module_text_to_speech_config_setup_accessible_description": (
        "Kies NeMo-Speech.cpp en download MagpieTTS, NanoCodec en tokenizers. Modellen hebben een aparte"
        " licentie."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "NeMo-Speech.cpp 0.1.0 is vereist. Pak het archief uit en kies bin/nemo-speech "
        "(bin/nemo-speech.exe op Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Modellen worden hier gedownload. Bestaande bestanden worden gecontroleerd en hergebruikt. "
        "Vereist curl en ongeveer 550 MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Vervang modelpaden of wis de velden om de modelmap te gebruiken."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Kies stem, taal en snelheid. Code kan worden vervangen door een kort gesproken label."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Kies de documenttaal; geen automatische detectie. Standaard Engels. Mandarijn en Japans "
        "vereisen een runtime met ondersteuning voor die talen."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS-stemmen: John, Sofia, Aria, Jason en Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "De afspeelsnelheid verandert ook de toonhoogte."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Zegt Chapter, Section, Subsection en Sub-subsection voor Markdown- en HTML-koppen 1–4, daarna "
        "Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Aangevinkt: zegt “Inline code block”. Anders wordt inlinecode voorgelezen. Afgebakende en "
        "ingesprongen code gebruikt de meerregelige instelling."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Aangevinkt: zegt “Multiline code block”. Anders wordt afgebakende en ingesprongen code "
        "voorgelezen."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Controleer bestaande bestanden en download ontbrekende of beschadigde bestanden."
    ),
    "module_text_to_speech_config_editor_required": "Open deze instellingen vanuit de editor om de stem te testen.",
    "module_text_to_speech_config_context_length_label": "Contextlengte",
    "module_text_to_speech_config_context_whole_document": "Heel document",
    "module_text_to_speech_config_context_characters": "{count} tekens",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Maximaal aantal tekens per spraakverzoek. Helemaal rechts: heel document, met pauzes bij "
        "koppen. Grotere contexten starten langzamer en gebruiken meer geheugen. De runtimelimieten "
        "blijven gelden."
    ),
    "module_text_to_speech_config_cancel_download_title": "Download annuleren?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Bij het sluiten van de instellingen wordt de download geannuleerd. Voltooide bestanden blijven "
        "bewaard. Instellingen sluiten?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Aangepaste modelbestanden zijn geselecteerd. Downloads gebruiken de modellenmap."
    ),
}
