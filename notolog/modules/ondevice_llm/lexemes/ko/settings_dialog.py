# Korean lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "기기 내 LLM",

    "module_ondevice_llm_config_label": "기기 내 LLM 모델",
    "module_ondevice_llm_config_path_label": "ONNX 모델 위치",
    "module_ondevice_llm_config_path_input_placeholder_text": "모델 디렉토리 경로",
    "module_ondevice_llm_config_path_input_accessible_description":
        "ONNX 파일이 위치한 모델 디렉토리 경로를 지정하기 위한 선택기가 있는 입력 필드입니다.\n"
        "지원되는 모델은 ONNX 형식으로, Open Neural Network Exchange의 약자이며 기계 학습 모델의 개방형 표준\n"
        "형식입니다.",

    "module_ondevice_llm_config_response_temperature_label": "온도: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "모델의 반응의 무작위성을 조절합니다. 높은 값은 더 다양한 출력을 생성하며,\n"
        "낮은 값은 반응을 더 예측 가능하게 합니다.",

    "module_ondevice_llm_config_response_max_tokens_label": "최대 응답 토큰 수",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "응답에서 받을 수 있는 토큰의 최대 수를 설정합니다. 여기에는 단어와 구두점이 포함되며,\n"
        "출력의 길이를 제어합니다.",

    "module_ondevice_llm_config_prompt_history_size_label": "프롬프트 기록 크기",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "시스템에 의해 참조용으로 유지되는 프롬프트 기록의 항목 수를 제어합니다.\n"
        "0값은 무제한 항목을 허용합니다."
}
