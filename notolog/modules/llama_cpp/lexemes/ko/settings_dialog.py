# Korean lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "모듈 llama.cpp",

    "module_llama_cpp_config_label": "모듈 llama.cpp",
    "module_llama_cpp_config_path_label": "모델 위치",
    "module_llama_cpp_config_path_input_placeholder_text": "모델 경로 선택 또는 입력",
    "module_llama_cpp_config_path_input_accessible_description":
        "로컬 모델의 경로를 지정하는 선택기가 있는 입력 필드입니다. GGUF 형식의 모델을 지원하며,\n"
        "GGML 및 GGML 기반 실행기와 함께 사용되는 모델을 저장하기 위해 최적화된 이진 파일 형식입니다.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF 파일",

    "module_llama_cpp_config_context_window_label": "콘텍스트 윈도우 크기",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "모델이 응답을 생성하는 데 고려하는 토큰 수를 설정합니다. 얼마나 많은 이전 콘텍스트가 사용되는지를 제어합니다.",

    "module_llama_cpp_config_chat_formats_label": "채팅 형식",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "채팅 형식 선택",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "모델 대화에 사용되는 형식을 선택하기 위한 드롭다운 메뉴입니다.",

    "module_llama_cpp_config_gpu_layers_label": "GPU 레이어",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "GPU로 오프로드할 모델 레이어 수입니다.\n"
        "Auto: 자동 감지(Apple Silicon에서는 GPU, 그 외에는 CPU).\n"
        "-1: 모든 레이어를 GPU로 오프로드.\n"
        "0: CPU 전용 모드(Intel Mac에 권장).\n"
        "1-999: 부분 GPU 오프로드(고급).",

    "module_llama_cpp_config_system_prompt_label": "시스템 프롬프트",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "시스템 프롬프트 텍스트를 입력하세요",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "모델 응답을 안내하는 시스템 프롬프트를 입력하기 위한 텍스트 필드입니다.",

    "module_llama_cpp_config_response_temperature_label": "응답 온도: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "모델 응답의 무작위성을 조절합니다. 높은 값은 더 다양한 출력을 생성하며,\n"
        "낮은 값은 더 예측 가능한 응답을 초래합니다.",

    "module_llama_cpp_config_response_max_tokens_label": "응답당 최대 토큰 수",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "실제 콘텍스트 윈도우 한계까지 모델 응답에서 토큰 수를 제한합니다.\n"
        "제로 값은 콘텍스트 윈도우의 용량을 가정합니다.",

    "module_llama_cpp_config_prompt_history_size_label": "프롬프트 기록 크기",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "시스템에 의해 참조용으로 유지되는 프롬프트 기록의 항목 수를 제어합니다.\n"
        "제로 값은 무제한 항목을 허용합니다."
}
