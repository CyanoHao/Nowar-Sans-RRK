import json
import codecs
import enum
import hashlib
from functools import reduce
from itertools import product


class Config:
    version = "0.8.1 TT"
    fontRevision = 0.0801
    vendor = "Nowar Typeface"
    vendorId = "NOWR"
    vendorUrl = "https://github.com/nowar-fonts"
    copyright = "Copyright © 2018—2020 Cyano Hao and Nowar Typeface, with Reserved Font Name “Nowar”, “Новар”, “Νοωαρ”, “有爱”, and “有愛”. Portions Copyright 2011 Google Inc. Portions © 2014-2019 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. Portions Copyright 2015-2020, Belleve Invis (belleve@typeof.net)."
    designer = "Cyano Hao (character set definition & modification for World of Warcraft); Monotype Design Team (Latin, Greek & Cyrillic); Ryoko NISHIZUKA 西塚涼子 (kana, bopomofo & ideographs); Sandoll Communications 산돌커뮤니케이션, Soo-young JANG 장수영 & Joo-yeon KANG 강주연 (hangul elements, letters & syllables); Dr. Ken Lunde (project architect, glyph set definition & overall production); Masataka HATTORI 服部正貴 (production & ideograph elements)"
    designerUrl = "https://github.com/CyanoHao"
    license = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This Font Software is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the SIL Open Font License for the specific language, permissions and limitations governing your use of this Font Software."
    licenseUrl = "https://scripts.sil.org/OFL"

    fontPackWeight = [300, 400, 500, 700]
    fontPackRegion = ["CN", "TW"]
    fontPackFeature = ["RRK"]
    # feature tags must be sorted alphabetically
    fontPackExportFeature = [
        ("CN", ["RRK"]),
        ("TW", ["RRK"]),
    ]


config = Config()


# define Chinese characters orthographies, and feature mods:
#
# base - common fonts, `FRIZQT__` and `ARIALN`; must be defined
# enUS - fonts for languages in Latin script, `skurri` and `MORPHEUS`
#        if set to something to be true, the orthography is considered to be same as `base`
#        if set to something to be false, fonts will be not overwritten
# ruRU - fonts for Русский; like `enUS`
# zhCN - fonts for 简体中文; can be false
# zhTW - fonts for 繁體中文; can be false
# koKR - fonts for 한국어; can be false
#
# xmod - a list of tuples of feature mod and related parameter list
# available mods:
#   PSimp - 伪简体, remap traditional Chinese characters to simplified ones in zhTW text, damage, and note font
#     base - also do remapping in common fonts (`FRIZQT__` and `ARIALN`)
#     chat - also do remapping in zhTW chat fonts (`arheiuhk_bd` for Battle and `bHEI01B` for Classic)
regionalVariant = {
    "CN": {
        "base": "CN",
        "enUS": True,
        "ruRU": None,
        "zhCN": "CN",
        "zhTW": None,
        "koKR": None,
    },
    "TW": {
        "base": "TW",
        "enUS": True,
        "ruRU": None,
        "zhCN": None,
        "zhTW": "TW",
        "koKR": None,
    },
}


class LanguageId(enum.IntEnum):
    enUS = 0x0409

    deAT = 0x0C07
    deCH = 0x0807
    deDE = 0x0407
    deLI = 0x1407
    deLU = 0x1007

    elGR = 0x0408

    enAU = 0x0C09
    enBZ = 0x2809
    enCA = 0x1009
    enCaribbean = 0x2409
    enGB = 0x0809
    enIE = 0x1809
    enIN = 0x4009
    enJM = 0x2009
    enMY = 0x4409
    enNZ = 0x1409
    enPH = 0x3409
    enSG = 0x4809
    enTT = 0x2C09
    enZA = 0x1C09
    enZW = 0x3009

    esAR = 0x2C0A
    esBO = 0x400A
    esCL = 0x340A
    esCO = 0x240A
    esCR = 0x140A
    esDO = 0x1C0A
    esEC = 0x300A
    esES = 0x0C0A
    esEST = 0x040A
    esGT = 0x100A
    esHN = 0x480A
    esMX = 0x080A
    esNI = 0x4C0A
    esPA = 0x180A
    esPE = 0x280A
    esPR = 0x500A
    esPY = 0x3C0A
    esSV = 0x440A
    esUS = 0x540A
    esUY = 0x380A
    esVE = 0x200A

    frBE = 0x080C
    frCA = 0x0C0C
    frCH = 0x100C
    frFR = 0x040C
    frLU = 0x140C
    frMC = 0x180C

    itCH = 0x0810
    itIT = 0x0410

    jaJP = 0x0411

    koKR = 0x0412

    ptBR = 0x0416
    ptPT = 0x0816

    ruRU = 0x0419

    zhCN = 0x0804
    zhHK = 0x0C04
    zhMO = 0x1404
    zhSG = 0x1004
    zhTW = 0x0404


familyLocalization = {
    "CN": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "TW": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "HK": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "MO": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "JP": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "KR": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
    "CL": {
        "Latin": True, "Cyrillic": True, "Hellenic": True,
        "Chinese": True, "Japanese": True, "Korean": True,
    },
}

weightMap = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    372: "Normal",
    400: "",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}

weightMapShort = {
    100: "Th",
    200: "XLt",
    300: "Lt",
    372: "Nm",
    400: "",
    500: "Md",
    600: "SmBd",
    700: "Bd",
    800: "XBd",
    900: "Bk",
}

widthMap = {
    3: "Condensed",
    4: "SemiCondensed",
    5: None,
    7: "Extended",
    10: "Warcraft",  # Warcraft numeral hack
}

widthMapShort = {
    3: "Cn",
    4: "SmCn",
    5: None,
    7: "Ex",
    10: "Wc",
}

slantMapShort = {
    "Italic": "It",
    "Oblique": "Obl",
}

notoWidthMap = {
    3: 3,
    5: 4,
    7: 5,
}

# map orthography to source file
shsRegionMap = {
    "CN": "SourceHanSansSC",
    "TW": "SourceHanSansTC",
    "HK": "SourceHanSansHC",
    "MO": "SourceHanSansMC",
    "JP": "SourceHanSans",
    "KR": "SourceHanSansK",
    "CL": "SourceHanSansK",
}

regionNameMap = {
    "CN": "CN",
    "TW": "TW",
    "HK": "HK",
    "MO": "MO",
    "JP": "JP",
    "KR": "KR",
    "CL": "Classical",
}

# sorted alphabetically
featureNameMap = {
    "OSF": "Oldstyle",
    "RP": "Roleplaying",
    "RRK": "[ʜᴀɴɢᴜᴇʟ]",
    "SC": "Smallcaps",
    "Simp": "Simplified",
    "UI": "UI",
}

tagNameMap = {**regionNameMap, **featureNameMap}


def LocalizedFamily(p):
    if "nameList" not in LocalizedFamily.__dict__:
        LocalizedFamily.nameList = {
            LanguageId.enUS: "Nowar Sans",

            LanguageId.deAT: "Nowar Grotesk",
            LanguageId.deCH: "Nowar Grotesk",
            LanguageId.deDE: "Nowar Grotesk",
            LanguageId.deLI: "Nowar Grotesk",
            LanguageId.deLU: "Nowar Grotesk",

            LanguageId.elGR: "Νοωαρ Σανς",

            LanguageId.enAU: "Nowar Sans",
            LanguageId.enBZ: "Nowar Sans",
            LanguageId.enCA: "Nowar Sans",
            LanguageId.enCaribbean: "Nowar Sans",
            LanguageId.enGB: "Nowar Sans",
            LanguageId.enIE: "Nowar Sans",
            LanguageId.enIN: "Nowar Sans",
            LanguageId.enJM: "Nowar Sans",
            LanguageId.enMY: "Nowar Sans",
            LanguageId.enNZ: "Nowar Sans",
            LanguageId.enPH: "Nowar Sans",
            LanguageId.enSG: "Nowar Sans",
            LanguageId.enTT: "Nowar Sans",
            LanguageId.enZA: "Nowar Sans",
            LanguageId.enZW: "Nowar Sans",

            LanguageId.esAR: "Nowar Palo",
            LanguageId.esBO: "Nowar Palo",
            LanguageId.esCL: "Nowar Palo",
            LanguageId.esCO: "Nowar Palo",
            LanguageId.esCR: "Nowar Palo",
            LanguageId.esDO: "Nowar Palo",
            LanguageId.esEC: "Nowar Palo",
            LanguageId.esES: "Nowar Palo",
            LanguageId.esEST: "Nowar Palo",
            LanguageId.esGT: "Nowar Palo",
            LanguageId.esHN: "Nowar Palo",
            LanguageId.esMX: "Nowar Palo",
            LanguageId.esNI: "Nowar Palo",
            LanguageId.esPA: "Nowar Palo",
            LanguageId.esPE: "Nowar Palo",
            LanguageId.esPR: "Nowar Palo",
            LanguageId.esPY: "Nowar Palo",
            LanguageId.esSV: "Nowar Palo",
            LanguageId.esUS: "Nowar Palo",
            LanguageId.esUY: "Nowar Palo",
            LanguageId.esVE: "Nowar Palo",

            LanguageId.frBE: "Nowar Linéale",
            LanguageId.frCA: "Nowar Linéale",
            LanguageId.frCH: "Nowar Linéale",
            LanguageId.frFR: "Nowar Linéale",
            LanguageId.frLU: "Nowar Linéale",
            LanguageId.frMC: "Nowar Linéale",

            # senza (without) grazie (serif)
            LanguageId.itCH: "Nowar Senza",
            LanguageId.itIT: "Nowar Senza",

            LanguageId.jaJP: "有愛角ゴシック",

            LanguageId.koKR: "有愛 고딕",

            # sem (without) serifa (serif)
            LanguageId.ptBR: "Nowar Sem",
            LanguageId.ptPT: "Nowar Sem",

            LanguageId.ruRU: "Новар Гротеск",

            LanguageId.zhCN: "有爱黑体",
            LanguageId.zhHK: "有愛黑體",
            LanguageId.zhMO: "有愛黑體",
            LanguageId.zhSG: "有爱黑体",
            LanguageId.zhTW: "有愛黑體",
        }

    r = p["region"]
    isLocalized = {
        LanguageId.deAT: familyLocalization[r]["Latin"],
        LanguageId.deCH: familyLocalization[r]["Latin"],
        LanguageId.deDE: familyLocalization[r]["Latin"],
        LanguageId.deLI: familyLocalization[r]["Latin"],
        LanguageId.deLU: familyLocalization[r]["Latin"],

        LanguageId.elGR: familyLocalization[r]["Hellenic"],

        LanguageId.enAU: familyLocalization[r]["Latin"],
        LanguageId.enBZ: familyLocalization[r]["Latin"],
        LanguageId.enCA: familyLocalization[r]["Latin"],
        LanguageId.enCaribbean: familyLocalization[r]["Latin"],
        LanguageId.enGB: familyLocalization[r]["Latin"],
        LanguageId.enIE: familyLocalization[r]["Latin"],
        LanguageId.enIN: familyLocalization[r]["Latin"],
        LanguageId.enJM: familyLocalization[r]["Latin"],
        LanguageId.enMY: familyLocalization[r]["Latin"],
        LanguageId.enNZ: familyLocalization[r]["Latin"],
        LanguageId.enPH: familyLocalization[r]["Latin"],
        LanguageId.enSG: familyLocalization[r]["Latin"],
        LanguageId.enTT: familyLocalization[r]["Latin"],
        LanguageId.enZA: familyLocalization[r]["Latin"],
        LanguageId.enZW: familyLocalization[r]["Latin"],

        LanguageId.esAR: familyLocalization[r]["Latin"],
        LanguageId.esBO: familyLocalization[r]["Latin"],
        LanguageId.esCL: familyLocalization[r]["Latin"],
        LanguageId.esCO: familyLocalization[r]["Latin"],
        LanguageId.esCR: familyLocalization[r]["Latin"],
        LanguageId.esDO: familyLocalization[r]["Latin"],
        LanguageId.esEC: familyLocalization[r]["Latin"],
        LanguageId.esES: familyLocalization[r]["Latin"],
        LanguageId.esEST: familyLocalization[r]["Latin"],
        LanguageId.esGT: familyLocalization[r]["Latin"],
        LanguageId.esHN: familyLocalization[r]["Latin"],
        LanguageId.esMX: familyLocalization[r]["Latin"],
        LanguageId.esNI: familyLocalization[r]["Latin"],
        LanguageId.esPA: familyLocalization[r]["Latin"],
        LanguageId.esPE: familyLocalization[r]["Latin"],
        LanguageId.esPR: familyLocalization[r]["Latin"],
        LanguageId.esPY: familyLocalization[r]["Latin"],
        LanguageId.esSV: familyLocalization[r]["Latin"],
        LanguageId.esUS: familyLocalization[r]["Latin"],
        LanguageId.esUY: familyLocalization[r]["Latin"],
        LanguageId.esVE: familyLocalization[r]["Latin"],

        LanguageId.frBE: familyLocalization[r]["Latin"],
        LanguageId.frCA: familyLocalization[r]["Latin"],
        LanguageId.frCH: familyLocalization[r]["Latin"],
        LanguageId.frFR: familyLocalization[r]["Latin"],
        LanguageId.frLU: familyLocalization[r]["Latin"],
        LanguageId.frMC: familyLocalization[r]["Latin"],

        LanguageId.itCH: familyLocalization[r]["Latin"],
        LanguageId.itIT: familyLocalization[r]["Latin"],

        LanguageId.jaJP: familyLocalization[r]["Japanese"],

        LanguageId.koKR: familyLocalization[r]["Korean"],

        LanguageId.ptBR: familyLocalization[r]["Latin"],
        LanguageId.ptPT: familyLocalization[r]["Latin"],

        LanguageId.ruRU: familyLocalization[r]["Cyrillic"],

        LanguageId.zhCN: familyLocalization[r]["Chinese"],
        LanguageId.zhHK: familyLocalization[r]["Chinese"],
        LanguageId.zhMO: familyLocalization[r]["Chinese"],
        LanguageId.zhSG: familyLocalization[r]["Chinese"],
        LanguageId.zhTW: familyLocalization[r]["Chinese"],
    }

    result = dict(LocalizedFamily.nameList)
    result.update({lang: result[LanguageId.enUS]
                   for lang, local in isLocalized.items() if not local})
    return result


def TagListToStr(lst):
    return ",".join(lst)


def GenerateFontName(p):
    localizedFamily = LocalizedFamily(p)
    region = p["region"]
    feature = [*sorted(p["feature"])]

    regionName = regionNameMap[region]
    subfamily = [tagNameMap[fea] for fea in feature]
    filenameSf = []
    wwsF = [region, *feature]
    wwsSf = []
    legacyF = [region, *feature]
    legacySf = []

    width = p["width"]
    widthName = widthMap[width]
    widthShort = widthMapShort[width]
    if widthName:
        subfamily.append(widthName)
        filenameSf.append(widthName)
        legacyF.append(widthShort)
    # Warcraft numeral hack
    if width == 10:
        wwsF.append(widthShort)
    elif widthName:
        wwsSf.append(widthName)

    weight = p["weight"]
    weightName = weightMap[weight]
    weightShort = weightMapShort[weight]
    if weightName:
        subfamily.append(weightName)
        filenameSf.append(weightName)
        wwsSf.append(weightName)
        if weight == 700:
            legacySf.append(weightName)
        else:
            legacyF.append(weightShort)

    if p.get("slant"):
        slantName = p["slant"]
        slantShort = slantMapShort[slantName]
        subfamily.append(slantName)
        filenameSf.append(slantName)
        wwsSf.append(slantName)
        if slantName == "Italic":
            legacySf.append(slantName)
        else:
            legacyF.append(slantShort)

    def formatFamily(f):
        return " ".join(f)

    def formatSubfamily(sf):
        return " ".join(sf) or "Regular"

    subfamily = formatSubfamily(subfamily)
    filenameF = localizedFamily[LanguageId.enUS].replace(" ", "")
    filenameTag = TagListToStr([p["region"], *sorted(p["feature"])])
    filenameSf = formatSubfamily(filenameSf).replace(" ", "")
    wwsF = formatFamily(wwsF)
    wwsSf = formatSubfamily(wwsSf)
    legacyF = formatSubfamily(legacyF)
    legacySf = formatSubfamily(legacySf)

    return {
        "typographic": ({k: "{} {}".format(v, regionName) for k, v in localizedFamily.items()}, subfamily),
        "wws": ({k: "{} {}".format(v, wwsF) for k, v in localizedFamily.items()}, wwsSf),
        "legacy": ({k: "{} {}".format(v, legacyF) for k, v in localizedFamily.items()}, legacySf),
        "friendly": {k: "{} {} {}".format(v, regionName, subfamily) for k, v in localizedFamily.items()},
        "file": "{}-{}-{}".format(filenameF, filenameTag, filenameSf),
        # font name can be too long to fit in 63-char PostScript name
        # the hashed name makes no sence but is valid
        "postscript": filenameF + "-" + hashlib.sha1("{} {}".format(regionName, subfamily).encode()).hexdigest(),
    }


def GenerateFilename(p):
    if p["family"] == "Nowar":
        filename = GenerateFontName(p)["file"]
        return p["encoding"] + "-" + filename
    else:
        nameList = {
            "Noto": lambda p: "NotoSans",
            "RRK": lambda p: "rrk",
            "SHS": lambda p: p["region"],
        }
        family = nameList[p["family"]](p)
        subfamily = ((widthMap[p["width"]] or "") + (weightMap[p["weight"]] or "") +
                     (p.get("slant") or "")) or "Regular"
        return family + "-" + subfamily


def ResolveDependency(p):
    if p["width"] == 10:  # Warcraft numeral hack
        result = {
            "Latin": {
                "family": "Noto",
                "width": 4,
                "weight": p["weight"],
            },
            "Numeral": {
                "family": "Noto",
                "width": 3,
                "weight": p["weight"],
            },
        }
    else:
        result = {
            "Latin": {
                "family": "Noto",
                "width": notoWidthMap[p["width"]],
                "weight": p["weight"],
            },
        }
    if "RRK" in p["feature"]:
        result["RRK"] = {
            "family": "RRK",
            "width": 5,
            "weight": p["weight"],
        }
    result["CJK"] = {
        "family": "SHS",
        "weight": p["weight"],
        "width": 5,
        "region": shsRegionMap[p["region"]],
    }
    return result


def GetCommonFont(weight, region, feature):
    xfea = []
    for mod, params in regionalVariant[region].get("xmod", []):
        if mod == "PSimp" and "base" in params:
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "unspec",
    }


def GetCommonChatFont(weight, region, feature):
    xfea = []
    for mod, params in regionalVariant[region].get("xmod", []):
        if mod == "PSimp" and "base" in params:
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature + xfea,
        "encoding": "unspec",
    }


def GetLatinFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature,
        "encoding": "abg",
    }


def GetLatinChatFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["base"],
        "feature": ["UI"] + feature,
        "encoding": "abg",
    }


def GetHansFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 10,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": feature,
        "encoding": "gbk",
    }


def GetHansCombatFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": feature,
        "encoding": "gbk",
    }


def GetHansChatFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["zhCN"],
        "feature": feature,
        "encoding": "gbk",
    }


def GetHantFont(weight, region, feature):
    xfea = []
    for mod, _ in regionalVariant[region].get("xmod", []):
        if mod == "PSimp":
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 10,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantCombatFont(weight, region, feature):
    xfea = []
    for mod, _ in regionalVariant[region].get("xmod", []):
        if mod == "PSimp":
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantNoteFont(weight, region, feature):
    xfea = []
    for mod, _ in regionalVariant[region].get("xmod", []):
        if mod == "PSimp":
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 5,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetHantChatFont(weight, region, feature):
    xfea = []
    for mod, params in regionalVariant[region].get("xmod", []):
        if mod == "PSimp" and "chat" in params:
            xfea.append("Simp")
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["zhTW"],
        "feature": feature + xfea,
        "encoding": "big5",
    }


def GetKoreanFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 5,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature,
        "encoding": "korean",
    }


def GetKoreanCombatFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 7,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature,
        "encoding": "korean",
    }


def GetKoreanDisplayFont(weight, region, feature):
    return {
        "weight": weight,
        "width": 3,
        "family": "Nowar",
        "region": regionalVariant[region]["koKR"],
        "feature": ["UI"] + feature,
        "encoding": "korean",
    }


def ParamToArgument(param):
    js = json.dumps(param, separators=(',', ':'))
    return "'{}'".format(js)


if __name__ == "__main__":
    makefile = {
        "variable": {
            "VERSION": config.version.split()[0],
        },
        "rule": {
            ".PHONY": {
                "depend": ["all", "GlobalFont", "NamingTest"],
            },
            "all": {
                "depend": [],
            },
            "GlobalFont": {
                "depend": [],
            },
            "NamingTest": {
                "depend": [],
            },
            "clean": {
                "command": [
                    "-rm -rf build/",
                    "-rm -rf out/??*-???/",
                ]
            }
        },
    }

    def powerset(lst): return reduce(lambda result, x: result +
                                     [subset + [x] for subset in result], lst, [[]])

    # font pack for each regional variant and weight
    for r, w, fea in product(config.fontPackRegion, config.fontPackWeight, powerset(config.fontPackFeature)):
        tagList = [r] + fea
        target = "{}-{}".format(TagListToStr(tagList), w)
        pack = "out/NowarSansTT-{}-${{VERSION}}.7z".format(target)

        makefile["rule"][".PHONY"]["depend"].append(target)
        makefile["rule"][target] = {
            "depend": [pack],
        }

        if (r, fea) in config.fontPackExportFeature:
            makefile["rule"]["all"]["depend"].append(pack)

        fontlist = {
            "ARIALN": GetCommonChatFont(w, r, fea),
            "FRIZQT__": GetCommonFont(w, r, fea),
        }

        if regionalVariant[r]["enUS"]:
            fontlist.update({
                "skurri": GetLatinFont(w, r, fea),
                "MORPHEUS": GetLatinChatFont(w, r, fea),
            })

        if regionalVariant[r]["ruRU"]:
            fontlist.update({
                "FRIZQT___CYR": GetLatinFont(w, r, fea),
                "SKURRI_CYR": GetLatinFont(w, r, fea),
                "MORPHEUS_CYR": GetLatinChatFont(w, r, fea),
            })

        if regionalVariant[r]["zhCN"]:
            fontlist.update({
                "ARKai_C": GetHansCombatFont(w, r, fea),
                "ARKai_T": GetHansFont(w, r, fea),
                "ARHei": GetHansChatFont(w, r, fea),
            })

        if regionalVariant[r]["zhTW"]:
            fontlist.update({
                "arheiuhk_bd": GetHantChatFont(w, r, fea),
                "bHEI00M": GetHantNoteFont(w, r, fea),
                "bHEI01B": GetHantChatFont(w, r, fea),
                "bKAI00M": GetHantCombatFont(w, r, fea),
                "blei00d": GetHantFont(w, r, fea),
            })

        if regionalVariant[r]["koKR"]:
            fontlist.update({
                "2002": GetKoreanFont(w, r, fea),
                "2002B": GetKoreanFont(w, r, fea),
                "K_Damage": GetKoreanCombatFont(w, r, fea),
                "K_Pagetext": GetKoreanDisplayFont(w, r, fea),
            })

        makefile["rule"][pack] = {
            "depend": ["out/{}/Fonts/{}.ttf".format(target, f) for f in fontlist],
            "command": [
                "cd out/{};".format(target) +
                "cp ../../LICENSE.txt Fonts/LICENSE.txt;" +
                "7z a -t7z -m0=LZMA:d=512m:fb=273 -ms ../../$@ Fonts/"
            ]
        }

        for f, p in fontlist.items():
            makefile["rule"]["out/{}/Fonts/{}.ttf".format(target, f)] = {
                "depend": ["build/nowar/{}.ttf".format(GenerateFilename(p))],
                "command": [
                    "mkdir -p out/{}/Fonts".format(target),
                    "cp $^ $@",
                ]
            }

    # otf files
    for w, wd, r, fea in product(config.fontPackWeight, [3, 5, 7, 10], regionNameMap.keys(), powerset(featureNameMap.keys())):
        param = {
            "family": "Nowar",
            "weight": w,
            "width": wd,
            "region": r,
            "feature": fea,
            "encoding": "unspec",
        }
        makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(param))] = {
            "depend": ["build/nowar/{}.otd".format(GenerateFilename(param))],
            "command": ["otfccbuild -q -O3 --keep-average-char-width $< -o $@"]
        }
        dep = ResolveDependency(param)
        makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(param))] = {
            "depend": [
                "build/noto/{}.otd".format(GenerateFilename(dep["Latin"])),
                "build/shs/{}.otd".format(
                    GenerateFilename(dep["CJK"])),
            ] + ([
                "build/noto/{}.otd".format(
                    GenerateFilename(dep["Numeral"]))
            ] if "Numeral" in dep else []) + ([
                "build/rrk/{}.otd".format(
                    GenerateFilename(dep["RRK"]))
            ] if "RRK" in dep else []),
            "command": [
                "mkdir -p build/nowar/",
                "python merge.py {}".format(ParamToArgument(param))
            ]
        }
        makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Latin"]))] = {
            "depend": ["source/noto/{}.ttf".format(GenerateFilename(dep["Latin"]))],
            "command": [
                "mkdir -p build/noto/",
                "otfccdump --glyph-name-prefix latn --ignore-hints $< -o $@",
            ]
        }
        if "Numeral" in dep:
            makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Numeral"]))] = {
                "depend": ["source/noto/{}.ttf".format(GenerateFilename(dep["Numeral"]))],
                "command": [
                    "mkdir -p build/noto/",
                    "otfccdump --glyph-name-prefix latn --ignore-hints $< -o $@",
                ]
            }
        if "RRK" in dep:
            makefile["rule"]["build/rrk/{}.otd".format(GenerateFilename(dep["RRK"]))] = {
                "depend": ["source/rrk/{}.ttf".format(GenerateFilename(dep["RRK"]))],
                "command": [
                    "mkdir -p build/rrk/",
                    "otfccdump --glyph-name-prefix rrk --ignore-hints $< -o $@",
                ]
            }
        makefile["rule"]["build/shs/{}.otd".format(GenerateFilename(dep["CJK"]))] = {
            "depend": ["source/shs/{}.ttf".format(GenerateFilename(dep["CJK"]))],
            "command": [
                "mkdir -p build/shs/",
                "otfccdump --glyph-name-prefix hani --ignore-hints $< -o $@",
            ]
        }

        # set encoding
        for e in ["abg", "gbk", "big5", "jis", "korean"]:
            enc = {
                "family": "Nowar",
                "weight": w,
                "width": wd,
                "region": r,
                "feature": fea,
                "encoding": e,
            }
            makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(enc))] = {
                "depend": ["build/nowar/{}.otd".format(GenerateFilename(enc))],
                "command": ["otfccbuild -q -O3 --keep-average-char-width $< -o $@"]
            }
            makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(enc))] = {
                "depend": ["build/nowar/{}.otd".format(GenerateFilename(param))],
                "command": ["python set-encoding.py {}".format(ParamToArgument(enc))]
            }

    # dump `makefile` dict to actual “GNU Makefile”
    makedump = ""

    for var, val in makefile["variable"].items():
        makedump += "{}={}\n".format(var, val)

    for tar, recipe in makefile["rule"].items():
        dep = recipe["depend"] if "depend" in recipe else []
        makedump += "{}: {}\n".format(tar, " ".join(dep))
        com = recipe["command"] if "command" in recipe else []
        for c in com:
            makedump += "\t{}\n".format(c)

    with codecs.open("Makefile", 'w', 'UTF-8') as mf:
        mf.write(makedump)
