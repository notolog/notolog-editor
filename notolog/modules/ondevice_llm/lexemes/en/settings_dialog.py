# English lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "On Device LLM",

    "module_ondevice_llm_config_label": "On Device LLM Model",
    "module_ondevice_llm_config_path_label": "ONNX Model Location",
    "module_ondevice_llm_config_path_input_placeholder_text": "Path to the Model Directory",
    "module_ondevice_llm_config_path_input_accessible_description":
        "An input field with a selector to specify the path to the model directory where ONNX files are located.\n"
        "Supported models are in the ONNX format, which stands for Open Neural Network Exchange, an open standard\n"
        "format for machine learning models.",

    "module_ondevice_llm_config_response_temperature_label": "Temperature: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Adjusts the randomness of the model's responses. Higher values produce more varied outputs,\n"
        "while lower values make responses more predictable.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maximum Response Tokens",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Sets the maximum number of tokens to be received in a response, such as words and punctuation,\n"
        "controlling the length of the output.",

    "module_ondevice_llm_config_execution_provider_label": "Hardware Acceleration",
    "module_ondevice_llm_config_execution_provider_placeholder": "Select provider",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Select hardware acceleration provider for model inference. Options include:\n"
        "CPU (default), CUDA (NVIDIA GPUs), DirectML (Windows), TensorRT, OpenVINO (Intel), QNN (Qualcomm), CoreML (Apple).\n"
        "Note: Non-CPU providers require specific ONNX Runtime packages (e.g., onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Prompt History Size",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Controls the number of entries in the prompt history that the system retains for reference.\n"
        "A zero value allows for unlimited entries."
}
