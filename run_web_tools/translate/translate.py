import json
import shutil
import xml.etree.ElementTree as ET
from enum import Enum
import os
import re
import pandas as pd
from datetime import datetime
from translate.feishu_table_to_json import (
    get_csv_gzip_str,
    parse_csv_gzip_to_str,
    to_lang_code,
)

default_value = "未翻译"
translate_false_map = {"common_ad": "Ad"}


class LangKey(Enum):
    ZH_HANS = "values-zh-rCN"
    EN = "values"
    ZH_HANT = "values-zh-rTW"
    FIL = "values-fil"
    JA = "values-ja"
    KO = "values-ko"
    ID = "values-in"
    HI = "values-hi"
    TH = "values-th"
    AR = "values-ar"
    PT = "values-pt"
    ES = "values-es"
    VI = "values-vi"
    DE = "values-de"
    FR = "values-fr"


def read_strings_en(path):
    keys = []
    global translate_false_map
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    def repl(match):
        key = match.group(1)
        value = match.group(2)
        if 'translatable="false"' in match.group(0):
            translate_false_map[key] = value
        keys.append(key)
        return f'<string name="{key}">[{key}]</string>'

    template = re.sub(
        r'<string name="(.+?)">(.+?)</string>',
        repl,
        content,
        flags=re.DOTALL,
    )
    return keys, template


def create_xml(csv_path):
    excel = pd.read_csv(csv_path)
    country = {
        "zh-Hans": "values-zh-rCN",
        "en": "values",
        "zh-Hant": "values-zh-rTW",
        "fil": "values-fil",
        "ja": "values-ja",
        "ko": "values-ko",
        "id": "values-in",
        "hi": "values-hi",
        "th": "values-th",
        "ar": "values-ar",
        "pt": "values-pt",
        "es": "values-es",
        "vi": "values-vi",
        "de": "values-de",
        "fr": "values-fr",
    }

    country_lang = {}
    for index, row in excel.iterrows():
        row_key = row["key-Android"]
        for col_name, col_value in row.items():
            if col_name in country:
                country_lang_key = country[col_name]
                if country_lang_key not in country_lang:
                    country_lang[country_lang_key] = {}
                col_value = (
                    str(col_value)
                    .replace("'", r"\'")
                    .replace("&", "&amp;")
                    .replace("...", "…")
                    .replace("-", "–")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                ).rstrip()

                regex = r"(?i)short\s*tv"

                def replacement(match):
                    if " " in match.group():
                        if "S" in match.group():
                            return "Short Max"
                        else:
                            return "short max"
                    else:
                        if "S" in match.group():
                            return "ShortMax"
                        else:
                            return "shortmax"

                col_value = re.sub(regex, replacement, col_value)

                if col_value == "nan":
                    col_value = default_value
                country_lang[country_lang_key][row_key] = col_value

    return country_lang


def high_light_valid_strings(all_lang):
    source = "normal_login_guide_dialog_fragment_desc"
    high_light = ["normal_login_guide_dialog_fragment_protect_your_property"]

    for dir in all_lang.keys():
        lang = all_lang[dir]
        source_str = lang[source]
        for high_light_item in high_light:
            if lang[high_light_item] not in source_str:
                print(
                    f"\n高亮bug: {dir}\nkey={source}\nvalue={source_str}\nkey={high_light_item}\nvalue={lang[high_light_item]}"
                )


def write_strings_xml(keys, template, all_lang, output_dir_base):
    global translate_false_map
    for dir in all_lang.keys():
        lang = all_lang[dir]
        for key in translate_false_map.keys():
            lang[key] = translate_false_map[key]

        result = template
        for key in keys:
            if key not in lang:
                lang[key] = default_value
                print(f"飞书表格没配置 ${key} in {dir}")

            value = lang[key]
            result = result.replace(f"[{key}]", str(value).replace("$@", "$s"))

        output_dir = os.path.join(output_dir_base, dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(os.path.join(output_dir, "strings.xml"), "w", encoding="utf-8") as f:
            f.write(result)
    return output_dir_base


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
            )


def exec(strings_xml_path, csv_path, output_dirs=["res_output"]):
    keys, template = read_strings_en(strings_xml_path)
    all_lang = create_xml(csv_path)
    high_light_valid_strings(all_lang)
    print("start")
    print("模板:" + strings_xml_path)
    print(
        datetime.fromtimestamp(os.path.getmtime(strings_xml_path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print("\n多语言文本:" + csv_path)
    print(
        datetime.fromtimestamp(os.path.getmtime(csv_path)).strftime("%Y-%m-%d %H:%M:%S")
    )

    for output_dir in output_dirs:
        print("\n输出文件夹 start:" + output_dir)
        output = write_strings_xml(keys, template, all_lang, output_dir + "/")
        print("\n输出文件夹 end:" + output)


def exec(strings_xml_path, all_lang, output_dirs=["res_output"]):
    keys, template = read_strings_en(strings_xml_path)
    high_light_valid_strings(all_lang)
    print("start")
    print("模板:" + strings_xml_path)
    print(
        datetime.fromtimestamp(os.path.getmtime(strings_xml_path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    for output_dir in output_dirs:
        print("\n输出文件夹 start:" + output_dir)
        output = write_strings_xml(keys, template, all_lang, output_dir + "/")
        print("\n输出文件夹 end:" + output)


def read_feishu_cookie(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def save_feishu_cookie(file_path, cookie):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cookie)


def delete_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' has been deleted.")
    else:
        print(f"Directory '{directory_path}' does not exist.")


def zip_directory(directory_path, output_zip_path):
    shutil.make_archive(output_zip_path, "zip", directory_path)


def create_zip_file(xml, feishu_cookie_new=None):
    translate_path = "cache"
    translate_path_output = f"{translate_path}/res_output"
    translate_path_output_res = f"{translate_path}/res_output/res"
    translate_path_output_gzip = f"{translate_path}/res_output/compressed"
    cookies_file_path = f"{translate_path}/cookies.txt"
    os.makedirs(translate_path_output_res, exist_ok=True)
    os.makedirs(translate_path_output_gzip, exist_ok=True)

    # Read the default feishu_cookie from cookies.txt
    feishu_cookie = read_feishu_cookie(cookies_file_path)

    # If feishu_cookie_new is provided, save it to cookies.txt
    if feishu_cookie_new:
        feishu_cookie = feishu_cookie_new
        save_feishu_cookie(cookies_file_path, feishu_cookie)

    delete_directory(translate_path_output)
    gzip_str = get_csv_gzip_str(feishu_cookie)
    cvs_dict = parse_csv_gzip_to_str(json.loads(gzip_str))
    lang = to_lang_code(cvs_dict)
    exec(xml, lang, [translate_path_output_res])
    zip_directory(translate_path_output_res, translate_path_output_gzip)
    return translate_path_output_gzip + ".zip"


if __name__ == "__main__":
    # gzip_str = get_csv_gzip_str()
    # cvs_dict = parse_csv_gzip_to_str(json.loads(gzip_str.text))
    # lang = to_lang_code(cvs_dict)
    # exec(
    #     r"D:/mWork/mKalaTeam/mShortTV202407018/shorttv-code/app/src/main/res/values/strings.xml",
    #     lang,
    #     [r"D:/mWork/mKalaTeam/mShortTV202407018/shorttv-code/app/src/main/res/"],
    # )
    create_zip_file(
        "D:/mWork/mKalaTeam/mShortTV202407018/shorttv-code/app/src/main/res/values/strings.xml",
        """
    QXV0aHpDb250ZXh0	fff4923cbb7b4f1a8b36f0e466e35c30	.feishu.cn	/	2025-11-27T07:09:16.431Z	48	✓	✓	None			Medium	
    __tea__ug__uid	7287233560862443008	.feishu.cn	/	2025-02-25T07:09:17.399Z	33						Medium	
    _csrf_token	410de5d7edb9feffad4e6b5b1d1e1d03a84cd821-1732691376	.feishu.cn	/	2024-12-27T07:09:36.235Z	62		✓	None			Medium	
    _ga	GA1.1.2108309228.1696691267	.feishu.cn	/	2026-01-01T07:09:17.805Z	30						Medium	
    _ga_VPYRHN104D	GS1.1.1732691357.1.1.1732691357.60.0.0	.feishu.cn	/	2026-01-01T07:09:17.835Z	52						Medium	
    _gcl_au	1.1.1202027923.1732691358	.feishu.cn	/	2025-02-25T07:09:17.000Z	32						Medium	
    _gid	GA1.2.876623194.1732691358	.feishu.cn	/	2024-11-28T07:09:17.000Z	30						Medium	
    ccm_cdn_host	//lf-package-cn.feishucdn.com/obj/feishu-static	ehyg6a9wjd.feishu.cn	/	2024-12-04T07:16:00.000Z	59						Medium	
    et	cd087752a7d41bacf6caa07efe7e9f28	ehyg6a9wjd.feishu.cn	/	2025-11-27T07:09:40.000Z	34		✓	None			Medium	
    fg_uid	RID20241127150940264C8DDFC8D77503DA40	api.feelgood.cn	/	2025-11-27T07:17:45.694Z	43		✓	None			Medium	
    i18n_locale	zh	.feishu.cn	/	2026-01-01T07:09:35.980Z	13		✓	None			Medium	
    is_anonymous_session		.feishu.cn	/	2024-12-27T07:17:41.293Z	20	✓	✓				Medium	
    js_version	1	ehyg6a9wjd.feishu.cn	/	2024-12-04T07:17:42.000Z	11						Medium	
    landing_url	https://accounts.feishu.cn/accounts/page/login?app_id=2&no_trap=1&query_scope=all&redirect_uri=https%3A%2F%2Fehyg6a9wjd.feishu.cn%2Fsheets%2FYBuUsM4v8hyM7ytvvKYcVYDdnTh%3Flogin_redirect_times%3D1%26sheet%3DzUcAiZ	.feishu.cn	/	2024-11-29T07:09:17.449Z	223						Medium	
    lang	zh	.feishu.cn	/	2026-01-01T07:09:35.980Z	6		✓	None			Medium	
    locale	zh	.feishu.cn	/	2026-01-01T07:09:35.980Z	8		✓	None			Medium	
    login_recently	1	.feishu.cn	/	会话	15	✓	✓	None			Medium	
    passport_app_access_token	eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI3MzQ1ODMsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjIiOnsiaWF0IjoxNzMyNjkxMzc1LCJhY2Nlc3MiOnRydWV9LCIyOSI6eyJpYXQiOjE3MzI2OTEzNzgsImFjY2VzcyI6dHJ1ZX0sIjE0MyI6eyJpYXQiOjE3MzI2OTEzODMsImFjY2VzcyI6dHJ1ZX19LCJzdW0iOiJjMzdjZDNjNDBhMWM1MGZmNmJkZmI1MzdkZmVkYjM4ZDMxM2ZlZTRkNWU3ZGZjNzE5Y2E0YzBmOTA3Y2ExMWViIn19.C6xVlZiDX_mJRLZ1zj9FY3NBN-x7i9CQIWUCe8ecXM6ghG0gt4w1AA05wafNvyIWMuLqh1eoqhxGEkiObueWOg	ehyg6a9wjd.feishu.cn	/	2024-11-27T19:09:42.750Z	477	✓	✓	None			Medium	
    passport_app_access_token	eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI3MzQ1NzksInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzMyNjkxMzc5LCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiYzM3Y2QzYzQwYTFjNTBmZjZiZGZiNTM3ZGZlZGIzOGQzMTNmZWU0ZDVlN2RmYzcxOWNhNGMwZjkwN2NhMTFlYiJ9fQ.Qx9WVRfYyeGiY5W_1kUmQGj-m2QIftqjjuKSzNQD_4qgFkK9bby91Y4jkh-XhMBHoRrGPBSMMBnJ26U9nfy4cQ	internal-api-lark-api.feishu.cn	/	2024-11-27T19:09:38.861Z	375	✓	✓	None			Medium	
    passport_trace_id	7441852712046608385	.feishu.cn	/	2025-11-27T07:09:16.431Z	36		✓	None			Medium	
    passport_web_did	7441852712042496028	.feishu.cn	/	2025-11-27T07:09:16.431Z	35	✓	✓	None			Medium	
    session	XN0YXJ0-c22he990-6c5a-43a0-b7be-132c4680cad6-WVuZA	.feishu.cn	/	2025-11-27T07:09:34.284Z	57	✓	✓	None			Medium	
    session_list	XN0YXJ0-c22he990-6c5a-43a0-b7be-132c4680cad6-WVuZA	.feishu.cn	/	2025-11-27T07:09:34.284Z	62	✓	✓	None			Medium	
    sl_session	eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI3MzQ5NDUsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdWeElydFdrQUFEWW9GM3JtTWFBQU5uUnNXYzdCSUFIR2RHeFp6c0VnQWNaMGJGcnFoVUFBSUNLZ0VBUVVGQlFVRkJRVUZCUVVKdVVuTlhkWE5uYlVGQlp6MDkiLCJzdW0iOiJjMzdjZDNjNDBhMWM1MGZmNmJkZmI1MzdkZmVkYjM4ZDMxM2ZlZTRkNWU3ZGZjNzE5Y2E0YzBmOTA3Y2ExMWViIiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzMyNjkxNzQ1LCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJjbmYiOnsiamt0IjoiNVF4czEtZzV5WkFUcExoUGlZazFqbDNSMzdmNHZwMGJZVzRzcm96QjZyTSJ9LCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzA5NjYxODU4MjA1NTMyMTYzIiwibnNfdGlkIjoiNzA5ODA4NjA3ODU4MzI3NTUyMyIsIm90IjoxfX0.vQXXfx7YTcWtBqPV2qwSi0eBoy4wsl7Cn1x6w5mt3j-oykVtIgyNBKDai5AdJfQjPz8u9h6whWYxMpktOD3lTg	.feishu.cn	/	2024-11-27T19:15:45.486Z	749	✓	✓				Medium	
    swp_csrf_token	35370913-1753-4c9c-9a6f-0b0d93737ae3	.feishu.cn	/	2024-12-12T07:17:48.845Z	50		✓	None			Medium	
    t_beda37	889c7a41ad8b344478704db313dbf9e18b0f25aec79f1660ef5fbe106d4cfacb	.feishu.cn	/	2024-12-12T07:17:48.845Z	72	✓	✓	None			Medium	
    template-branch-list		ehyg6a9wjd.feishu.cn	/	2024-11-27T07:18:11.000Z	20						Medium	
    """,
    )
