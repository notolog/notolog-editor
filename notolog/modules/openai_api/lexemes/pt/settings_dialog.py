# Portuguese lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "API da OpenAI",

    "module_openai_api_label": "API da OpenAI",
    "module_openai_api_url_label": "URL da API",
    "module_openai_api_url_input_placeholder_text": "URL da API",
    "module_openai_api_url_input_accessible_description":
        "A URL da API da OpenAI é o endereço do endpoint da API, que pode variar dependendo do serviço e da versão.\n"
        "O Assistente de IA usa aquele para funcionalidades de chat conversacional ou completamentos de texto.\n"
        "Consulte a documentação oficial da API da OpenAI para obter a URL atual.",
    "module_openai_api_key_label": "Chave API",
    "module_openai_api_key_input_placeholder_text": "Chave API",
    "module_openai_api_key_input_accessible_description":
        "A chave API da OpenAI é um token secreto usado para autenticar solicitações ao endpoint da API.",
    "module_openai_api_supported_models_label": "Modelos suportados",
    "module_openai_api_model_names_combo_placeholder_text": "Escolha um modelo",
    "module_openai_api_model_names_combo_accessible_description":
        "Selecione entre os modelos suportados para conversas por chat.",

    "module_openai_api_base_system_prompt_label": "Prompt do sistema",
    "module_openai_api_base_system_prompt_edit_placeholder_text":
        "Prompt de sistema base que antecede cada solicitação",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Um prompt de sistema base que antecede cada solicitação.\n"
        "Normalmente é um texto simples com instruções ou características de papel.",

    "module_openai_api_base_response_temperature_label": "Temperatura: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Ajusta a aleatoriedade das respostas do modelo. Valores mais altos produzem saídas mais variadas, "
        "enquanto valores mais baixos tornam as respostas mais previsíveis.",

    "module_openai_api_base_response_max_tokens_label": "Máximo de tokens por resposta",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "O número máximo de tokens que podem ser recebidos em uma resposta, incluindo palavras e pontuação, "
        "controlando o comprimento da saída.",

    "module_openai_api_config_prompt_history_size_label": "Tamanho do histórico de prompts",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Controla o número de entradas no histórico de prompts que o sistema retém para referência.\n"
        "Um valor zero permite entradas ilimitadas."
}
