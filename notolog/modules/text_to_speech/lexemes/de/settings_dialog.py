# German lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Text zu Sprache aktivieren",
    "module_text_to_speech_config_setup_label": "Stimme einrichten",
    "module_text_to_speech_config_runtime_label": "Sprachlaufzeit",
    "module_text_to_speech_config_model_directory_label": "Modellordner",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizer",
    "module_text_to_speech_config_details_label": "Details",
    "module_text_to_speech_config_model_license_label": "Modelllizenz",
    "module_text_to_speech_config_download_models_button": "Modelle herunterladen",
    "module_text_to_speech_config_verify_models_button": "Modelle prüfen",
    "module_text_to_speech_config_cancel_button": "Abbrechen",
    "module_text_to_speech_config_stop_button": "Stopp",
    "module_text_to_speech_config_custom_models_label": "Eigene Modelldateien",
    "module_text_to_speech_config_reading_label": "Vorlesen",
    "module_text_to_speech_config_language_label": "Sprache",
    "module_text_to_speech_config_voice_label": "Stimme",
    "module_text_to_speech_config_speed_label": "Geschwindigkeit",
    "module_text_to_speech_config_announce_headings_label": "Überschriften ansagen",
    "module_text_to_speech_config_skip_inline_code_label": "Inline-Code überspringen",
    "module_text_to_speech_config_skip_multiline_code_label": "Mehrzeiligen Code überspringen",
    "module_text_to_speech_config_test_voice_button": "Stimme testen",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Programm auswählen…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatisch",
    "module_text_to_speech_config_get_runtime_link": "Laufzeit {version} beziehen",
    "module_text_to_speech_config_about_label": "Über {title}",
    "module_text_to_speech_config_choose_path_label": "{title} auswählen",
    "module_text_to_speech_config_status_checking_runtime": "Sprachlaufzeit wird geprüft…",
    "module_text_to_speech_config_status_checking_models": (
        "Gespeicherte Dateien werden geprüft, fehlende Modelle heruntergeladen…"
    ),
    "module_text_to_speech_config_status_models_verified": "Vorhandene Modelle geprüft. Bereit zum Vorlesen.",
    "module_text_to_speech_config_status_models_downloaded": (
        "Modelle heruntergeladen und geprüft. Bereit zum Vorlesen."
    ),
    "module_text_to_speech_config_status_models_found": (
        "Modelldateien gefunden. Prüfen Sie sie oder testen Sie die Stimme."
    ),
    "module_text_to_speech_config_status_models_missing": "Modelle fehlen. Laden Sie die Stimme herunter.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Laufzeit erforderlich. Wählen Sie ein Programm oder beziehen Sie die Laufzeit."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Abgebrochen. Fertige Downloads bleiben erhalten; versuchen Sie es erneut."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Zugriff verweigert. Wählen Sie einen beschreibbaren Modellordner und prüfen Sie die "
        "Zugriffsrechte."
    ),
    "module_text_to_speech_config_error_file_access": "Dateizugriff fehlgeschlagen: {error}. Siehe Details.",
    "module_text_to_speech_config_progress_elapsed": "{time} vergangen",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 Dateien fertig",
    "module_text_to_speech_config_progress_downloading": "Datei {number}/3 · {role} wird heruntergeladen · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 Modelldateien im Cache geprüft…",
    "module_text_to_speech_config_progress_verifying": "Datei {number}/3 · Download wird geprüft…",
    "module_text_to_speech_config_download_role_voice": "Sprachmodell",
    "module_text_to_speech_config_download_role_codec": "Audiodecoder",
    "module_text_to_speech_config_download_role_tokenizers": "Tokenizer",
    "module_text_to_speech_config_download_role_model": "Modell",
    "module_text_to_speech_config_runtime_required": "Wählen Sie zuerst eine Sprachlaufzeit.",
    "module_text_to_speech_config_models_required": "Laden Sie zuerst die Modelle herunter.",
    "module_text_to_speech_config_enable_required": "Aktivieren Sie zuerst Text zu Sprache.",
    "module_text_to_speech_config_status_testing_voice": "Modelle werden geladen und die Teststimme vorbereitet…",
    "module_text_to_speech_config_details_accessible_description": "Protokoll ein- oder ausblenden",
    "module_text_to_speech_config_setup_accessible_description": (
        "Wählen Sie NeMo-Speech.cpp und laden Sie MagpieTTS, NanoCodec und Tokenizer herunter. Modelle "
        "haben eine eigene Lizenz."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Erfordert NeMo-Speech.cpp 0.1.0. Entpacken Sie das Archiv und wählen Sie bin/nemo-speech (unter"
        " Windows bin/nemo-speech.exe)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Modelle werden hier gespeichert. Vorhandene Dateien werden geprüft und wiederverwendet. "
        "Erfordert curl und etwa 550 MB Speicher."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Modellpfade überschreiben oder die Felder leeren, um den Modellordner zu verwenden."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Stimme, Sprache und Geschwindigkeit wählen. Code kann durch eine kurze gesprochene Bezeichnung "
        "ersetzt werden."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Dokumentsprache wählen; keine automatische Erkennung. Standard: Englisch. Mandarin und "
        "Japanisch benötigen eine dafür erstellte Laufzeit."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS-Stimmen: John, Sofia, Aria, Jason und Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "Die Wiedergabegeschwindigkeit verändert auch die Tonhöhe."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Sagt für Markdown- und HTML-Überschriften der Ebenen 1–4 Chapter, Section, Subsection und "
        "Sub-subsection, danach Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Aktiviert: sagt „Inline code block“. Deaktiviert: liest Inline-Code. Eingerückter und umzäunter"
        " Code nutzt die Option für mehrzeiligen Code."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Aktiviert: sagt „Multiline code block“. Deaktiviert: liest eingerückten und umzäunten Code."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Vorhandene Dateien prüfen und fehlende oder beschädigte Dateien herunterladen."
    ),
    "module_text_to_speech_config_editor_required": (
        "Öffnen Sie diese Einstellungen im Editor, um die Stimme zu testen."
    ),
    "module_text_to_speech_config_context_length_label": "Kontextlänge",
    "module_text_to_speech_config_context_whole_document": "Ganzes Dokument",
    "module_text_to_speech_config_context_characters": "{count} Zeichen",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Maximale Zeichen pro Sprachanfrage. Ganz rechts: ganzes Dokument mit Pausen vor Überschriften. "
        "Größere Kontexte brauchen mehr Startzeit und Speicher. Die Grenzen der Laufzeit gelten "
        "weiterhin."
    ),
    "module_text_to_speech_config_cancel_download_title": "Download abbrechen?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Beim Schließen der Einstellungen wird der Download abgebrochen. Fertige Dateien bleiben "
        "erhalten. Einstellungen schließen?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Eigene Modelldateien sind ausgewählt. Downloads werden im Modellordner gespeichert."
    ),
}
