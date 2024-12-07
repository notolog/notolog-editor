# Chinese lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "本地设备LLM",

    "module_ondevice_llm_config_label": "本地设备LLM模型",
    "module_ondevice_llm_config_path_label": "ONNX模型位置",
    "module_ondevice_llm_config_path_input_placeholder_text": "模型目录路径",
    "module_ondevice_llm_config_path_input_accessible_description":
        "一个带选择器的输入字段，用于指定ONNX文件所在的模型目录路径。\n"
        "支持的模型格式为ONNX，即开放神经网络交换，这是一个开放标准的机器学习模型格式。",

    "module_ondevice_llm_config_response_temperature_label": "温度：{temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "调整模型响应的随机性。较高的值产生更多变化的输出，\n"
        "而较低的值使响应更可预测。",

    "module_ondevice_llm_config_response_max_tokens_label": "最大响应令牌数",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "设置响应中接收的最大令牌数，如单词和标点，\n"
        "控制输出的长度。",

    "module_ondevice_llm_config_prompt_history_size_label": "提示历史大小",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "控制系统保留用于参考的提示历史中的条目数量。\n"
        "零值允许无限制条目。"
}
