scheme = {
    "get_sergant": "SELECT * FROM newschema2.kurs WHERE `rank` = 'с-т';",
    "get_kursant_boy": "SELECT * FROM newschema2.kurs WHERE `rank` = 'сол.' AND `sex` = 'Чоловік';",
    "get_girl": "SELECT * FROM newschema2.kurs WHERE `rank` = 'сол.' AND `sex` = 'Жінка';"
}

big_naryad = {
    "ЧК": (1, "get_sergant"),
    "ДК": (2, "get_kursant_boy"),
    "ДЖГ": (1, "get_girl"),
    "ЧНК": (1, "get_sergant"),
    "ПЧНК": (3, "get_kursant_boy"),
    "Ст.ЧП": (1, "get_kursant_boy"),
    "ЧП": (9, "get_kursant_boy")
}
small_naryad = {
    "ЧК": (1, "get_sergant"),
    "ДК": (2, "get_kursant_boy"),
    "ДЖГ": (1, "get_girl")
}

DATA_COURCES = {  # день великих нарядів
    "26.02": "C0",
    "27.02": "C1",
    "28.02": "C2",
    "29.02": "C0",
    "01.03": "C1",
    "02.03": "C2",
    "03.03": "MK"
}

ENTER_BD = {
    "ЧК": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ДК": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ДЖГ": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ЧНК": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ПЧНК": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "Ст.ЧП": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1 WHERE `pib` = {pib};",
    "ЧП": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1 WHERE `pib` = {pib};",

    # субота
    "ЧК1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1 WHERE `pib` = {pib};",
    "ДК1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ДЖГ1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ЧНК1": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ПЧНК1": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "Ст.ЧП1": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1,`chepe_sb` = `chepe_sb` + 1  WHERE `pib` = {pib};",
    "ЧП1": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1,`chepe_sb` = `chepe_sb` + 1  WHERE `pib` = {pib};"

}
