# Finnish lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Ota puhe käyttöön",
    "module_text_to_speech_config_setup_label": "Äänen asetukset",
    "module_text_to_speech_config_runtime_label": "Puhemoottori",
    "module_text_to_speech_config_model_directory_label": "Mallikansio",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenisoijat",
    "module_text_to_speech_config_details_label": "Tiedot",
    "module_text_to_speech_config_model_license_label": "Mallin lisenssi",
    "module_text_to_speech_config_download_models_button": "Lataa mallit",
    "module_text_to_speech_config_verify_models_button": "Tarkista mallit",
    "module_text_to_speech_config_cancel_button": "Peruuta",
    "module_text_to_speech_config_stop_button": "Pysäytä",
    "module_text_to_speech_config_custom_models_label": "Omat mallitiedostot",
    "module_text_to_speech_config_reading_label": "Lukeminen",
    "module_text_to_speech_config_language_label": "Kieli",
    "module_text_to_speech_config_voice_label": "Ääni",
    "module_text_to_speech_config_speed_label": "Nopeus",
    "module_text_to_speech_config_announce_headings_label": "Ilmoita otsikot",
    "module_text_to_speech_config_skip_inline_code_label": "Ohita rivinsisäinen koodi",
    "module_text_to_speech_config_skip_multiline_code_label": "Ohita monirivinen koodi",
    "module_text_to_speech_config_test_voice_button": "Kokeile ääntä",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Valitse ohjelmatiedosto…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automaattinen",
    "module_text_to_speech_config_get_runtime_link": "Hanki moottori {version}",
    "module_text_to_speech_config_about_label": "Tietoja: {title}",
    "module_text_to_speech_config_choose_path_label": "Valitse {title}",
    "module_text_to_speech_config_status_checking_runtime": "Tarkistetaan puhemoottoria…",
    "module_text_to_speech_config_status_checking_models": "Tarkistetaan välimuistia ja ladataan puuttuvia malleja…",
    "module_text_to_speech_config_status_models_verified": "Nykyiset mallit tarkistettu. Valmis lukemaan.",
    "module_text_to_speech_config_status_models_downloaded": "Mallit ladattu ja tarkistettu. Valmis lukemaan.",
    "module_text_to_speech_config_status_models_found": "Mallit löytyivät. Tarkista ne tai kokeile ääntä.",
    "module_text_to_speech_config_status_models_missing": "Mallit tarvitaan. Aloita lataamalla ääni.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Moottori tarvitaan. Valitse ohjelmatiedosto tai hanki moottori."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Peruutettu. Valmiit lataukset säilyvät; yritä uudelleen."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Käyttö estetty. Valitse kirjoitettava mallikansio ja tarkista oikeudet."
    ),
    "module_text_to_speech_config_error_file_access": "Tiedoston käyttö epäonnistui: {error}. Katso tiedot.",
    "module_text_to_speech_config_progress_elapsed": "Kulunut {time}",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 tiedostoa valmis",
    "module_text_to_speech_config_progress_downloading": "Tiedosto {number}/3 · Ladataan: {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 mallitiedostoa tarkistettu välimuistissa…",
    "module_text_to_speech_config_progress_verifying": "Tiedosto {number}/3 · Tarkistetaan latausta…",
    "module_text_to_speech_config_download_role_voice": "puhemalli",
    "module_text_to_speech_config_download_role_codec": "äänen dekooderi",
    "module_text_to_speech_config_download_role_tokenizers": "tokenisoijat",
    "module_text_to_speech_config_download_role_model": "malli",
    "module_text_to_speech_config_runtime_required": "Valitse ensin puhemoottori.",
    "module_text_to_speech_config_models_required": "Lataa ensin mallit.",
    "module_text_to_speech_config_enable_required": "Ota ensin puhe käyttöön.",
    "module_text_to_speech_config_status_testing_voice": "Ladataan malleja ja valmistellaan testiääntä…",
    "module_text_to_speech_config_details_accessible_description": "Näytä tai piilota toimintaloki",
    "module_text_to_speech_config_setup_accessible_description": (
        "Valitse NeMo-Speech.cpp ja lataa MagpieTTS, NanoCodec sekä tokenisoijat. Malleilla on erillinen"
        " lisenssi."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Vaatii NeMo-Speech.cpp 0.1.0:n. Pura arkisto ja valitse bin/nemo-speech (Windowsissa "
        "bin/nemo-speech.exe)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Mallit ladataan tähän. Nykyiset tiedostot tarkistetaan ja käytetään uudelleen. Vaatii curlin ja"
        " noin 550 Mt tilaa."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Korvaa mallien polut tai tyhjennä kentät käyttääksesi mallikansiota."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Valitse ääni, kieli ja nopeus. Koodi voidaan korvata lyhyellä puhutulla nimikkeellä."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Valitse asiakirjan kieli; sitä ei tunnisteta automaattisesti. Oletus on englanti. "
        "Mandariinikiina ja japani vaativat niitä tukevan moottorin."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS-äänet: John, Sofia, Aria, Jason ja Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": "Toistonopeus muuttaa myös äänenkorkeutta.",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Markdown- ja HTML-otsikoiden tasot 1–4 ilmoitetaan sanoilla Chapter, Section, Subsection ja "
        "Sub-subsection, sitten Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Valittu: sanoo “Inline code block”. Muuten lukee rivinsisäisen koodin. Rajattu ja sisennetty "
        "koodi käyttää moniriviasetusta."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Valittu: sanoo “Multiline code block”. Muuten lukee rajatun ja sisennetyn koodin."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Tarkista nykyiset tiedostot ja lataa puuttuvat tai vaurioituneet."
    ),
    "module_text_to_speech_config_editor_required": "Avaa nämä asetukset editorista kokeillaksesi ääntä.",
    "module_text_to_speech_config_context_length_label": "Kontekstin pituus",
    "module_text_to_speech_config_context_whole_document": "Koko asiakirja",
    "module_text_to_speech_config_context_characters": "{count} merkkiä",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Merkkien enimmäismäärä puhepyynnössä. Oikea ääriasento: koko asiakirja otsikkotauot säilyttäen."
        " Suuri konteksti lisää aloitusviivettä ja muistinkäyttöä. Moottorin rajoitukset ovat voimassa."
    ),
    "module_text_to_speech_config_cancel_download_title": "Peruutetaanko lataus?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Asetusten sulkeminen peruuttaa latauksen. Valmiit tiedostot säilytetään. Suljetaanko asetukset?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Mukautetut mallitiedostot on valittu. Lataukset käyttävät mallikansiota."
    ),
}
