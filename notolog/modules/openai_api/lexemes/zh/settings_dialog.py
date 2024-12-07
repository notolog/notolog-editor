# Chinese lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API URL",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI API的URL是API端点的地址，可能因服务和版本而有所不同。\n"
        "AI助手使用专用于对话聊天功能或文本完成的端点。\n"
        "请参考OpenAI API的官方文档以获取当前的URL。",
    "module_openai_api_key_label": "API密钥",
    "module_openai_api_key_input_placeholder_text": "API密钥",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API密钥是用于验证到API端点请求的秘密令牌。",
    "module_openai_api_supported_models_label": "支持的模型",
    "module_openai_api_model_names_combo_placeholder_text": "选择模型",
    "module_openai_api_model_names_combo_accessible_description":
        "从支持的模型中选择用于聊天对话。",

    "module_openai_api_base_system_prompt_label": "系统提示",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "每个请求前的基础系统提示",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "每个请求前的基础系统提示。\n"
        "通常是包含指导或角色特征的简单文本。",

    "module_openai_api_base_response_temperature_label": "温度: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "调整模型响应的随机性。较高的值产生更多样化的输出，"
        "而较低的值使响应更可预测。",

    "module_openai_api_base_response_max_tokens_label": "响应的最大令牌数",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "接收响应中的最大令牌数，如单词和标点，"
        "控制输出的长度。",

    "module_openai_api_config_prompt_history_size_label": "提示历史大小",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "控制系统保留的提示历史记录中的条目数量。\n"
        "零值允许无限条目。"
}
