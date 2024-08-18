# Finnish lexemes common.py
lexemes = {
    "app_title": "Notolog Editori",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Tiedostosuodattimen kenttä",

    "menu_action_copy_file_path": "Kopioi tiedostopolku",
    "menu_action_rename": "Nimeä uudelleen",
    "menu_action_delete": "Poista",
    "menu_action_delete_completely": "Poista kokonaan",
    "menu_action_restore": "Palauta",
    "menu_action_create_new_dir": "Luo uusi hakemisto",

    "dialog_file_rename_title": "Nimeä tiedosto uudelleen",
    "dialog_file_rename_field_label": "Anna uusi tiedostonimi",
    "dialog_file_rename_button_ok": "Nimeä uudelleen",
    "dialog_file_rename_warning_exists": "Samanniminen tiedosto on jo olemassa",

    "dialog_file_delete_title": "Poista tiedosto",
    "dialog_file_delete_text": "Poista tiedosto \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Poista tiedosto kokonaan",
    "dialog_file_delete_completely_text": "Poista tiedosto \"{file_name}\" kokonaan?",
    "dialog_file_delete_error": "Tiedostoa ei voi poistaa, tapahtui virhe",
    "dialog_file_delete_error_not_found": "Tiedostoa ei löydy",

    "dialog_file_restore_title": "Palauta tiedosto",
    "dialog_file_restore_text": "Palauta tiedosto \"{file_name}\"?",
    "dialog_file_restore_error": "Tiedostoa ei voi palauttaa, tapahtui virhe",
    "dialog_file_restore_warning_exists": "Samanniminen tiedosto on jo olemassa",

    "dialog_create_new_dir_title": "Luo uusi hakemisto",
    "dialog_create_new_dir_label": "Uuden hakemiston nimi",
    "dialog_create_new_dir_input_placeholder_text": "Anna hakemiston nimi",
    "dialog_create_new_dir_button_ok": "Luo",
    "dialog_create_new_dir_button_cancel": "Peruuta",
    "dialog_create_new_dir_warning_empty_title": "Uuden hakemiston nimen virhe",
    "dialog_create_new_dir_warning_empty_text": "Hakemiston nimi ei voi olla tyhjä",
    "dialog_create_new_dir_warning_too_long_title": "Uuden hakemiston nimen virhe",
    "dialog_create_new_dir_warning_too_long_text": "Hakemiston nimi on liian pitkä; enintään "
                                                   "{symbols} merkkiä sallittu!",
    "dialog_create_new_dir_error_existed": "Hakemisto on jo olemassa",
    "dialog_create_new_dir_error": "Hakemistoa ei voi luoda. Varmista, että kohdehakemisto "
                                   "{base_dir} on kirjoitettavissa",

    "dialog_message_box_title": "Viesti",
    "dialog_message_box_button_ok": "Sulje",

    "action_new_file_first_line_template_text": "Uusi asiakirja",
    "action_open_file_dialog_caption": "Avaa tiedosto",
    "action_save_as_file_dialog_caption": "Tallenna tiedosto",

    "dialog_save_empty_file_title": "Tallenna tyhjä tiedosto",
    "dialog_save_empty_file_text": "Salli tiedoston tallentaminen ilman sisältöä?",

    "dialog_encrypt_file_title": "Salaa tiedosto",
    "dialog_encrypt_file_text": "Salaa tiedosto \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "Tiedosto on jo salattu!",
    "dialog_encrypt_file_rewrite_existing_title": "Kirjoita olemassa oleva tiedosto uudelleen",
    "dialog_encrypt_file_rewrite_existing_text": "Kirjoita olemassa oleva tiedosto \"{file_path}\" uudelleen?",

    "dialog_decrypt_file_title": "Pura tiedoston salaus",
    "dialog_decrypt_file_text": "Pura tiedoston salaus \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "Tiedosto ei ole salattu!",
    "dialog_decrypt_file_rewrite_existing_title": "Kirjoita olemassa oleva tiedosto uudelleen",
    "dialog_decrypt_file_rewrite_existing_text": "Kirjoita olemassa oleva tiedosto \"{file_path}\" uudelleen?",

    "dialog_encrypt_new_password_title": "Uusi salasana",
    "dialog_encrypt_new_password_label": "Salasana:",
    "dialog_encrypt_new_password_input_placeholder_text": "Anna uusi salasana",
    "dialog_encrypt_new_password_hint_label": "Vihje:",
    "dialog_encrypt_new_password_hint_label_description": "Vihje ei ole salattu ja sen voi lukea tiedostosta!"
                                                          "\nVältä ilmeisiä vihjeitä, joita voi helposti arvata, kuten "
                                                          "syntymäpäiviä."
                                                          "\nYritä käyttää viitettä, jota ei ole helppo yhdistää sinuun.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Anna vihje (valinnainen)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Peruuta",
    "dialog_encrypt_new_password_warning_empty_title": "Varoitus",
    "dialog_encrypt_new_password_warning_empty_text": "Salasanakenttä ei voi olla tyhjä!",
    "dialog_encrypt_new_password_warning_too_long_title": "Varoitus",
    "dialog_encrypt_new_password_warning_too_long_text": "Vihjekenttä on liian pitkä, enintään {symbols} merkkiä!",

    "dialog_encrypt_password_title": "Anna salasana",
    "dialog_encrypt_password_label": "Salasana:",
    "dialog_encrypt_password_input_placeholder_text": "Anna salasana",
    "dialog_encrypt_password_hint_label": "Vihje:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Peruuta",

    "dialog_encrypt_password_reset_title": "Nollaa salauksen salasana",
    "dialog_encrypt_password_reset_text": "Haluatko varmasti nollata nykyisen salauksen salasanan?",
    "dialog_encrypt_password_reset_button_cancel": "Peruuta",
    "dialog_encrypt_password_reset_button_yes": "Kyllä",

    "dialog_open_link_title": "Linkki",
    "dialog_open_link_text": "Avaa linkki \"{url}\" selaimessa?",

    "dialog_reset_settings_title": "Nollaa asetukset?",
    "dialog_reset_settings_text":
        "Kaikki asetuksissa tallennetut tiedot poistetaan, ja sovellus käynnistetään uudelleen muutosten soveltamiseksi.",

    "field_dir_path_line_edit": "Valitse hakemisto",

    "load_file_encryption_password_mismatch": "Salaussalasana ei täsmää!",
    "load_file_encryption_password_incorrect": "Väärä salaussalasana!",
    "load_file_none_content_error": "Tiedostoa ei voi ladata.",

    "save_active_file_error_occurred": "Tiedostoa ei voi tallentaa, tapahtui virhe",

    "expandable_block_default_title": "Lisätietoja...",
    "expandable_block_open_close_tags_mismatch_warning": "<details>-lohkon avaamis- ja sulkumerkkien epäjohdonmukaisuus",

    "dialog_color_picker_color_copied_to_the_clipboard": "Muotoiltu teksti on kopioitu leikepöydälle",

    "popup_about_title": "Sovelluksen tiedot",
    "popup_about_app_name_description": "Python Markdown -editori",

    "popup_about_version": "Versio",
    "popup_about_license": "Lisenssi",
    "popup_about_website": "Verkkosivusto",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Päivämäärä",

    "update_helper_new_version_is_available": "Sovelluksen uusi versio '{latest_version}' on saatavilla",
    "update_helper_latest_version_installed": "Sovelluksen uusin versio on asennettu",

    "network_connection_error_empty": "Vastausinformaatiota ei voi hankkia",
    "network_connection_error_connection_or_dns":
        "Isäntää ei löydy. Internet-yhteydessä tai DNS:ssä voi olla ongelma.",
    "network_connection_error_connection_refused":
        "Yhteys hylätty. Palvelin voi olla alhaalla tai verkossa voi olla ongelmia.",
    "network_connection_error_connection_timed_out": "Yhteys katkesi aikakatkaisun vuoksi. Verkossa voi olla ongelmia.",
    "network_connection_error_connection_404_error":
        "Yhteys 404 virhe. Pyydettyä sivua tai resurssia ei löydy.",
    "network_connection_error_generic_with_status_code": "Pyyntö epäonnistui tilakoodilla: {status_code}",
}
