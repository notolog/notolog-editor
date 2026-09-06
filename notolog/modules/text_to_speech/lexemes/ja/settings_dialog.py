# Japanese lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "テキスト読み上げを有効にする",
    "module_text_to_speech_config_setup_label": "音声の設定",
    "module_text_to_speech_config_runtime_label": "音声ランタイム",
    "module_text_to_speech_config_model_directory_label": "モデルフォルダー",
    "module_text_to_speech_config_tokenizer_directory_label": "トークナイザー",
    "module_text_to_speech_config_details_label": "詳細",
    "module_text_to_speech_config_model_license_label": "モデルのライセンス",
    "module_text_to_speech_config_download_models_button": "モデルをダウンロード",
    "module_text_to_speech_config_verify_models_button": "モデルを検証",
    "module_text_to_speech_config_cancel_button": "キャンセル",
    "module_text_to_speech_config_stop_button": "停止",
    "module_text_to_speech_config_custom_models_label": "カスタムモデルファイル",
    "module_text_to_speech_config_reading_label": "読み上げ",
    "module_text_to_speech_config_language_label": "言語",
    "module_text_to_speech_config_voice_label": "音声",
    "module_text_to_speech_config_speed_label": "速度",
    "module_text_to_speech_config_announce_headings_label": "見出しレベルを読み上げる",
    "module_text_to_speech_config_skip_inline_code_label": "インラインコードをスキップ",
    "module_text_to_speech_config_skip_multiline_code_label": "複数行コードをスキップ",
    "module_text_to_speech_config_test_voice_button": "音声をテスト",
    "module_text_to_speech_config_runtime_input_placeholder_text": "実行ファイルを選択…",
    "module_text_to_speech_config_model_input_placeholder_text": "自動",
    "module_text_to_speech_config_get_runtime_link": "ランタイム {version} を入手",
    "module_text_to_speech_config_about_label": "{title}について",
    "module_text_to_speech_config_choose_path_label": "{title}を選択",
    "module_text_to_speech_config_status_checking_runtime": "音声ランタイムを確認中…",
    "module_text_to_speech_config_status_checking_models": "キャッシュを確認し、不足するモデルをダウンロード中…",
    "module_text_to_speech_config_status_models_verified": "既存のモデルを検証しました。読み上げ準備完了。",
    "module_text_to_speech_config_status_models_downloaded": "モデルをダウンロードして検証しました。読み上げ準備完了。",
    "module_text_to_speech_config_status_models_found": "モデルが見つかりました。検証または音声テストを行ってください。",
    "module_text_to_speech_config_status_models_missing": "モデルが必要です。音声をダウンロードしてください。",
    "module_text_to_speech_config_status_runtime_missing": "ランタイムが必要です。実行ファイルを選ぶか入手してください。",
    "module_text_to_speech_config_status_download_cancelled": "キャンセルしました。完了したダウンロードは保存されます。再試行してください。",
    "module_text_to_speech_config_error_permission_denied": "アクセスが拒否されました。書き込み可能なモデルフォルダーを選び、権限を確認してください。",
    "module_text_to_speech_config_error_file_access": "ファイルにアクセスできません：{error}。詳細をご覧ください。",
    "module_text_to_speech_config_progress_elapsed": "経過時間 {time}",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 ファイル完了",
    "module_text_to_speech_config_progress_downloading": "ファイル {number}/3 · {role}をダウンロード中 · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "キャッシュ内の {count}/3 モデルファイルを検証済み…",
    "module_text_to_speech_config_progress_verifying": "ファイル {number}/3 · ダウンロードを検証中…",
    "module_text_to_speech_config_download_role_voice": "音声モデル",
    "module_text_to_speech_config_download_role_codec": "音声デコーダー",
    "module_text_to_speech_config_download_role_tokenizers": "トークナイザー",
    "module_text_to_speech_config_download_role_model": "モデル",
    "module_text_to_speech_config_runtime_required": "先に音声ランタイムを選択してください。",
    "module_text_to_speech_config_models_required": "先にモデルをダウンロードしてください。",
    "module_text_to_speech_config_enable_required": "先にテキスト読み上げを有効にしてください。",
    "module_text_to_speech_config_status_testing_voice": "モデルを読み込み、テスト音声を準備中…",
    "module_text_to_speech_config_details_accessible_description": "操作ログを表示／非表示",
    "module_text_to_speech_config_setup_accessible_description": (
        "NeMo-Speech.cpp を選択し、MagpieTTS、NanoCodec、トークナイザーをダウンロードします。モデルには別のライセンスが適用されます。"
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "NeMo-Speech.cpp 0.1.0 が必要です。アーカイブを展開し、bin/nemo-speech（Windows では bin/nemo-speech.exe）を選択します。"
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "モデルはここに保存されます。既存のファイルは検証して再利用します。curl と約550 MBの空き容量が必要です。"
    ),
    "module_text_to_speech_config_custom_models_accessible_description": "モデルのパスを指定するか、空欄にしてモデルフォルダーを使用します。",
    "module_text_to_speech_config_reading_accessible_description": "音声、言語、速度を選択します。コードの代わりに短い音声ラベルを読み上げられます。",
    "module_text_to_speech_config_language_input_accessible_description": (
        "文書の言語を選択します。自動検出は行いません。既定は英語です。標準中国語と日本語には、対応する機能を有効にしてビルドしたランタイムが必要です。"
    ),
    "module_text_to_speech_config_voice_input_accessible_description": "MagpieTTS の音声：John、Sofia、Aria、Jason、Leo。",
    "module_text_to_speech_config_speed_input_accessible_description": "再生速度を変えると声の高さも変わります。",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Markdown と HTML の見出しレベル1～4は Chapter、Section、Subsection、Sub-subsection、5～6は Heading level 5–6 "
        "と読み上げます。"
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "オン：「Inline code block」と読み上げます。オフ：インラインコードを読みます。フェンス付き・インデント付きコードには複数行設定を使います。"
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "オン：「Multiline code block」と読み上げます。オフ：フェンス付き・インデント付きコードを読みます。"
    ),
    "module_text_to_speech_config_verify_models_accessible_description": "既存ファイルを検証し、不足または破損したファイルをダウンロードします。",
    "module_text_to_speech_config_editor_required": "音声をテストするには、エディターからこの設定を開いてください。",
    "module_text_to_speech_config_context_length_label": "コンテキスト長",
    "module_text_to_speech_config_context_whole_document": "文書全体",
    "module_text_to_speech_config_context_characters": "{count} 文字",
    "module_text_to_speech_config_context_length_accessible_description": (
        "音声リクエストごとの最大文字数。右端は見出しの間を保った文書全体です。長いコンテキストは開始までの時間とメモリ使用量が増えます。ランタイムの制限は引き続き適用されます。"
    ),
    "module_text_to_speech_config_cancel_download_title": "ダウンロードをキャンセルしますか？",
    "module_text_to_speech_config_cancel_download_confirmation": "設定を閉じるとダウンロードがキャンセルされます。完了したファイルは保持されます。設定を閉じますか？",
    "module_text_to_speech_config_status_custom_models": "カスタムモデルファイルが選択されています。ダウンロードにはモデルフォルダーが使われます。",
}
