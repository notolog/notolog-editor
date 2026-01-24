# Spanish lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM en Dispositivo",

    "module_ondevice_llm_config_label": "Modelo LLM en Dispositivo",
    "module_ondevice_llm_config_path_label": "Ubicación del Modelo ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Ruta al directorio del modelo",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Un campo de entrada con un selector para especificar la ruta al directorio del modelo donde se encuentran\n"
        "los archivos ONNX. Los modelos compatibles están en formato ONNX, que representa el intercambio de redes\n"
        "neuronales abiertas, un estándar abierto para los formatos de modelos de aprendizaje automático.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatura: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Ajusta la aleatoriedad de las respuestas del modelo. Valores más altos producen salidas más variadas,\n"
        "mientras que valores más bajos hacen que las respuestas sean más predecibles.",

    "module_ondevice_llm_config_response_max_tokens_label": "Máximo de Tokens de Respuesta",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Establece el número máximo de tokens que se recibirán en una respuesta, como palabras y puntuación,\n"
        "controlando la longitud de la salida.",

    "module_ondevice_llm_config_execution_provider_label": "Aceleración de Hardware",
    "module_ondevice_llm_config_execution_provider_placeholder": "Seleccionar proveedor",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Seleccione el proveedor de aceleración de hardware para la inferencia del modelo. "
        "Las opciones incluyen:\n"
        "CPU (predeterminado), CUDA (GPUs NVIDIA), DirectML (Windows), TensorRT, OpenVINO (Intel), "
        "QNN (Qualcomm), CoreML (Apple).\n"
        "Nota: Los proveedores que no son CPU requieren paquetes específicos de ONNX Runtime "
        "(ej: onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Tamaño del Historial de Prompts",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Controla el número de entradas en el historial de prompts que el sistema retiene para referencia.\n"
        "Un valor de cero permite entradas ilimitadas."
}
