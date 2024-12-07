# Korean lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API URL",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI API의 URL은 API 엔드포인트의 주소이며, 서비스와 버전에 따라 달라질 수 있습니다.\n"
        "AI 어시스턴트는 대화형 채팅 기능 또는 텍스트 완성을 위해 해당 엔드포인트를 사용합니다.\n"
        "현재 URL을 확인하려면 OpenAI API의 공식 문서를 참조하세요.",
    "module_openai_api_key_label": "API 키",
    "module_openai_api_key_input_placeholder_text": "API 키",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API 키는 API 엔드포인트에 대한 요청을 인증하는 데 사용되는 비밀 토큰입니다.",
    "module_openai_api_supported_models_label": "지원 모델",
    "module_openai_api_model_names_combo_placeholder_text": "모델 선택",
    "module_openai_api_model_names_combo_accessible_description":
        "채팅 대화에 지원되는 모델 중에서 선택합니다.",

    "module_openai_api_base_system_prompt_label": "시스템 프롬프트",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "각 요청에 앞서는 기본 시스템 프롬프트",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "각 요청에 앞서는 기본 시스템 프롬프트입니다.\n"
        "보통 지시사항이나 역할 특성을 포함한 일반 텍스트입니다.",

    "module_openai_api_base_response_temperature_label": "온도: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "모델 응답의 무작위성을 조정합니다. 높은 값은 더 다양한 출력을 생성하고,\n"
        "낮은 값은 응답을 더 예측 가능하게 만듭니다.",

    "module_openai_api_base_response_max_tokens_label": "최대 응답 토큰 수",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "응답에서 받을 수 있는 최대 토큰 수를 설정합니다. 이에는 단어와 구두점이 포함되며,\n"
        "출력의 길이를 제어합니다.",

    "module_openai_api_config_prompt_history_size_label": "프롬프트 이력 크기",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "시스템이 참조용으로 유지하는 프롬프트 이력의 항목 수를 제어합니다.\n"
        "0의 값은 무제한 항목을 허용합니다."
}
