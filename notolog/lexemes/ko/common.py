# Korean lexemes common.py
lexemes = {
    "app_title": "Notolog 에디터",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_input_placeholder_text": "빠른 필터",
    "tree_filter_input_accessible_desc": "파일 및 디렉터리를 이름으로 필터링",
    "tree_filter_clear_button_tooltip": "필터 지우기",
    "tree_filter_clear_button_accessible_name": "필터 입력 필드 지우기",

    "menu_action_copy_file_path": "파일 경로 복사",
    "menu_action_rename": "이름 바꾸기",
    "menu_action_delete": "삭제",
    "menu_action_delete_completely": "완전히 삭제",
    "menu_action_restore": "복원",
    "menu_action_create_new_dir": "새 디렉터리 만들기",

    "dialog_file_rename_title": "파일 이름 바꾸기",
    "dialog_file_rename_field_label": "새 파일 이름 입력",
    "dialog_file_rename_button_ok": "이름 바꾸기",
    "dialog_file_rename_warning_exists": "동일한 이름의 파일이 이미 존재합니다",

    "dialog_file_delete_title": "파일 삭제",
    "dialog_file_delete_text": "파일 \"{file_name}\"을(를) 삭제하시겠습니까?",
    "dialog_file_delete_completely_title": "파일 완전 삭제",
    "dialog_file_delete_completely_text": "파일 \"{file_name}\"을(를) 완전히 삭제하시겠습니까?",
    "dialog_file_delete_error": "파일을 삭제할 수 없습니다. 오류가 발생했습니다",
    "dialog_file_delete_error_not_found": "파일을 찾을 수 없습니다",

    "dialog_file_restore_title": "파일 복원",
    "dialog_file_restore_text": "파일 \"{file_name}\"을(를) 복원하시겠습니까?",
    "dialog_file_restore_error": "파일을 복원할 수 없습니다. 오류가 발생했습니다",
    "dialog_file_restore_warning_exists": "{file_name} 이름의 파일이 이미 존재합니다",

    "dialog_create_new_dir_title": "새 디렉터리 만들기",
    "dialog_create_new_dir_label": "새 디렉터리 이름",
    "dialog_create_new_dir_input_placeholder_text": "디렉터리 이름 입력",
    "dialog_create_new_dir_button_ok": "만들기",
    "dialog_create_new_dir_button_cancel": "취소",
    "dialog_create_new_dir_warning_empty_title": "새 디렉터리 이름 오류",
    "dialog_create_new_dir_warning_empty_text": "디렉터리 이름은 비워둘 수 없습니다",
    "dialog_create_new_dir_warning_too_long_title": "새 디렉터리 이름 오류",
    "dialog_create_new_dir_warning_too_long_text": "디렉터리 이름이 너무 깁니다. 최대 "
                                                   "{symbols} 자까지 허용됩니다!",
    "dialog_create_new_dir_error_existed": "디렉터리가 이미 존재합니다",
    "dialog_create_new_dir_error": "디렉터리를 만들 수 없습니다. 대상 디렉터리 "
                                   "{base_dir} 이 쓰기 가능한지 확인하십시오",

    "dialog_message_box_title": "메시지",
    "dialog_message_box_button_ok": "닫기",

    "action_new_file_first_line_template_text": "새 문서",
    "action_open_file_dialog_caption": "파일 열기",
    "action_save_as_file_dialog_caption": "파일 저장",

    "dialog_save_empty_file_title": "빈 파일 저장",
    "dialog_save_empty_file_text": "내용이 없는 파일을 저장하시겠습니까?",

    "dialog_encrypt_file_title": "파일 암호화",
    "dialog_encrypt_file_text": "파일 \"{file_name}\"을(를) 암호화하시겠습니까?",
    "encrypt_file_warning_file_is_already_encrypted": "파일이 이미 암호화되었습니다!",
    "dialog_encrypt_file_rewrite_existing_title": "기존 파일 덮어쓰기",
    "dialog_encrypt_file_rewrite_existing_text": "기존 파일 \"{file_path}\"을(를) 덮어쓰시겠습니까?",

    "dialog_decrypt_file_title": "파일 복호화",
    "dialog_decrypt_file_text": "파일 \"{file_name}\"을(를) 복호화하시겠습니까?",
    "decrypt_file_warning_file_is_not_encrypted": "파일이 암호화되지 않았습니다!",
    "dialog_decrypt_file_rewrite_existing_title": "기존 파일 덮어쓰기",
    "dialog_decrypt_file_rewrite_existing_text": "기존 파일 \"{file_path}\"을(를) 덮어쓰시겠습니까?",

    "dialog_encrypt_new_password_title": "새 비밀번호",
    "dialog_encrypt_new_password_label": "비밀번호:",
    "dialog_encrypt_new_password_input_placeholder_text": "새 비밀번호 입력",
    "dialog_encrypt_new_password_hint_label": "힌트:",
    "dialog_encrypt_new_password_hint_label_description": "힌트는 암호화되지 않으며 파일에서 읽을 수 있습니다!"
                                                          "\n생일 등 쉽게 추측할 수 있는 힌트를 사용하지 마세요."
                                                          "\n관련 없는 참조를 사용해 보세요.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "힌트 입력(선택 사항)",
    "dialog_encrypt_new_password_button_ok": "확인",
    "dialog_encrypt_new_password_button_cancel": "취소",
    "dialog_encrypt_new_password_warning_empty_title": "경고",
    "dialog_encrypt_new_password_warning_empty_text": "비밀번호 필드는 비워 둘 수 없습니다!",
    "dialog_encrypt_new_password_warning_too_long_title": "경고",
    "dialog_encrypt_new_password_warning_too_long_text": "힌트 필드가 너무 깁니다, 최대 {symbols}개의 기호!",

    "dialog_encrypt_password_title": "비밀번호 입력",
    "dialog_encrypt_password_label": "비밀번호:",
    "dialog_encrypt_password_input_placeholder_text": "비밀번호 입력",
    "dialog_encrypt_password_hint_label": "힌트:",
    "dialog_encrypt_password_button_ok": "확인",
    "dialog_encrypt_password_button_cancel": "취소",

    "dialog_encrypt_password_reset_title": "암호화 비밀번호 재설정",
    "dialog_encrypt_password_reset_text": "현재 암호화 비밀번호를 재설정하시겠습니까?",
    "dialog_encrypt_password_reset_button_cancel": "취소",
    "dialog_encrypt_password_reset_button_yes": "예",

    "dialog_open_link_title": "링크",
    "dialog_open_link_text": "링크 \"{url}\"을(를) 브라우저에서 열겠습니까?",

    "dialog_reset_settings_title": "설정을 재설정하시겠습니까?",
    "dialog_reset_settings_text": "설정에 저장된 모든 데이터가 삭제되며, 변경 사항을 적용하기 위해 앱이 재시작됩니다.",

    "dialog_exit_unsaved_title": "종료 확인",
    "dialog_exit_unsaved_text": "열린 파일 '{file_name}'을(를) 저장할 수 없습니다. 종료하시겠습니까?",

    "message_app_config_file_access": "{file_path}에서 앱 구성 파일에 접근할 때 권한이 거부되었습니다. "
                                      "제대로된 작동을 보장하기 위해 올바른 권한을 설정하세요.",

    "field_dir_path_dialog_caption": "디렉토리 선택",
    "field_file_path_dialog_caption": "파일 선택",

    "dialog_select_default_dir_title": "기본 폴더 선택",
    "dialog_select_default_dir_label": "노트를 위한 기본 폴더를 선택하세요",
    "dialog_select_default_dir_input_placeholder_text": "기본 노트 폴더",
    "dialog_select_default_dir_button_ok": "선택",
    "dialog_select_default_dir_button_cancel": "취소",

    "load_file_encryption_password_mismatch": "암호화 비밀번호가 일치하지 않습니다!",
    "load_file_encryption_password_incorrect": "암호화 비밀번호가 잘못되었습니다!",
    "load_file_none_content_error": "파일을 로드할 수 없습니다.",

    "open_dir_permission_error": "디렉토리에 접근할 수 없습니다.",
    "open_file_permission_error": "파일에 접근할 권한이 거부되었습니다.",
    "rename_file_permission_error": "파일 이름을 변경할 권한이 거부되었습니다.",

    "action_new_file_error_occurred": "파일을 생성할 수 없습니다; 오류가 발생했습니다。\n파일 시스템 권한을 확인하십시오。",
    "save_active_file_error_occurred": "파일을 저장할 수 없습니다; 오류가 발생했습니다。",

    "expandable_block_default_title": "추가 정보...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> 블록 열기/닫기 태그 불일치",

    "dialog_color_picker_color_copied_to_the_clipboard": "서식이 지정된 텍스트가 클립보드에 복사되었습니다",

    "popup_about_title": "애플리케이션 정보",
    "popup_about_app_name_description": "파이썬 마크다운 에디터",

    "popup_about_version": "버전",
    "popup_about_license": "라이선스",
    "popup_about_website": "웹사이트",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "날짜",

    "update_helper_new_version_is_available": "앱의 새 버전 {latest_version}을(를) 사용할 수 있습니다.",
    "update_helper_latest_version_installed": "앱의 최신 버전이 설치되었습니다",

    "network_connection_error_empty": "응답 정보를 가져올 수 없습니다",
    "network_connection_error_connection_or_dns":
        "호스트를 찾을 수 없습니다. 인터넷 연결 또는 DNS에 문제가 있을 수 있습니다.",
    "network_connection_error_connection_refused":
        "연결이 거부되었습니다. 서버가 다운되었거나 네트워크에 문제가 있을 수 있습니다.",
    "network_connection_error_connection_timed_out": "연결 시간 초과. 네트워크에 문제가 있을 수 있습니다.",
    "network_connection_error_connection_404_error":
        "404 연결 오류. 요청한 페이지 또는 리소스를 찾을 수 없습니다.",
    "network_connection_error_generic_with_status_code": "상태 코드 {status_code}으로 요청 실패",
}
