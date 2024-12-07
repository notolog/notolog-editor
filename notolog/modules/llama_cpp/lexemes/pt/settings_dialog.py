# Portuguese lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Módulo llama.cpp",

    "module_llama_cpp_config_label": "Módulo llama.cpp",
    "module_llama_cpp_config_path_label": "Localização do Modelo",
    "module_llama_cpp_config_path_input_placeholder_text": "Selecione ou digite o caminho do modelo",
    "module_llama_cpp_config_path_input_accessible_description":
        "Um campo de entrada com um seletor para especificar o caminho do modelo local. Suporta modelos no formato GGUF,\n"
        "um formato de arquivo binário otimizado para armazenar modelos usados com GGML e executores baseados em GGML.",
    "module_llama_cpp_config_path_input_filter_text": "Arquivos GGUF",

    "module_llama_cpp_config_context_window_label": "Tamanho da Janela de Contexto",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Define o número de tokens que o modelo considera para gerar respostas. Controla quanto do contexto anterior é usado.",

    "module_llama_cpp_chat_formats_label": "Formatos de Chat",
    "module_llama_cpp_chat_formats_combo_placeholder_text": "Selecione um formato de chat",
    "module_llama_cpp_chat_formats_combo_accessible_description":
        "Menu suspenso para selecionar o formato usado para conversas do modelo.",

    "module_llama_cpp_config_system_prompt_label": "Prompt do Sistema",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Digite o texto do prompt do sistema",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Campo de texto para inserir prompts de sistema que orientam as respostas do modelo.",

    "module_llama_cpp_config_response_temperature_label": "Temperatura de Resposta: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Ajusta a aleatoriedade das respostas do modelo. Valores mais altos produzem saídas mais variadas,\n"
        "enquanto valores mais baixos resultam em respostas mais previsíveis.",

    "module_llama_cpp_config_response_max_tokens_label": "Máximo de Tokens por Resposta",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Limita o número de tokens nas respostas do modelo até o limite real da janela de contexto.\n"
        "Um valor zero assume a capacidade da janela de contexto.",

    "module_llama_cpp_config_prompt_history_size_label": "Tamanho do Histórico de Prompts",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Controla o número de entradas no histórico de prompts mantidas pelo sistema para referência.\n"
        "Um valor zero permite entradas ilimitadas."
}
