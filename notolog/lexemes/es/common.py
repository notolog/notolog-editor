# Spanish lexemes common.py
lexemes = {
    "app_title": "Editor Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Campo de filtro de archivos",

    "menu_action_copy_file_path": "Copiar ruta del archivo",
    "menu_action_rename": "Renombrar",
    "menu_action_delete": "Eliminar",
    "menu_action_delete_completely": "Eliminar completamente",
    "menu_action_restore": "Restaurar",
    "menu_action_create_new_dir": "Crear un nuevo directorio",

    "dialog_file_rename_title": "Renombrar archivo",
    "dialog_file_rename_field_label": "Ingrese el nuevo nombre del archivo",
    "dialog_file_rename_button_ok": "Renombrar",
    "dialog_file_rename_warning_exists": "Ya existe un archivo con el mismo nombre",

    "dialog_file_delete_title": "Eliminar archivo",
    "dialog_file_delete_text": "¿Eliminar archivo \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Eliminar archivo completamente",
    "dialog_file_delete_completely_text": "¿Eliminar completamente el archivo \"{file_name}\"?",
    "dialog_file_delete_error": "No se puede eliminar el archivo, ocurrió un error",
    "dialog_file_delete_error_not_found": "Archivo no encontrado",

    "dialog_file_restore_title": "Restaurar archivo",
    "dialog_file_restore_text": "¿Restaurar el archivo \"{file_name}\"?",
    "dialog_file_restore_error": "No se puede restaurar el archivo, ocurrió un error",
    "dialog_file_restore_warning_exists": "Ya existe un archivo con el nombre {file_name}",

    "dialog_create_new_dir_title": "Crear un nuevo directorio",
    "dialog_create_new_dir_label": "Nombre del nuevo directorio",
    "dialog_create_new_dir_input_placeholder_text": "Ingrese el nombre del directorio",
    "dialog_create_new_dir_button_ok": "Crear",
    "dialog_create_new_dir_button_cancel": "Cancelar",
    "dialog_create_new_dir_warning_empty_title": "Error en el nombre del nuevo directorio",
    "dialog_create_new_dir_warning_empty_text": "El nombre del directorio no puede estar vacío",
    "dialog_create_new_dir_warning_too_long_title": "Error en el nombre del nuevo directorio",
    "dialog_create_new_dir_warning_too_long_text": "El nombre del directorio es demasiado largo; ¡máximo "
                                                   "{symbols} caracteres permitidos!",
    "dialog_create_new_dir_error_existed": "El directorio ya existe",
    "dialog_create_new_dir_error": "No se puede crear el directorio. Asegúrese de que el directorio de destino "
                                   "{base_dir} sea escribible",

    "dialog_message_box_title": "Mensaje",
    "dialog_message_box_button_ok": "Cerrar",

    "action_new_file_first_line_template_text": "Nuevo documento",
    "action_open_file_dialog_caption": "Abrir archivo",
    "action_save_as_file_dialog_caption": "Guardar archivo",

    "dialog_save_empty_file_title": "Guardar archivo vacío",
    "dialog_save_empty_file_text": "¿Permitir guardar el archivo con contenido vacío?",

    "dialog_encrypt_file_title": "Encriptar archivo",
    "dialog_encrypt_file_text": "¿Encriptar archivo \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "¡El archivo ya está encriptado!",
    "dialog_encrypt_file_rewrite_existing_title": "Reescribir archivo existente",
    "dialog_encrypt_file_rewrite_existing_text": "¿Reescribir archivo existente \"{file_path}\"?",

    "dialog_decrypt_file_title": "Desencriptar archivo",
    "dialog_decrypt_file_text": "¿Desencriptar archivo \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "¡El archivo no está encriptado!",
    "dialog_decrypt_file_rewrite_existing_title": "Reescribir archivo existente",
    "dialog_decrypt_file_rewrite_existing_text": "¿Reescribir archivo existente \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Nueva Contraseña",
    "dialog_encrypt_new_password_label": "Contraseña:",
    "dialog_encrypt_new_password_input_placeholder_text": "Introduzca la nueva contraseña",
    "dialog_encrypt_new_password_hint_label": "Pista:",
    "dialog_encrypt_new_password_hint_label_description":
        "¡La pista no está cifrada y puede ser leída desde el archivo! "
        "\nEvite pistas obvias que se puedan adivinar fácilmente, como fechas de nacimiento. "
        "\nIntente utilizar una referencia que no se asocie fácilmente con usted.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Introduzca una pista (opcional)",
    "dialog_encrypt_new_password_button_ok": "Aceptar",
    "dialog_encrypt_new_password_button_cancel": "Cancelar",
    "dialog_encrypt_new_password_warning_empty_title": "Advertencia",
    "dialog_encrypt_new_password_warning_empty_text": "¡El campo de contraseña no puede estar vacío!",
    "dialog_encrypt_new_password_warning_too_long_title": "Advertencia",
    "dialog_encrypt_new_password_warning_too_long_text":
        "El campo de la pista es demasiado largo, ¡máximo de {symbols} caracteres!",

    "dialog_encrypt_password_title": "Introducir Contraseña",
    "dialog_encrypt_password_label": "Contraseña:",
    "dialog_encrypt_password_input_placeholder_text": "Introducir contraseña",
    "dialog_encrypt_password_hint_label": "Pista:",
    "dialog_encrypt_password_button_ok": "Aceptar",
    "dialog_encrypt_password_button_cancel": "Cancelar",

    "dialog_encrypt_password_reset_title": "Restablecer Contraseña de Cifrado",
    "dialog_encrypt_password_reset_text": "¿Está seguro de querer restablecer la contraseña de cifrado actual?",
    "dialog_encrypt_password_reset_button_cancel": "Cancelar",
    "dialog_encrypt_password_reset_button_yes": "Sí",

    "dialog_open_link_title": "Enlace",
    "dialog_open_link_text": "¿Abrir enlace \"{url}\" en un navegador?",

    "dialog_reset_settings_title": "¿Restablecer configuraciones?",
    "dialog_reset_settings_text":
        "Todos los datos almacenados en las configuraciones serán borrados, y la aplicación se reiniciará para aplicar "
        "los cambios.",

    "field_dir_path_line_edit": "Seleccionar Directorio",

    "load_file_encryption_password_mismatch": "¡La contraseña de encriptación no coincide!",
    "load_file_encryption_password_incorrect": "¡Contraseña de encriptación incorrecta!",
    "load_file_none_content_error": "No se puede cargar el archivo.",

    "save_active_file_error_occurred": "No se puede guardar el archivo, ocurrió un error",

    "expandable_block_default_title": "Más información...",
    "expandable_block_open_close_tags_mismatch_warning":
        "Incompatibilidad de etiquetas de apertura/cierre del bloque <details>",

    "dialog_color_picker_color_copied_to_the_clipboard": "El texto formateado ha sido copiado al portapapeles",

    "popup_about_title": "Información de la Aplicación",
    "popup_about_app_name_description": "Editor Markdown de Python",

    "popup_about_version": "Versión",
    "popup_about_license": "Licencia",
    "popup_about_website": "Sitio Web",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Fecha",

    "update_helper_new_version_is_available": "Una nueva versión {latest_version} de la aplicación está disponible",
    "update_helper_latest_version_installed": "La última versión de la aplicación está instalada",

    "network_connection_error_empty": "No se puede obtener información de la respuesta",
    "network_connection_error_connection_or_dns":
        "Host no encontrado. Puede haber un problema con la conexión a internet o DNS.",
    "network_connection_error_connection_refused":
        "Conexión rechazada. El servidor podría estar caído o puede haber problemas de red.",
    "network_connection_error_connection_timed_out": "Tiempo de conexión agotado. Puede haber problemas de red.",
    "network_connection_error_connection_404_error":
        "Error de conexión 404. La página o recurso solicitado no se encuentra.",
    "network_connection_error_generic_with_status_code": "La solicitud falló con el código de estado: {status_code}",
}
