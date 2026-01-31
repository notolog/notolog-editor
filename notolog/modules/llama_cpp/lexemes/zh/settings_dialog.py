# Chinese lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "模块 llama.cpp",

    "module_llama_cpp_config_label": "模块 llama.cpp",
    "module_llama_cpp_config_path_label": "模型位置",
    "module_llama_cpp_config_path_input_placeholder_text": "选择或输入模型路径",
    "module_llama_cpp_config_path_input_accessible_description":
        "一个带选择器的输入字段，用于指定本地模型的路径。支持GGUF格式的模型，\n"
        "一种二进制文件格式，专为存储用于GGML及基于GGML执行器的模型而优化。",
    "module_llama_cpp_config_path_input_filter_text": "GGUF 文件",

    "module_llama_cpp_config_context_window_label": "上下文窗口大小",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "设置模型生成响应时考虑的令牌数量。控制使用多少先前上下文。",

    "module_llama_cpp_config_chat_formats_label": "聊天格式",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "选择聊天格式",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "用于选择模型对话格式的下拉菜单。",

    "module_llama_cpp_config_gpu_layers_label": "GPU层数",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "要卸载到GPU的模型层数。\n"
        "Auto：自动检测（Apple Silicon使用GPU，其他使用CPU）。\n"
        "-1：将所有层卸载到GPU。\n"
        "0：仅CPU模式（推荐用于Intel Mac）。\n"
        "1-999：部分GPU卸载（高级）。",

    "module_llama_cpp_config_system_prompt_label": "系统提示",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "输入系统提示文本",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "用于输入指导模型响应的系统提示的文本字段。",

    "module_llama_cpp_config_response_temperature_label": "响应温度：{temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "调整模型响应的随机性。较高的值产生更多变化的输出，\n"
        "而较低的值结果更可预测的响应。",

    "module_llama_cpp_config_response_max_tokens_label": "每次响应的最大令牌数",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "限制模型响应中的令牌数量，直至实际的上下文窗口限制。\n"
        "零值假设上下文窗口的容量。",

    "module_llama_cpp_config_prompt_history_size_label": "提示历史大小",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "控制系统保留供参考的提示历史记录中的条目数量。\n"
        "零值允许无限条目。"
}
