# Portuguese lexemes common.py
lexemes = {
    "app_title": "Editor Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Campo de filtro de arquivo",

    "menu_action_copy_file_path": "Copiar caminho do arquivo",
    "menu_action_rename": "Renomear",
    "menu_action_delete": "Excluir",
    "menu_action_delete_completely": "Excluir completamente",
    "menu_action_restore": "Restaurar",
    "menu_action_create_new_dir": "Criar um novo diretório",

    "dialog_file_rename_title": "Renomear arquivo",
    "dialog_file_rename_field_label": "Digite o novo nome do arquivo",
    "dialog_file_rename_button_ok": "Renomear",
    "dialog_file_rename_warning_exists": "Já existe um arquivo com o mesmo nome",

    "dialog_file_delete_title": "Excluir arquivo",
    "dialog_file_delete_text": "Excluir arquivo \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Excluir arquivo completamente",
    "dialog_file_delete_completely_text": "Excluir completamente o arquivo \"{file_name}\"?",
    "dialog_file_delete_error": "Não foi possível excluir o arquivo, ocorreu um erro",
    "dialog_file_delete_error_not_found": "Arquivo não encontrado",

    "dialog_file_restore_title": "Restaurar arquivo",
    "dialog_file_restore_text": "Restaurar o arquivo \"{file_name}\"?",
    "dialog_file_restore_error": "Não é possível restaurar o arquivo, ocorreu um erro",
    "dialog_file_restore_warning_exists": "Já existe um arquivo com o nome {file_name}",

    "dialog_create_new_dir_title": "Criar um novo diretório",
    "dialog_create_new_dir_label": "Nome do novo diretório",
    "dialog_create_new_dir_input_placeholder_text": "Digite o nome do diretório",
    "dialog_create_new_dir_button_ok": "Criar",
    "dialog_create_new_dir_button_cancel": "Cancelar",
    "dialog_create_new_dir_warning_empty_title": "Erro no nome do novo diretório",
    "dialog_create_new_dir_warning_empty_text": "O nome do diretório não pode estar vazio",
    "dialog_create_new_dir_warning_too_long_title": "Erro no nome do novo diretório",
    "dialog_create_new_dir_warning_too_long_text": "O nome do diretório é muito longo; máximo de "
                                                   "{symbols} caracteres permitidos!",
    "dialog_create_new_dir_error_existed": "O diretório já existe",
    "dialog_create_new_dir_error": "Não é possível criar o diretório. Certifique-se de que o diretório de destino "
                                   "{base_dir} seja gravável",

    "dialog_message_box_title": "Mensagem",
    "dialog_message_box_button_ok": "Fechar",

    "action_new_file_first_line_template_text": "Novo documento",
    "action_open_file_dialog_caption": "Abrir arquivo",
    "action_save_as_file_dialog_caption": "Salvar arquivo",

    "dialog_save_empty_file_title": "Salvar arquivo vazio",
    "dialog_save_empty_file_text": "Permitir salvar o arquivo com conteúdo vazio?",

    "dialog_encrypt_file_title": "Criptografar arquivo",
    "dialog_encrypt_file_text": "Criptografar arquivo \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "O arquivo já está criptografado!",
    "dialog_encrypt_file_rewrite_existing_title": "Sobrescrever arquivo existente",
    "dialog_encrypt_file_rewrite_existing_text": "Sobrescrever arquivo existente \"{file_path}\"?",

    "dialog_decrypt_file_title": "Descriptografar arquivo",
    "dialog_decrypt_file_text": "Descriptografar arquivo \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "O arquivo não está criptografado!",
    "dialog_decrypt_file_rewrite_existing_title": "Sobrescrever arquivo existente",
    "dialog_decrypt_file_rewrite_existing_text": "Sobrescrever arquivo existente \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Nova senha",
    "dialog_encrypt_new_password_label": "Senha:",
    "dialog_encrypt_new_password_input_placeholder_text": "Digite a nova senha",
    "dialog_encrypt_new_password_hint_label": "Dica:",
    "dialog_encrypt_new_password_hint_label_description":
        "A dica não é criptografada e pode ser lida do arquivo!"
        "\nNão use dicas óbvias que possam ser adivinhadas, como"
        "\na data de nascimento, ou algo do tipo. Tente usar uma referência.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Digite uma dica (opcional)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Cancelar",
    "dialog_encrypt_new_password_warning_empty_title": "Aviso",
    "dialog_encrypt_new_password_warning_empty_text": "O campo de senha não pode ficar vazio!",
    "dialog_encrypt_new_password_warning_too_long_title": "Aviso",
    "dialog_encrypt_new_password_warning_too_long_text":
        "O campo de dica é muito longo, máximo de {symbols} caracteres!",

    "dialog_encrypt_password_title": "Digite a senha",
    "dialog_encrypt_password_label": "Senha:",
    "dialog_encrypt_password_input_placeholder_text": "Digite a senha",
    "dialog_encrypt_password_hint_label": "Dica:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Cancelar",

    "dialog_encrypt_password_reset_title": "Redefinir senha de criptografia",
    "dialog_encrypt_password_reset_text": "Você tem certeza que deseja redefinir a senha de criptografia atual?",
    "dialog_encrypt_password_reset_button_cancel": "Cancelar",
    "dialog_encrypt_password_reset_button_yes": "Sim",

    "dialog_open_link_title": "Link",
    "dialog_open_link_text": "Abrir link \"{url}\" no navegador?",

    "dialog_reset_settings_title": "Redefinir configurações?",
    "dialog_reset_settings_text":
        "Todos os dados armazenados nas configurações serão apagados, e o aplicativo será reiniciado para aplicar "
        "as mudanças.",

    "dialog_exit_unsaved_title": "Confirmar Saída",
    "dialog_exit_unsaved_text": "O arquivo aberto '{file_name}' não pode ser salvo. Continuar com a saída?",

    "message_app_config_file_access": "Permissão negada ao acessar o arquivo de configuração do aplicativo em {file_path}. "
                                      "Defina as permissões corretas para garantir a operação adequada.",

    "field_dir_path_dialog_caption": "Selecionar Diretório",
    "field_file_path_dialog_caption": "Selecionar Arquivo",

    "dialog_select_default_dir_title": "Selecionar Pasta Padrão",
    "dialog_select_default_dir_label": "Selecione a pasta padrão para notas",
    "dialog_select_default_dir_input_placeholder_text": "Pasta Padrão de Notas",
    "dialog_select_default_dir_button_ok": "Selecionar",
    "dialog_select_default_dir_button_cancel": "Cancelar",

    "load_file_encryption_password_mismatch": "Senha de criptografia não corresponde!",
    "load_file_encryption_password_incorrect": "Senha de criptografia incorreta!",
    "load_file_none_content_error": "Não foi possível carregar o arquivo.",

    "open_dir_permission_error": "Permissão negada ao acessar o diretório.",
    "open_file_permission_error": "Permissão negada ao acessar o arquivo.",
    "rename_file_permission_error": "Permissão negada ao renomear o arquivo.",

    "action_new_file_error_occurred": "Não é possível criar o arquivo; ocorreu um erro."
                                      "\nVerifique as permissões do sistema de arquivos.",
    "save_active_file_error_occurred": "Não é possível salvar o arquivo; ocorreu um erro.",

    "expandable_block_default_title": "Mais informações...",
    "expandable_block_open_close_tags_mismatch_warning":
        "Incompatibilidade das tags de abertura/fechamento do bloco <details>",

    "dialog_color_picker_color_copied_to_the_clipboard": "O texto formatado foi copiado para a área de transferência",

    "popup_about_title": "Informações do Aplicativo",
    "popup_about_app_name_description": "Editor de Markdown Python",

    "popup_about_version": "Versão",
    "popup_about_license": "Licença",
    "popup_about_website": "Site",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Data",

    "update_helper_new_version_is_available": "Nova versão {latest_version} do aplicativo disponível",
    "update_helper_latest_version_installed": "A versão mais recente do aplicativo está instalada",

    "network_connection_error_empty": "Não é possível obter informações de resposta",
    "network_connection_error_connection_or_dns":
        "Host não encontrado. Pode haver um problema com a conexão de internet ou DNS.",
    "network_connection_error_connection_refused":
        "Conexão recusada. O servidor pode estar inativo ou há problemas de rede.",
    "network_connection_error_connection_timed_out": "A conexão expirou. Pode haver problemas de rede.",
    "network_connection_error_connection_404_error":
        "Erro de conexão 404. A página ou recurso solicitado não foi encontrado.",
    "network_connection_error_generic_with_status_code": "Falha na solicitação com código de status: {status_code}",
}
