# Japanese lexemes common.py
lexemes = {
    "app_title": "Notolog エディタ",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "ファイルフィルタフィールド",

    "menu_action_rename": "名前を変更",
    "menu_action_delete": "削除",
    "menu_action_delete_completely": "完全に削除",
    "menu_action_restore": "復元",

    "dialog_file_rename_title": "ファイル名の変更",
    "dialog_file_rename_field_label": "新しいファイル名を入力",
    "dialog_file_rename_button_ok": "名前を変更",
    "dialog_file_rename_warning_exists": "同名のファイルがすでに存在しています",

    "dialog_file_delete_title": "ファイルの削除",
    "dialog_file_delete_text": "ファイル \"{file_name}\" を削除しますか？",
    "dialog_file_delete_completely_title": "ファイルを完全に削除",
    "dialog_file_delete_completely_text": "ファイル「{file_name}」を完全に削除しますか？",
    "dialog_file_delete_error": "ファイルを削除できませんでした。エラーが発生しました",
    "dialog_file_delete_error_not_found": "ファイルが見つかりません",

    "dialog_file_restore_title": "ファイルを復元",
    "dialog_file_restore_text": "ファイル \"{file_name}\" を復元しますか？",
    "dialog_file_restore_error": "ファイルを復元できませんでした。エラーが発生しました",
    "dialog_file_restore_warning_exists": "{file_name} という名前のファイルがすでに存在します",

    "dialog_message_box_title": "メッセージ",
    "dialog_message_box_button_ok": "閉じる",

    "action_new_file_first_line_template_text": "新しいドキュメント",
    "action_open_file_dialog_caption": "ファイルを開く",
    "action_save_as_file_dialog_caption": "ファイルを保存",

    "dialog_save_empty_file_title": "空のファイルを保存",
    "dialog_save_empty_file_text": "内容が空のファイルを保存しますか？",

    "dialog_encrypt_file_title": "ファイルの暗号化",
    "dialog_encrypt_file_text": "ファイル \"{file_name}\" を暗号化しますか？",
    "encrypt_file_warning_file_is_already_encrypted": "ファイルはすでに暗号化されています！",
    "dialog_encrypt_file_rewrite_existing_title": "既存のファイルを上書き",
    "dialog_encrypt_file_rewrite_existing_text": "既存のファイル \"{file_path}\" を上書きしますか？",

    "dialog_decrypt_file_title": "ファイルの復号",
    "dialog_decrypt_file_text": "ファイル \"{file_name}\" を復号しますか？",
    "decrypt_file_warning_file_is_not_encrypted": "ファイルは暗号化されていません！",
    "dialog_decrypt_file_rewrite_existing_title": "既存のファイルを上書き",
    "dialog_decrypt_file_rewrite_existing_text": "既存のファイル \"{file_path}\" を上書きしますか？",

    "dialog_encrypt_new_password_title": "新しいパスワード",
    "dialog_encrypt_new_password_label": "パスワード：",
    "dialog_encrypt_new_password_input_placeholder_text": "新しいパスワードを入力",
    "dialog_encrypt_new_password_hint_label": "ヒント：",
    "dialog_encrypt_new_password_hint_label_description": "ヒントは暗号化されずにファイルから読み取ることができます！"
                                                          "\n誕生日など簡単に推測できるヒントは使用しないでください。"
                                                          "\n関連性の低い参照を使用してください。",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "ヒントを入力（オプション）",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "キャンセル",
    "dialog_encrypt_new_password_warning_empty_title": "警告",
    "dialog_encrypt_new_password_warning_empty_text": "パスワード欄は空にできません！",
    "dialog_encrypt_new_password_warning_too_long_title": "警告",
    "dialog_encrypt_new_password_warning_too_long_text": "ヒント欄が長すぎます。最大{symbols}文字です！",

    "dialog_encrypt_password_title": "パスワードを入力",
    "dialog_encrypt_password_label": "パスワード：",
    "dialog_encrypt_password_input_placeholder_text": "パスワードを入力",
    "dialog_encrypt_password_hint_label": "ヒント：",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "キャンセル",

    "dialog_encrypt_password_reset_title": "暗号化パスワードのリセット",
    "dialog_encrypt_password_reset_text": "現在の暗号化パスワードをリセットしますか？",
    "dialog_encrypt_password_reset_button_cancel": "キャンセル",
    "dialog_encrypt_password_reset_button_yes": "はい",

    "dialog_open_link_title": "リンク",
    "dialog_open_link_text": "リンク \"{url}\" をブラウザで開きますか？",

    "dialog_reset_settings_title": "設定をリセットしますか？",
    "dialog_reset_settings_text": "設定に保存されているすべてのデータがクリアされ、変更を適用するためにアプリが再起動されます。",

    "field_dir_path_line_edit": "ディレクトリを選択",

    "load_file_encryption_password_mismatch": "暗号化パスワードが一致しません！",
    "load_file_encryption_password_incorrect": "暗号化パスワードが正しくありません！",
    "load_file_none_content_error": "ファイルを読み込めません。",

    "save_active_file_error_occurred": "ファイルを保存できませんでした。エラーが発生しました",

    "expandable_block_default_title": "詳細情報...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> ブロックの開始/終了タグの不一致",

    "dialog_color_picker_color_copied_to_the_clipboard": "フォーマットされたテキストがクリップボードにコピーされました",

    "popup_about_title": "アプリ情報",
    "popup_about_app_name_description": "Python Markdown エディタ",

    "popup_about_version": "バージョン",
    "popup_about_license": "ライセンス",
    "popup_about_website": "ウェブサイト",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "日付",

    "update_helper_new_version_is_available": "アプリの新しいバージョン '{latest_version}' が利用可能です",
    "update_helper_latest_version_installed": "アプリの最新バージョンがインストールされています",

    "network_connection_error_empty": "応答情報を取得できません",
    "network_connection_error_connection_or_dns":
        "ホストが見つかりません。インターネット接続またはDNSに問題があるかもしれません。",
    "network_connection_error_connection_refused":
        "接続が拒否されました。サーバーがダウンしているか、ネットワークに問題がある可能性があります。",
    "network_connection_error_connection_timed_out": "接続がタイムアウトしました。ネットワークに問題があるかもしれません。",
    "network_connection_error_connection_404_error":
        "接続404エラー。要求されたページまたはリソースが見つかりません。",
    "network_connection_error_generic_with_status_code": "ステータスコード{status_code}でリクエストが失敗しました",
}
