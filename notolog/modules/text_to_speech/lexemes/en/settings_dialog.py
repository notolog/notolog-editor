# English lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Enable Text-to-Speech",
    "module_text_to_speech_config_setup_label": "Voice setup",
    "module_text_to_speech_config_runtime_label": "Speech runtime",
    "module_text_to_speech_config_model_directory_label": "Model folder",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizers",
    "module_text_to_speech_config_details_label": "Details",
    "module_text_to_speech_config_model_license_label": "Model license",
    "module_text_to_speech_config_download_models_button": "Download models",
    "module_text_to_speech_config_verify_models_button": "Verify models",
    "module_text_to_speech_config_cancel_button": "Cancel",
    "module_text_to_speech_config_stop_button": "Stop",
    "module_text_to_speech_config_custom_models_label": "Custom model files",
    "module_text_to_speech_config_reading_label": "Reading",
    "module_text_to_speech_config_language_label": "Language",
    "module_text_to_speech_config_voice_label": "Voice",
    "module_text_to_speech_config_speed_label": "Speed",
    "module_text_to_speech_config_announce_headings_label": "Announce headings",
    "module_text_to_speech_config_skip_inline_code_label": "Skip inline code",
    "module_text_to_speech_config_skip_multiline_code_label": "Skip multiline code",
    "module_text_to_speech_config_test_voice_button": "Test voice",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Select executable…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatic",
    "module_text_to_speech_config_get_runtime_link": "Get runtime {version}",
    "module_text_to_speech_config_about_label": "About {title}",
    "module_text_to_speech_config_choose_path_label": "Choose {title}",
    "module_text_to_speech_config_status_checking_runtime": "Checking speech runtime…",
    "module_text_to_speech_config_status_checking_models": "Checking cached files and downloading missing models…",
    "module_text_to_speech_config_status_models_verified": "Existing models verified. Ready to read.",
    "module_text_to_speech_config_status_models_downloaded": "Models downloaded and verified. Ready to read.",
    "module_text_to_speech_config_status_models_found": "Model files found. Verify them or test the voice.",
    "module_text_to_speech_config_status_models_missing": "Models needed. Download the voice to start reading.",
    "module_text_to_speech_config_status_runtime_missing": "Runtime required. Select an executable or use Get runtime.",
    "module_text_to_speech_config_status_download_cancelled": (
        "Cancelled. Completed downloads are retained; retry to continue."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Permission denied. Choose a writable model folder and check file access."
    ),
    "module_text_to_speech_config_error_file_access": "File access failed: {error}. See Details.",
    "module_text_to_speech_config_progress_elapsed": "{time} elapsed",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 files complete",
    "module_text_to_speech_config_progress_downloading": "File {number}/3 · Downloading {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 model files verified in cache…",
    "module_text_to_speech_config_progress_verifying": "File {number}/3 · Verifying downloaded file…",
    "module_text_to_speech_config_download_role_voice": "voice model",
    "module_text_to_speech_config_download_role_codec": "audio decoder",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizers",
    "module_text_to_speech_config_download_role_model": "model",
    "module_text_to_speech_config_runtime_required": "Select a speech runtime first.",
    "module_text_to_speech_config_models_required": "Download models first.",
    "module_text_to_speech_config_enable_required": "Enable Text-to-Speech first.",
    "module_text_to_speech_config_status_testing_voice": "Loading models and preparing the test voice…",
    "module_text_to_speech_config_details_accessible_description": "Show or hide the operation log",
    "module_text_to_speech_config_setup_accessible_description": (
        "Select a NeMo-Speech.cpp runtime, then download the MagpieTTS voice. The model set includes "
        "NanoCodec and tokenizers. Models have a separate license."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "This integration requires NeMo-Speech.cpp 0.1.0. Extract the runtime archive and select "
        "bin/nemo-speech (bin/nemo-speech.exe on Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "MagpieTTS, NanoCodec and tokenizers are downloaded here. Existing files are verified and "
        "reused. Downloads require curl and about 550 MB of space."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Override downloaded model paths, or clear these fields to use the model folder."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Choose the voice, language and playback speed. Code can be replaced with a short spoken label "
        "instead of reading its contents."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Choose the document language; it is not detected automatically. English is the default. "
        "Mandarin and Japanese require a runtime built with support for those languages."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS voices: John, Sofia, Aria, Jason and Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "Native playback speed also changes voice pitch."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Say Chapter, Section, Subsection and Sub-subsection for heading levels 1–4, then Heading level "
        "5–6. Applies to Markdown and HTML headings."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Checked: say “Inline code block”. Unchecked: read the inline code contents. Fenced and indented"
        " blocks use the multiline setting."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Checked: say “Multiline code block”. Unchecked: read fenced and indented code contents."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Verify existing files and download any missing or damaged files."
    ),
    "module_text_to_speech_config_editor_required": "Open these settings from the editor to test the voice.",
    "module_text_to_speech_config_context_length_label": "Context length",
    "module_text_to_speech_config_context_whole_document": "Whole document",
    "module_text_to_speech_config_context_characters": "{count} characters",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Maximum characters per speech request. Far right: whole document, with heading breaks "
        "preserved. Larger contexts take longer to start and use more memory. Runtime limits still "
        "apply."
    ),
    "module_text_to_speech_config_cancel_download_title": "Cancel download?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Closing settings cancels the download. Completed files are kept. Close settings?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Custom model files are selected. Downloads use the model folder."
    ),
}
