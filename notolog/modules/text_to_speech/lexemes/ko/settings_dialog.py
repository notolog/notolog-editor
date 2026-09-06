# Korean lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "텍스트 음성 변환 활성화",
    "module_text_to_speech_config_setup_label": "음성 설정",
    "module_text_to_speech_config_runtime_label": "음성 런타임",
    "module_text_to_speech_config_model_directory_label": "모델 폴더",
    "module_text_to_speech_config_tokenizer_directory_label": "토크나이저",
    "module_text_to_speech_config_details_label": "자세히",
    "module_text_to_speech_config_model_license_label": "모델 라이선스",
    "module_text_to_speech_config_download_models_button": "모델 다운로드",
    "module_text_to_speech_config_verify_models_button": "모델 검증",
    "module_text_to_speech_config_cancel_button": "취소",
    "module_text_to_speech_config_stop_button": "중지",
    "module_text_to_speech_config_custom_models_label": "사용자 지정 모델 파일",
    "module_text_to_speech_config_reading_label": "읽기",
    "module_text_to_speech_config_language_label": "언어",
    "module_text_to_speech_config_voice_label": "음성",
    "module_text_to_speech_config_speed_label": "속도",
    "module_text_to_speech_config_announce_headings_label": "제목 수준 알림",
    "module_text_to_speech_config_skip_inline_code_label": "인라인 코드 건너뛰기",
    "module_text_to_speech_config_skip_multiline_code_label": "여러 줄 코드 건너뛰기",
    "module_text_to_speech_config_test_voice_button": "음성 테스트",
    "module_text_to_speech_config_runtime_input_placeholder_text": "실행 파일 선택…",
    "module_text_to_speech_config_model_input_placeholder_text": "자동",
    "module_text_to_speech_config_get_runtime_link": "런타임 {version} 받기",
    "module_text_to_speech_config_about_label": "{title} 정보",
    "module_text_to_speech_config_choose_path_label": "{title} 선택",
    "module_text_to_speech_config_status_checking_runtime": "음성 런타임 확인 중…",
    "module_text_to_speech_config_status_checking_models": "캐시 확인 및 누락된 모델 다운로드 중…",
    "module_text_to_speech_config_status_models_verified": "기존 모델 검증 완료. 읽을 준비가 되었습니다.",
    "module_text_to_speech_config_status_models_downloaded": "모델 다운로드 및 검증 완료. 읽을 준비가 되었습니다.",
    "module_text_to_speech_config_status_models_found": "모델을 찾았습니다. 검증하거나 음성을 테스트하세요.",
    "module_text_to_speech_config_status_models_missing": "모델이 필요합니다. 음성을 다운로드하세요.",
    "module_text_to_speech_config_status_runtime_missing": "런타임이 필요합니다. 실행 파일을 선택하거나 런타임을 받으세요.",
    "module_text_to_speech_config_status_download_cancelled": "취소되었습니다. 완료된 다운로드는 유지됩니다. 다시 시도하세요.",
    "module_text_to_speech_config_error_permission_denied": "권한이 거부되었습니다. 쓰기 가능한 모델 폴더를 선택하고 접근 권한을 확인하세요.",
    "module_text_to_speech_config_error_file_access": "파일 접근 실패: {error}. 자세한 내용을 확인하세요.",
    "module_text_to_speech_config_progress_elapsed": "{time} 경과",
    "module_text_to_speech_config_progress_files_complete": "{count}/3개 파일 완료",
    "module_text_to_speech_config_progress_downloading": "파일 {number}/3 · {role} 다운로드 중 · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "캐시의 모델 파일 {count}/3개 검증 완료…",
    "module_text_to_speech_config_progress_verifying": "파일 {number}/3 · 다운로드 검증 중…",
    "module_text_to_speech_config_download_role_voice": "음성 모델",
    "module_text_to_speech_config_download_role_codec": "오디오 디코더",
    "module_text_to_speech_config_download_role_tokenizers": "토크나이저",
    "module_text_to_speech_config_download_role_model": "모델",
    "module_text_to_speech_config_runtime_required": "먼저 음성 런타임을 선택하세요.",
    "module_text_to_speech_config_models_required": "먼저 모델을 다운로드하세요.",
    "module_text_to_speech_config_enable_required": "먼저 텍스트 음성 변환을 활성화하세요.",
    "module_text_to_speech_config_status_testing_voice": "모델 로드 및 테스트 음성 준비 중…",
    "module_text_to_speech_config_details_accessible_description": "작업 로그 표시 또는 숨기기",
    "module_text_to_speech_config_setup_accessible_description": (
        "NeMo-Speech.cpp를 선택한 후 MagpieTTS, NanoCodec 및 토크나이저를 다운로드하세요. 모델에는 별도 라이선스가 적용됩니다."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "NeMo-Speech.cpp 0.1.0이 필요합니다. 압축을 풀고 bin/nemo-speech(Windows: bin/nemo-speech.exe)를 선택하세요."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "모델을 여기에 다운로드합니다. 기존 파일은 검증 후 재사용합니다. curl과 약 550 MB의 공간이 필요합니다."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": "모델 경로를 지정하거나 필드를 비워 모델 폴더를 사용하세요.",
    "module_text_to_speech_config_reading_accessible_description": "음성, 언어 및 속도를 선택하세요. 코드 내용 대신 짧은 음성 안내를 읽을 수 있습니다.",
    "module_text_to_speech_config_language_input_accessible_description": (
        "문서 언어를 선택하세요. 자동으로 감지하지 않으며 기본값은 영어입니다. 표준 중국어와 일본어에는 해당 언어 지원을 포함해 빌드한 런타임이 필요합니다."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": "MagpieTTS 음성: John, Sofia, Aria, Jason, Leo.",
    "module_text_to_speech_config_speed_input_accessible_description": "재생 속도를 바꾸면 음높이도 바뀝니다.",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Markdown과 HTML의 제목 수준 1~4는 Chapter, Section, Subsection, Sub-subsection으로, 5~6은 Heading level "
        "5–6으로 읽습니다."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "선택: “Inline code block”을 읽습니다. 해제: 인라인 코드 내용을 읽습니다. 울타리 또는 들여쓰기로 구분한 코드는 여러 줄 설정을 따릅니다."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "선택: “Multiline code block”을 읽습니다. 해제: 울타리 또는 들여쓰기로 구분한 코드 내용을 읽습니다."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": "기존 파일을 검증하고 누락되거나 손상된 파일을 다운로드합니다.",
    "module_text_to_speech_config_editor_required": "음성을 테스트하려면 편집기에서 이 설정을 여세요.",
    "module_text_to_speech_config_context_length_label": "컨텍스트 길이",
    "module_text_to_speech_config_context_whole_document": "문서 전체",
    "module_text_to_speech_config_context_characters": "{count}자",
    "module_text_to_speech_config_context_length_accessible_description": (
        "음성 요청당 최대 문자 수입니다. 맨 오른쪽은 제목 사이의 쉼을 유지한 문서 전체입니다. 컨텍스트가 크면 시작이 느려지고 메모리를 더 사용합니다. 런타임 제한은 계속 "
        "적용됩니다."
    ),
    "module_text_to_speech_config_cancel_download_title": "다운로드를 취소할까요?",
    "module_text_to_speech_config_cancel_download_confirmation": "설정을 닫으면 다운로드가 취소됩니다. 완료된 파일은 보관됩니다. 설정을 닫을까요?",
    "module_text_to_speech_config_status_custom_models": "사용자 지정 모델 파일이 선택되었습니다. 다운로드에는 모델 폴더가 사용됩니다.",
}
