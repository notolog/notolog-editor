# Chinese lexemes common.py
lexemes = {
    "app_title": "Notolog 编辑器",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "文件过滤器字段",

    "menu_action_copy_file_path": "复制文件路径",
    "menu_action_rename": "重命名",
    "menu_action_delete": "删除",
    "menu_action_delete_completely": "彻底删除",
    "menu_action_restore": "恢复",
    "menu_action_create_new_dir": "创建新目录",

    "dialog_file_rename_title": "重命名文件",
    "dialog_file_rename_field_label": "输入新的文件名",
    "dialog_file_rename_button_ok": "重命名",
    "dialog_file_rename_warning_exists": "同名文件已经存在",

    "dialog_file_delete_title": "删除文件",
    "dialog_file_delete_text": "删除文件 \"{file_name}\"?",
    "dialog_file_delete_completely_title": "彻底删除文件",
    "dialog_file_delete_completely_text": "彻底删除文件 \"{file_name}\" 吗？",
    "dialog_file_delete_error": "无法删除文件，发生错误",
    "dialog_file_delete_error_not_found": "文件未找到",

    "dialog_file_restore_title": "恢复文件",
    "dialog_file_restore_text": "恢复文件 \"{file_name}\"?",
    "dialog_file_restore_error": "无法恢复文件，发生错误",
    "dialog_file_restore_warning_exists": "{file_name} 名称的文件已存在",

    "dialog_create_new_dir_title": "创建新目录",
    "dialog_create_new_dir_label": "新目录名称",
    "dialog_create_new_dir_input_placeholder_text": "输入目录名称",
    "dialog_create_new_dir_button_ok": "创建",
    "dialog_create_new_dir_button_cancel": "取消",
    "dialog_create_new_dir_warning_empty_title": "新目录名称错误",
    "dialog_create_new_dir_warning_empty_text": "目录名称不能为空",
    "dialog_create_new_dir_warning_too_long_title": "新目录名称错误",
    "dialog_create_new_dir_warning_too_long_text": "目录名称太长；最大允许 {symbols} 个字符！",
    "dialog_create_new_dir_error_existed": "目录已存在",
    "dialog_create_new_dir_error": "无法创建目录。请确保目标目录 {base_dir} 可写",

    "dialog_message_box_title": "消息",
    "dialog_message_box_button_ok": "关闭",

    "action_new_file_first_line_template_text": "新文档",
    "action_open_file_dialog_caption": "打开文件",
    "action_save_as_file_dialog_caption": "保存文件",

    "dialog_save_empty_file_title": "保存空文件",
    "dialog_save_empty_file_text": "允许保存空内容的文件吗？",

    "dialog_encrypt_file_title": "加密文件",
    "dialog_encrypt_file_text": "加密文件 \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "文件已经加密!",
    "dialog_encrypt_file_rewrite_existing_title": "重写现有文件",
    "dialog_encrypt_file_rewrite_existing_text": "重写现有文件 \"{file_path}\"?",

    "dialog_decrypt_file_title": "解密文件",
    "dialog_decrypt_file_text": "解密文件 \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "文件未加密!",
    "dialog_decrypt_file_rewrite_existing_title": "重写现有文件",
    "dialog_decrypt_file_rewrite_existing_text": "重写现有文件 \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "新密码",
    "dialog_encrypt_new_password_label": "密码：",
    "dialog_encrypt_new_password_input_placeholder_text": "输入新密码",
    "dialog_encrypt_new_password_hint_label": "提示：",
    "dialog_encrypt_new_password_hint_label_description": "提示信息未加密并且可以从文件中读取！"
                                                          "\n不要使用容易被猜到的提示，例如"
                                                          "\n生日等。尝试使用不容易与您关联的参考。",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "输入提示（可选）",
    "dialog_encrypt_new_password_button_ok": "确定",
    "dialog_encrypt_new_password_button_cancel": "取消",
    "dialog_encrypt_new_password_warning_empty_title": "警告",
    "dialog_encrypt_new_password_warning_empty_text": "密码字段不能为空！",
    "dialog_encrypt_new_password_warning_too_long_title": "警告",
    "dialog_encrypt_new_password_warning_too_long_text": "提示字段太长，最多{symbols}个字符！",

    "dialog_encrypt_password_title": "输入密码",
    "dialog_encrypt_password_label": "密码：",
    "dialog_encrypt_password_input_placeholder_text": "输入密码",
    "dialog_encrypt_password_hint_label": "提示：",
    "dialog_encrypt_password_button_ok": "确定",
    "dialog_encrypt_password_button_cancel": "取消",

    "dialog_encrypt_password_reset_title": "重置加密密码",
    "dialog_encrypt_password_reset_text": "您确定要重置当前加密密码吗？",
    "dialog_encrypt_password_reset_button_cancel": "取消",
    "dialog_encrypt_password_reset_button_yes": "是",

    "dialog_open_link_title": "链接",
    "dialog_open_link_text": "在浏览器中打开链接 \"{url}\"?",

    "dialog_reset_settings_title": "重置设置？",
    "dialog_reset_settings_text": "将清除设置中的所有存储数据，并将重新启动应用程序以应用更改。",

    "field_dir_path_line_edit": "选择目录",

    "load_file_encryption_password_mismatch": "加密密码不匹配!",
    "load_file_encryption_password_incorrect": "加密密码错误!",
    "load_file_none_content_error": "无法加载文件。",

    "save_active_file_error_occurred": "无法保存文件，发生错误",

    "expandable_block_default_title": "更多信息...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> 块打开/关闭标记不匹配",

    "dialog_color_picker_color_copied_to_the_clipboard": "格式化文本已复制到剪贴板",

    "popup_about_title": "应用信息",
    "popup_about_app_name_description": "Python Markdown 编辑器",

    "popup_about_version": "版本",
    "popup_about_license": "许可证",
    "popup_about_website": "网站",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "日期",

    "update_helper_new_version_is_available": "应用的新版本 {latest_version} 现已可用",
    "update_helper_latest_version_installed": "应用的最新版本已安装",

    "network_connection_error_empty": "无法获取响应信息",
    "network_connection_error_connection_or_dns":
        "未找到主机。可能是互联网连接或DNS出现问题。",
    "network_connection_error_connection_refused":
        "连接被拒绝。服务器可能已关闭或存在网络问题。",
    "network_connection_error_connection_timed_out": "连接超时。可能存在网络问题。",
    "network_connection_error_connection_404_error":
        "404连接错误。未找到请求的页面或资源。",
    "network_connection_error_generic_with_status_code": "请求失败，状态码：{status_code}",
}
