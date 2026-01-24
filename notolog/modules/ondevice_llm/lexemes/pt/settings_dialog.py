# Portuguese lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM no Dispositivo",

    "module_ondevice_llm_config_label": "Modelo LLM no Dispositivo",
    "module_ondevice_llm_config_path_label": "Localização do Modelo ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Caminho para o diretório do modelo",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Um campo de entrada com um seletor para especificar o caminho do diretório do modelo onde os arquivos\n"
        "ONNX estão localizados. Os modelos suportados estão no formato ONNX, que representa Open Neural Network Exchange,\n"
        "um padrão aberto para formatos de modelos de aprendizado de máquina.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatura: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Ajusta a aleatoriedade das respostas do modelo. Valores mais altos produzem saídas mais variadas,\n"
        "enquanto valores mais baixos tornam as respostas mais previsíveis.",

    "module_ondevice_llm_config_response_max_tokens_label": "Máximo de Tokens de Resposta",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Define o número máximo de tokens a serem recebidos em uma resposta, incluindo palavras e pontuações,\n"
        "controlando o comprimento da saída.",

    "module_ondevice_llm_config_execution_provider_label": "Aceleração de Hardware",
    "module_ondevice_llm_config_execution_provider_placeholder": "Selecionar provedor",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Selecione o provedor de aceleração de hardware para inferência do modelo. As opções incluem:\n"
        "CPU (padrão), CUDA (GPUs NVIDIA), DirectML (Windows), TensorRT, OpenVINO (Intel), QNN (Qualcomm), CoreML (Apple).\n"
        "Nota: Provedores não-CPU requerem pacotes ONNX Runtime específicos (ex: onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Tamanho do Histórico de Prompts",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Controla o número de entradas no histórico de prompts que o sistema retém para referência.\n"
        "Um valor zero permite entradas ilimitadas."
}
