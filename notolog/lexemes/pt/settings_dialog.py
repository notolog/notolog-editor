# Portuguese lexemes settings_dialog.py
lexemes = {
    # Configurações
    "window_title": "Configurações",

    "button_close": "Fechar",

    "tab_general": "Geral",
    "tab_workspace": "Área de trabalho",
    "tab_ai_config": "Configuração de IA",

    "general_app_config_label": "Configuração do aplicativo",
    "general_app_language_label": "Idioma",
    "general_app_language_combo_placeholder_text": "Escolher um idioma",
    "general_app_language_combo_accessible_description": "Idioma da interface do aplicativo",
    "general_app_theme_label": "Tema",
    "general_app_theme_combo_placeholder_text": "Escolher um tema",
    "general_app_theme_combo_accessible_description": "Tema da interface do aplicativo",
    "general_app_default_path_label": "Pasta padrão para notas",
    "general_app_default_path_input_accessible_description": "Especifique a pasta padrão onde as notas serão armazenadas",
    "general_app_default_path_input_placeholder_text": "Selecione ou insira um caminho de pasta",
    "general_app_elements_visibility_label": "Gerenciar visibilidade dos elementos",
    "general_app_main_menu_label": "Menu Principal",
    "general_app_main_menu_checkbox": "Mostrar menu principal",
    "general_app_main_menu_checkbox_accessible_description": "Exibir o menu dropdown principal do aplicativo",
    "general_app_font_size_label": "Tamanho da fonte: {size}pt",
    "general_app_font_size_slider_accessible_description": "Ajustar o tamanho da fonte global do aplicativo",

    "general_file_deletion_label": "Exclusão de arquivos",
    "general_reversible_file_deletion_checkbox": "Excluir arquivos de forma reversível",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Mover arquivos excluídos para a lixeira do Notolog adicionando uma extensão .del",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Mostrar Posição Global do Cursor",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Exibir a posição global do cursor na barra de status",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Mostrar setas de navegação",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Exibir as setas de navegação na barra de status",

    "workspace_editor_mode_label": "Modo de edição",
    "workspace_editor_mode_show_line_numbers_checkbox": "Mostrar Números de Linha",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Exibir números de linha no editor",

    "workspace_view_mode_label": "Modo de visualização",
    "workspace_view_mode_process_emojis_checkbox": "Converter Emojis de Texto em Gráficos",
    "workspace_view_mode_process_emojis_checkbox_accessible_description":
        "Converter emojis de texto em representações gráficas",
    "workspace_view_mode_highlight_todos_checkbox": "Destacar TODOs",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Destacar tags TODO no texto",
    "workspace_view_mode_open_link_confirmation_checkbox": "Requerer Confirmação para Abrir Links",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Solicitar confirmação antes de abrir links",
    "workspace_view_mode_save_resources_checkbox": "Salvar automaticamente imagens externas no disco",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
        "Salva automaticamente cópias de imagens externas no disco para acesso offline.",

    "ai_config_inference_module_label": "Módulo de Inferência",
    "ai_config_inference_module_names_combo_label": "Módulo de Inferência Ativo",
    "ai_config_inference_module_names_combo_placeholder_text": "Escolher Módulo",
    "ai_config_inference_module_names_combo_accessible_description":
        "Selecione dentre os módulos de inferência de IA disponíveis para operar com o Assistente de IA.\n"
        "As opções incluem Modelos de Linguagem de Grande Porte (LLM) com processamento em tempo real,\n"
        "ou funcionalidades baseadas em API.",

    "ai_config_base_label": "Parâmetros Base",
    "ai_config_multi_turn_dialogue_checkbox": "Diálogo de múltiplas interações com memória conversacional",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Ative um diálogo de múltiplas interações que retém a última mensagem para memória conversacional.\n"
        "Quando desativado, apenas a nova mensagem e o prompt do sistema influenciam a resposta.",
    "ai_config_convert_to_md_checkbox": "Converter o resultado para Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Converta a mensagem de saída para o formato Markdown.",
    "workspace_bottom_bar_label": "Barra inferior",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Mostrar gráficos de CPU e memória",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Mostrar gráficos de uso de CPU e memória e o separador na barra inferior",
    "workspace_bottom_bar_system_load_interval_ms_label": "Intervalo de atualização dos gráficos",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Definir a frequência de leitura do uso de CPU e memória em milissegundos",
}
