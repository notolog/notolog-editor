# Latin lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "In Machina LLM",

    "module_ondevice_llm_config_label": "Modello LLM in Machina",
    "module_ondevice_llm_config_path_label": "Locatio Modeli ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Iter ad Directorium Modeli",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Ager inductus cum selector ad viam directorii modeli, ubi ONNX files reperiuntur, designandum.\n"
        "Modeli fulciti sunt in formato ONNX, quod stat pro Open Neural Network Exchange, norma aperta\n"
        "formato pro machinalibus discendi modelis.",

    "module_ondevice_llm_config_response_temperature_label": "Temperatura: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Casualitatem responsionum modeli accommodat. Valores altiores output variores producunt,\n"
        "dum valores inferiores responsiones praedicibiliores reddunt.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maximi Responsionis Token",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Numerum summum signorum in responsione recipiendis constituit, ut verba et punctuationes,\n"
        "longitudinem productionis moderans.",

    "module_ondevice_llm_config_execution_provider_label": "Acceleratio Ferramentaria",
    "module_ondevice_llm_config_execution_provider_placeholder": "Elige provisorem",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Elige provisorem accelerationis ferramentariae pro modeli inferentia. Optiones includunt:\n"
        "CPU (defalta), CUDA (NVIDIA GPU), DirectML (Windows), TensorRT, OpenVINO (Intel), QNN (Qualcomm), CoreML (Apple).\n"
        "Nota: Provisores non-CPU requirunt fasciculos ONNX Runtime specificos (e.g. onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Magna Historia Prompti",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Numerum inquisitionum in historia prompti, quam systema ad referentiam conservat, moderatur.\n"
        "Valor nihili inquisitiones infinitas permittit."
}
