# Spanish lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Módulo llama.cpp",

    "module_llama_cpp_config_label": "Módulo llama.cpp",
    "module_llama_cpp_config_path_label": "Ubicación del modelo",
    "module_llama_cpp_config_path_input_placeholder_text": "Seleccione o introduzca la ruta del modelo",
    "module_llama_cpp_config_path_input_accessible_description":
        "Un campo de entrada con un selector para especificar la ruta del modelo local. Admite modelos en formato GGUF,\n"
        "un formato de archivo binario optimizado para almacenar modelos utilizados con GGML y ejecutores basados en GGML.",
    "module_llama_cpp_config_path_input_filter_text": "Archivos GGUF",

    "module_llama_cpp_config_context_window_label": "Tamaño de la ventana de contexto",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Establece el número de tokens que el modelo considera para generar respuestas.\n"
        "Controla cuánto contexto previo se utiliza.",

    "module_llama_cpp_config_chat_formats_label": "Formatos de chat",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Seleccione un formato de chat",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Menú desplegable para seleccionar el formato utilizado para las conversaciones del modelo.",

    "module_llama_cpp_config_gpu_layers_label": "Capas GPU",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "Número de capas del modelo a descargar en GPU.\n"
        "Auto: Detección automática (GPU en Apple Silicon, CPU en otros).\n"
        "-1: Descargar todas las capas a GPU.\n"
        "0: Modo solo CPU (recomendado para Intel Macs).\n"
        "1-999: Descarga parcial a GPU (avanzado).",

    "module_llama_cpp_config_system_prompt_label": "Prompt del sistema",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Ingrese el texto del prompt del sistema",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Campo de texto para introducir los prompts del sistema que guían las respuestas del modelo.",

    "module_llama_cpp_config_response_temperature_label": "Temperatura de respuesta: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Ajusta la aleatoriedad de las respuestas del modelo. Valores más altos producen resultados más variados,\n"
        "mientras que valores más bajos resultan en respuestas más predecibles.",

    "module_llama_cpp_config_response_max_tokens_label": "Máximos tokens por respuesta",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Limita el número de tokens en las respuestas del modelo hasta el límite actual de la ventana de contexto.\n"
        "Un valor de cero asume la capacidad de la ventana de contexto.",

    "module_llama_cpp_config_prompt_history_size_label": "Tamaño del historial de prompts",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Controla el número de entradas en el historial de prompts retenidas por el sistema para referencia.\n"
        "Un valor de cero permite entradas ilimitadas."
}
