# Japanese lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description": "OpenAI APIのURL",
    "module_openai_api_key_input_placeholder_text": "API キー",
    "module_openai_api_key_input_accessible_description": "OpenAI APIのキー",
    "module_openai_api_supported_models_label": "サポートされているモデル",
    "module_openai_api_model_names_combo_placeholder_text": "モデルを選択",
    "module_openai_api_model_names_combo_accessible_description": "選択可能なサポートされているモデル",

    "module_openai_api_base_system_prompt_label": "システムプロンプト",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "各リクエストに先立つ基本システムプロンプト",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "各リクエストに先立つ基本システムプロンプト。プレーンテキスト。",

    "module_openai_api_base_response_temperature_label": "温度: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "モデル出力のランダム性を調整します。高い値は創造性を増加させ、低い値は決定論を強化します。",

    "module_openai_api_base_response_max_tokens_label": "最大レスポンストークン数",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "レスポンスで受け取るトークンの最大数、例えば単語や句読点など、"
        "出力の長さを制御します。",
}
