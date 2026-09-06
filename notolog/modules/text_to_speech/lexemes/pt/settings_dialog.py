# Portuguese lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Ativar texto para fala",
    "module_text_to_speech_config_setup_label": "Configuração da voz",
    "module_text_to_speech_config_runtime_label": "Motor de voz",
    "module_text_to_speech_config_model_directory_label": "Pasta dos modelos",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizadores",
    "module_text_to_speech_config_details_label": "Detalhes",
    "module_text_to_speech_config_model_license_label": "Licença do modelo",
    "module_text_to_speech_config_download_models_button": "Baixar modelos",
    "module_text_to_speech_config_verify_models_button": "Verificar modelos",
    "module_text_to_speech_config_cancel_button": "Cancelar",
    "module_text_to_speech_config_stop_button": "Parar",
    "module_text_to_speech_config_custom_models_label": "Arquivos de modelo personalizados",
    "module_text_to_speech_config_reading_label": "Leitura",
    "module_text_to_speech_config_language_label": "Idioma",
    "module_text_to_speech_config_voice_label": "Voz",
    "module_text_to_speech_config_speed_label": "Velocidade",
    "module_text_to_speech_config_announce_headings_label": "Anunciar títulos",
    "module_text_to_speech_config_skip_inline_code_label": "Ignorar código em linha",
    "module_text_to_speech_config_skip_multiline_code_label": "Ignorar código multilinha",
    "module_text_to_speech_config_test_voice_button": "Testar voz",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Selecionar executável…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automático",
    "module_text_to_speech_config_get_runtime_link": "Obter motor {version}",
    "module_text_to_speech_config_about_label": "Sobre {title}",
    "module_text_to_speech_config_choose_path_label": "Escolher {title}",
    "module_text_to_speech_config_status_checking_runtime": "Verificando motor de voz…",
    "module_text_to_speech_config_status_checking_models": "Verificando cache e baixando modelos ausentes…",
    "module_text_to_speech_config_status_models_verified": "Modelos existentes verificados. Pronto para ler.",
    "module_text_to_speech_config_status_models_downloaded": "Modelos baixados e verificados. Pronto para ler.",
    "module_text_to_speech_config_status_models_found": "Modelos encontrados. Verifique-os ou teste a voz.",
    "module_text_to_speech_config_status_models_missing": "Modelos necessários. Baixe a voz para começar.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Motor necessário. Selecione um executável ou obtenha o motor."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Cancelado. Downloads concluídos foram mantidos; tente novamente."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Permissão negada. Escolha uma pasta gravável e verifique o acesso."
    ),
    "module_text_to_speech_config_error_file_access": "Falha no acesso ao arquivo: {error}. Veja Detalhes.",
    "module_text_to_speech_config_progress_elapsed": "{time} decorridos",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 arquivos concluídos",
    "module_text_to_speech_config_progress_downloading": "Arquivo {number}/3 · Baixando {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 arquivos de modelo verificados no cache…",
    "module_text_to_speech_config_progress_verifying": "Arquivo {number}/3 · Verificando download…",
    "module_text_to_speech_config_download_role_voice": "modelo de voz",
    "module_text_to_speech_config_download_role_codec": "decodificador de áudio",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizadores",
    "module_text_to_speech_config_download_role_model": "modelo",
    "module_text_to_speech_config_runtime_required": "Selecione primeiro um motor de voz.",
    "module_text_to_speech_config_models_required": "Baixe primeiro os modelos.",
    "module_text_to_speech_config_enable_required": "Ative primeiro o texto para fala.",
    "module_text_to_speech_config_status_testing_voice": "Carregando modelos e preparando a voz de teste…",
    "module_text_to_speech_config_details_accessible_description": "Mostrar ou ocultar registro da operação",
    "module_text_to_speech_config_setup_accessible_description": (
        "Selecione NeMo-Speech.cpp e baixe MagpieTTS, NanoCodec e os tokenizadores. Os modelos têm "
        "licença separada."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Requer NeMo-Speech.cpp 0.1.0. Extraia o arquivo e selecione bin/nemo-speech "
        "(bin/nemo-speech.exe no Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Os modelos são baixados aqui. Arquivos existentes são verificados e reutilizados. Requer curl e"
        " cerca de 550 MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Substitua os caminhos dos modelos ou limpe os campos para usar a pasta dos modelos."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Escolha voz, idioma e velocidade. O código pode ser substituído por uma breve identificação "
        "falada."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Escolha o idioma do documento; não há detecção automática. Padrão: inglês. Mandarim e japonês "
        "exigem um motor compatível."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Vozes MagpieTTS: John, Sofia, Aria, Jason e Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "A velocidade de reprodução também altera o tom da voz."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Anuncia Chapter, Section, Subsection e Sub-subsection para títulos Markdown e HTML de níveis "
        "1–4, depois Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Marcado: diz “Inline code block”. Desmarcado: lê o código em linha. Código delimitado ou "
        "indentado usa a opção multilinha."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Marcado: diz “Multiline code block”. Desmarcado: lê código delimitado ou indentado."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Verificar arquivos existentes e baixar os ausentes ou danificados."
    ),
    "module_text_to_speech_config_editor_required": "Abra estas configurações no editor para testar a voz.",
    "module_text_to_speech_config_context_length_label": "Tamanho do contexto",
    "module_text_to_speech_config_context_whole_document": "Documento inteiro",
    "module_text_to_speech_config_context_characters": "{count} caracteres",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Máximo de caracteres por solicitação de voz. À direita: documento inteiro, mantendo pausas nos "
        "títulos. Contextos maiores demoram mais para iniciar e usam mais memória. Os limites do motor "
        "continuam válidos."
    ),
    "module_text_to_speech_config_cancel_download_title": "Cancelar o download?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Fechar as configurações cancela o download. Os arquivos concluídos são mantidos. Fechar as "
        "configurações?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Arquivos de modelo personalizados estão selecionados. Os downloads usam a pasta de modelos."
    ),
}
