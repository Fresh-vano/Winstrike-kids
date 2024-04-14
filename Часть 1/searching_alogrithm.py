import cv2
import easyocr
import numpy as np
from PIL import Image
import sys
import json

from fuzzywuzzy import fuzz, process


def search_product_type(data_str: str, product_type: list):
    mass_include_val = []

    for prod_type in product_type:
        mass_include_val.append(fuzz.WRatio(data_str, prod_type))

    idx = mass_include_val.index(max(mass_include_val))

    return (idx, product_type[idx])


def search_fat(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("жиры" in data):
        idx = data.index("жиры")
    elif ("жир" in data):
        idx = data.index("жир")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_protein(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("белки" in data):
        idx = data.index("белки")
    elif ("белк" in data):
        idx = data.index("белк")
    elif ("елки" in data):
        idx = data.index("елки")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_carbs(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("левод" in data):
        idx = data.index("левод")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_energy_value(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("нергет" in data):
        idx = data.index("нергет")
    elif ("энерг" in data):
        idx = data.index("энерг")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_sodium(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("натри" in data):
        idx = data.index("натри")
    elif ("атри" in data):
        idx = data.index("атри")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_sugar(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("ахароз" in data):
        idx = data.index("ахароз")
    elif ("сахаро" in data):
        idx = data.index("сахаро")
    elif ("ахараз" in data):
        idx = data.index("ахараз")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 100):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_sugar(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("ахароз" in data):
        idx = data.index("ахароз")
    elif ("сахаро" in data):
        idx = data.index("сахаро")
    elif ("ахараз" in data):
        idx = data.index("ахараз")

    if (idx == -1):
        return "N/A"
    result = ""

    start_idx = idx
    while idx < len(data):
        cur_char = data[idx]
        if str.isdigit(cur_char):
            result += cur_char

        if ((cur_char in alpha) and (len(result) != 0)):
            return result

        if ((cur_char in ".,") and (cur_char not in result) and (len(result) != 0)):
            result += cur_char

        idx += 1
        if ((idx - start_idx) > 50):
            return "N/A" if len(result) == 0 else result

    return "N/A" if len(result) == 0 else result


def search_years(data: str):
    alpha = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower() + " "

    idx = -1
    if ("месяц" in data):
        idx = data.index("месяц")
    elif ("есяц" in data):
        idx = data.index("есяц")

    result = ""

    if idx - 7 > 0:
        new_str = data[idx-7: idx]

        for char in new_str:
            if char.isdigit():
                result += char

        if (len(result) != 0):
            return f"С {result if int(result) < 20 else result[0]} месяцев"

        else:
            return "N/A"

    return "N/A"


def search_description(data: str):

    idx = -1
    if ("остав" in data):
        idx = data.index("остав")
    elif ("(остав" in data):
        idx = data.index("(остав")
    elif ("соста" in data):
        idx = data.index("соста")
    elif ("сосав" in data):
        idx = data.index("сосав")

    if idx == -1:
        return "N/A"

    cur_char = data[idx]

    while ((idx < len(data)) and (cur_char != " ")):
        idx += 1
        cur_char = data[idx]

    if (idx == len(data)):
        return "N/A"

    new_len = len(data) - idx
    return data[idx:(idx + 100 if 100 < new_len else new_len)]


def save_scaled_img(img_path: str) -> None:

    str_strip_mass = img_path.split("/")[-1].split(".")
    new_path = str_strip_mass[0] + "-300." + str_strip_mass[1]
    img = Image.open(img_path)

    # склеиваем новый путь
    dir_path = img_path.split("/")
    dir_path[-1] = new_path
    new_path = str.join("/", dir_path)
    img.save(new_path, dpi=(500, 500))

    return new_path


def preprocess_image(new_path: str):

    preproc_img = cv2.imread(new_path)
    img_gray = cv2.cvtColor(preproc_img, cv2.COLOR_BGR2GRAY)

    return img_gray


def search_manufacturer(text_en: str, text_ru: str):
    text_ru = text_ru.lower()
    text_en = text_en.lower()

    manufacturer_mass_en = ["heinz", "nestle", "gerber",
                            "hero", "sivma"]

    manufacturer_mass_ru = ["умница", "агуша", "лукошко"]

    for name_ru in manufacturer_mass_ru:
        if (name_ru[:-1] in text_ru) or (
            name_ru[1:] in text_ru
        ):
            return name_ru

    for name_en in manufacturer_mass_en:
        if (name_en[:-1] in text_en) or (
            name_en[1:] in text_en
        ):
            return name_en

    return "N/A"


def get_contour(img):

    reader = easyocr.Reader(lang_list=['ru'])
    reader_en = easyocr.Reader(lang_list=['en'])
    allow_list = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        str("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890").lower() + " -.,+"

    en_res = reader_en.readtext(img, paragraph=True, detail=False)
    en_text = ""
    for string in en_res:
        en_text += string

    struct = {
        "name": "N/A",
        "manufacturer": "N/A",
        "category_id": "N/A",
        "description": "N/A",
        "characteristics": {
                "energy_value": "N/A",
                "sodium": "N/A",
                "total_sugar": "N/A",
                "free_sugar": "N/A",
                "total_protein": "N/A",
                "total_fat": "N/A",
                "fruit_content": "N/A",
                "age_marking": "N/A",
                "high_sugar_front_packaging": "Нет",
                "labeling": "Соответствует"
        }
    }

    res = reader.readtext(img, paragraph=True,
                          allowlist=allow_list, text_threshold=0.8)

    full_text = ""

    for item in res:
        full_text += item[1]
        y1 = item[0][0][0]
        x1 = item[0][0][1]
        y2 = item[0][2][0]
        x2 = item[0][2][1]

        coord_img = img[x1:x2, y1:y2]

        k = 2000.0 / coord_img.shape[1]

        new_x = 2000
        new_y = int(k*coord_img.shape[0])

        coord_img = cv2.resize(coord_img, (new_x, new_y))
        search_all_text(coord_img, struct, reader)

    struct["manufacturer"] = search_manufacturer(en_text, full_text)

    return struct


def search_all_text(img, struct, reader):
    allow_list = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
        str("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890").lower() + " -.,+"

    res = reader.readtext(img, paragraph=True,
                          allowlist=allow_list, detail=False, text_threshold=0.8)

    product_type = ["Сухие каши и крахмалистые продукты",
                    "Молочные продукты",
                    "Йогурт",
                    "Фруктовые и овощные пюре/коктейли",
                    "Фруктовые десерты",
                    "Поликомпонентные продукты/блюда",
                    "Сухие закуски",
                    "Перекусы",
                    "Ингредиенты"]

    for text in res:
        text = text.lower()
        if struct["name"] == "N/A":
            idx, name = search_product_type(text, product_type=product_type)
            if ("name" != "N/A"):
                struct["name"] = name
                struct["category_id"] = idx + 1
        if struct["description"] == "N/A":
            description = search_description(text)
            if (description != "N/A"):
                struct["description"] = description
        if struct["characteristics"]["energy_value"] == "N/A":
            energy_value = search_energy_value(text)
            if (energy_value != "N/A"):
                struct["characteristics"]["energy_value"] = energy_value

        if struct["characteristics"]["sodium"] == "N/A":
            sodium = search_sodium(text)
            if (sodium != "N/A"):
                struct["characteristics"]["sodium"] = sodium

        if struct["characteristics"]["total_sugar"] == "N/A":
            total_sugar = search_sugar(text)
            if (total_sugar != "N/A"):
                struct["characteristics"]["total_sugar"] = total_sugar

        if struct["characteristics"]["free_sugar"] == "N/A":
            ...

        if struct["characteristics"]["total_protein"] == "N/A":
            protein = search_protein(text)
            if (protein != "N/A"):
                struct["characteristics"]["total_protein"] = protein
        if struct["characteristics"]["total_fat"] == "N/A":
            fat = search_fat(text)
            if (fat != "N/A"):
                struct["characteristics"]["total_fat"] = fat
        if struct["characteristics"]["fruit_content"] == "N/A":
            ...

        if struct["characteristics"]["age_marking"] == "N/A":
            age = search_years(text)
            if (age != "N/A"):
                struct["characteristics"]["age_marking"] = age


def get_dict(new_path: str):
    img = save_scaled_img(new_path)
    elem_dict = get_contour(preprocess_image(img))

    json_path = new_path.split("\\")
    json_path[-1] = json_path[-1].split(".")[0] + ".json"
    json_path = "\\".join(json_path)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(elem_dict, f, ensure_ascii=False)
        print(fr"Файл сохранен по адресу: {json_path}")

    return elem_dict


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_dict(sys.argv[1])
