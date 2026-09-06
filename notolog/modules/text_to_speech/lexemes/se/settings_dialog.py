# Swedish lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Aktivera text till tal",
    "module_text_to_speech_config_setup_label": "Röstinställningar",
    "module_text_to_speech_config_runtime_label": "Talmotor",
    "module_text_to_speech_config_model_directory_label": "Modellmapp",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokeniserare",
    "module_text_to_speech_config_details_label": "Detaljer",
    "module_text_to_speech_config_model_license_label": "Modelllicens",
    "module_text_to_speech_config_download_models_button": "Hämta modeller",
    "module_text_to_speech_config_verify_models_button": "Kontrollera modeller",
    "module_text_to_speech_config_cancel_button": "Avbryt",
    "module_text_to_speech_config_stop_button": "Stoppa",
    "module_text_to_speech_config_custom_models_label": "Egna modellfiler",
    "module_text_to_speech_config_reading_label": "Läsning",
    "module_text_to_speech_config_language_label": "Språk",
    "module_text_to_speech_config_voice_label": "Röst",
    "module_text_to_speech_config_speed_label": "Hastighet",
    "module_text_to_speech_config_announce_headings_label": "Annonsera rubriker",
    "module_text_to_speech_config_skip_inline_code_label": "Hoppa över kod i löptext",
    "module_text_to_speech_config_skip_multiline_code_label": "Hoppa över flerradig kod",
    "module_text_to_speech_config_test_voice_button": "Testa röst",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Välj körbar fil…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatiskt",
    "module_text_to_speech_config_get_runtime_link": "Hämta motor {version}",
    "module_text_to_speech_config_about_label": "Om {title}",
    "module_text_to_speech_config_choose_path_label": "Välj {title}",
    "module_text_to_speech_config_status_checking_runtime": "Kontrollerar talmotor…",
    "module_text_to_speech_config_status_checking_models": "Kontrollerar cache och hämtar saknade modeller…",
    "module_text_to_speech_config_status_models_verified": "Befintliga modeller kontrollerade. Redo att läsa.",
    "module_text_to_speech_config_status_models_downloaded": "Modeller hämtade och kontrollerade. Redo att läsa.",
    "module_text_to_speech_config_status_models_found": "Modellfiler hittades. Kontrollera dem eller testa rösten.",
    "module_text_to_speech_config_status_models_missing": "Modeller behövs. Hämta rösten för att börja.",
    "module_text_to_speech_config_status_runtime_missing": "Motor krävs. Välj en körbar fil eller hämta motorn.",
    "module_text_to_speech_config_status_download_cancelled": "Avbrutet. Slutförda hämtningar sparas; försök igen.",
    "module_text_to_speech_config_error_permission_denied": (
        "Åtkomst nekad. Välj en skrivbar modellmapp och kontrollera behörigheter."
    ),
    "module_text_to_speech_config_error_file_access": "Filåtkomst misslyckades: {error}. Se detaljer.",
    "module_text_to_speech_config_progress_elapsed": "{time} har gått",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 filer klara",
    "module_text_to_speech_config_progress_downloading": "Fil {number}/3 · Hämtar {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 modellfiler kontrollerade i cache…",
    "module_text_to_speech_config_progress_verifying": "Fil {number}/3 · Kontrollerar hämtning…",
    "module_text_to_speech_config_download_role_voice": "talmodell",
    "module_text_to_speech_config_download_role_codec": "ljudavkodare",
    "module_text_to_speech_config_download_role_tokenizers": "tokeniserare",
    "module_text_to_speech_config_download_role_model": "modell",
    "module_text_to_speech_config_runtime_required": "Välj en talmotor först.",
    "module_text_to_speech_config_models_required": "Hämta modellerna först.",
    "module_text_to_speech_config_enable_required": "Aktivera text till tal först.",
    "module_text_to_speech_config_status_testing_voice": "Läser in modeller och förbereder teströst…",
    "module_text_to_speech_config_details_accessible_description": "Visa eller dölj åtgärdslogg",
    "module_text_to_speech_config_setup_accessible_description": (
        "Välj NeMo-Speech.cpp och hämta MagpieTTS, NanoCodec och tokeniserare. Modellerna har en separat"
        " licens."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Kräver NeMo-Speech.cpp 0.1.0. Packa upp arkivet och välj bin/nemo-speech (bin/nemo-speech.exe i"
        " Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Modeller hämtas hit. Befintliga filer kontrolleras och återanvänds. Kräver curl och cirka 550 "
        "MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Ersätt modellsökvägar eller töm fälten för att använda modellmappen."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Välj röst, språk och hastighet. Kod kan ersättas med en kort talad etikett."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Välj dokumentets språk; det identifieras inte automatiskt. Engelska är standard. Mandarin och "
        "japanska kräver en motor med stöd för dessa språk."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS-röster: John, Sofia, Aria, Jason och Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": "Uppspelningshastigheten ändrar även tonhöjden.",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Säger Chapter, Section, Subsection och Sub-subsection för Markdown- och HTML-rubriker på nivå "
        "1–4, sedan Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Markerat: säger ”Inline code block”. Annars läses koden i löptext. Avgränsad och indragen kod "
        "använder inställningen för flerradig kod."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Markerat: säger ”Multiline code block”. Annars läses avgränsad och indragen kod."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Kontrollera befintliga filer och hämta saknade eller skadade filer."
    ),
    "module_text_to_speech_config_editor_required": "Öppna dessa inställningar från redigeraren för att testa rösten.",
    "module_text_to_speech_config_context_length_label": "Kontextlängd",
    "module_text_to_speech_config_context_whole_document": "Hela dokumentet",
    "module_text_to_speech_config_context_characters": "{count} tecken",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Högsta antal tecken per talbegäran. Längst till höger: hela dokumentet med rubrikpauser. Större"
        " kontext tar längre tid att starta och använder mer minne. Motorns gränser gäller fortfarande."
    ),
    "module_text_to_speech_config_cancel_download_title": "Avbryta hämtningen?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Om inställningarna stängs avbryts hämtningen. Färdiga filer behålls. Stäng inställningarna?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Anpassade modellfiler har valts. Hämtningar använder modellmappen."
    ),
}
