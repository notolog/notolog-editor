# Spanish lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Activar texto a voz",
    "module_text_to_speech_config_setup_label": "Configurar voz",
    "module_text_to_speech_config_runtime_label": "Motor de voz",
    "module_text_to_speech_config_model_directory_label": "Carpeta de modelos",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizadores",
    "module_text_to_speech_config_details_label": "Detalles",
    "module_text_to_speech_config_model_license_label": "Licencia del modelo",
    "module_text_to_speech_config_download_models_button": "Descargar modelos",
    "module_text_to_speech_config_verify_models_button": "Verificar modelos",
    "module_text_to_speech_config_cancel_button": "Cancelar",
    "module_text_to_speech_config_stop_button": "Detener",
    "module_text_to_speech_config_custom_models_label": "Archivos de modelo personalizados",
    "module_text_to_speech_config_reading_label": "Lectura",
    "module_text_to_speech_config_language_label": "Idioma",
    "module_text_to_speech_config_voice_label": "Voz",
    "module_text_to_speech_config_speed_label": "Velocidad",
    "module_text_to_speech_config_announce_headings_label": "Anunciar encabezados",
    "module_text_to_speech_config_skip_inline_code_label": "Omitir código en línea",
    "module_text_to_speech_config_skip_multiline_code_label": "Omitir código multilínea",
    "module_text_to_speech_config_test_voice_button": "Probar voz",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Seleccionar ejecutable…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automático",
    "module_text_to_speech_config_get_runtime_link": "Obtener motor {version}",
    "module_text_to_speech_config_about_label": "Acerca de {title}",
    "module_text_to_speech_config_choose_path_label": "Seleccionar {title}",
    "module_text_to_speech_config_status_checking_runtime": "Verificando motor de voz…",
    "module_text_to_speech_config_status_checking_models": (
        "Verificando archivos guardados y descargando modelos que faltan…"
    ),
    "module_text_to_speech_config_status_models_verified": "Modelos existentes verificados. Listo para leer.",
    "module_text_to_speech_config_status_models_downloaded": "Modelos descargados y verificados. Listo para leer.",
    "module_text_to_speech_config_status_models_found": "Modelos encontrados. Verifíquelos o pruebe la voz.",
    "module_text_to_speech_config_status_models_missing": "Faltan modelos. Descargue la voz para empezar.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Se requiere un motor. Seleccione un ejecutable u obtenga el motor."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Cancelado. Se conservan las descargas completas; reintente para continuar."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Permiso denegado. Elija una carpeta de modelos con permiso de escritura y revise el acceso."
    ),
    "module_text_to_speech_config_error_file_access": "Error de acceso al archivo: {error}. Consulte Detalles.",
    "module_text_to_speech_config_progress_elapsed": "{time} transcurridos",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 archivos completos",
    "module_text_to_speech_config_progress_downloading": "Archivo {number}/3 · Descargando {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 archivos de modelo verificados en caché…",
    "module_text_to_speech_config_progress_verifying": "Archivo {number}/3 · Verificando descarga…",
    "module_text_to_speech_config_download_role_voice": "modelo de voz",
    "module_text_to_speech_config_download_role_codec": "decodificador de audio",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizadores",
    "module_text_to_speech_config_download_role_model": "modelo",
    "module_text_to_speech_config_runtime_required": "Seleccione primero un motor de voz.",
    "module_text_to_speech_config_models_required": "Descargue primero los modelos.",
    "module_text_to_speech_config_enable_required": "Active primero texto a voz.",
    "module_text_to_speech_config_status_testing_voice": "Cargando modelos y preparando la voz de prueba…",
    "module_text_to_speech_config_details_accessible_description": "Mostrar u ocultar el registro",
    "module_text_to_speech_config_setup_accessible_description": (
        "Seleccione NeMo-Speech.cpp y descargue MagpieTTS, NanoCodec y los tokenizadores. Los modelos "
        "tienen su propia licencia."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Requiere NeMo-Speech.cpp 0.1.0. Extraiga el archivo y seleccione bin/nemo-speech "
        "(bin/nemo-speech.exe en Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Los modelos se descargan aquí. Los archivos existentes se verifican y reutilizan. Requiere curl"
        " y unos 550 MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Indique otras rutas de modelos o vacíe los campos para usar la carpeta de modelos."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Elija voz, idioma y velocidad. El código puede sustituirse por una breve etiqueta hablada."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Elija el idioma del documento; no se detecta automáticamente. Por defecto: inglés. Mandarín y "
        "japonés requieren un motor con soporte específico."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Voces MagpieTTS: John, Sofia, Aria, Jason y Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "La velocidad de reproducción también cambia el tono de voz."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Anuncia Chapter, Section, Subsection y Sub-subsection para encabezados Markdown y HTML de "
        "niveles 1–4, y Heading level 5–6 para los demás."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Marcado: dice «Inline code block». Desmarcado: lee el código en línea. El código delimitado o "
        "sangrado usa la opción multilínea."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Marcado: dice «Multiline code block». Desmarcado: lee el código delimitado o sangrado."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Verificar los archivos existentes y descargar los que faltan o están dañados."
    ),
    "module_text_to_speech_config_editor_required": "Abre estos ajustes desde el editor para probar la voz.",
    "module_text_to_speech_config_context_length_label": "Longitud de contexto",
    "module_text_to_speech_config_context_whole_document": "Documento completo",
    "module_text_to_speech_config_context_characters": "{count} caracteres",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Máximo de caracteres por solicitud de voz. Extremo derecho: documento completo, conservando las"
        " pausas de títulos. Un contexto mayor tarda más en iniciar y usa más memoria. Se mantienen los "
        "límites del motor."
    ),
    "module_text_to_speech_config_cancel_download_title": "¿Cancelar la descarga?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Cerrar los ajustes cancela la descarga. Los archivos completados se conservan. ¿Cerrar los "
        "ajustes?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Se han seleccionado archivos de modelo personalizados. Las descargas usan la carpeta de "
        "modelos."
    ),
}
