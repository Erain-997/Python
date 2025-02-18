import json
import gzip
import base64
import pycurl
import zlib
from io import BytesIO


def parse_csv_gzip_to_str(csv_data):
    result = {"rows": []}
    for block in csv_data["data"]["blocks"]:
        gzip_datatable = block["gzip_datatable"]
        compressed_data = base64.b64decode(gzip_datatable)
        decompressed_data = gzip.decompress(compressed_data)
        decompressed_str = decompressed_data.decode("utf-8", errors="replace")
        data = json.loads(decompressed_str)
        result["rows"].extend(data["rows"])
    return result


def to_lang_code(json):
    index_info = {
        "values-zh-rCN": 5,
        "values": 6,
        "values-zh-rTW": 7,
        "values-fil": 8,
        "values-ja": 9,
        "values-ko": 10,
        "values-in": 11,
        "values-hi": 12,
        "values-th": 13,
        "values-ar": 14,
        "values-pt": 15,
        "values-es": 16,
        "values-vi": 17,
        "values-de": 18,
        "values-fr": 19,
    }
    lang = {}
    for country_key in index_info.keys():
        lang[country_key] = {}

    rows = json["rows"]

    for row in rows:
        for key in index_info.keys():
            value = None
            columns = row["columns"]
            if not columns or not columns[2]:
                continue

            if "value" not in columns[2]:
                continue

            key = columns[2]["value"]

            for country_key in index_info.keys():
                lang[country_key][key] = ""
                try:
                    col_value_origin = columns[index_info[country_key]]["value"]
                    if isinstance(col_value_origin, list):
                        col_value = "".join(
                            [
                                item.get("text", "")
                                for item in col_value_origin
                                if isinstance(item, dict)
                            ]
                        )
                    else:
                        col_value = col_value_origin

                    col_value = (
                        str(col_value)
                        .replace("'", r"\'")
                        .replace("&", "&amp;")
                        .replace("...", "…")
                        .replace("-", "–")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    ).rstrip()
                    lang[country_key][key] = col_value
                except:
                    continue

    return lang


def sanitize_headers(headers):
    sanitized_headers = {}
    for key, value in headers.items():
        try:
            value.encode("latin-1")
            sanitized_headers[key] = value
        except UnicodeEncodeError:
            sanitized_headers[key] = value.encode("utf-8").decode("latin-1")
    return sanitized_headers


def make_request(url, headers, cookies, timeout=50):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.TIMEOUT, timeout)
    c.setopt(c.HTTPHEADER, [f"{k}: {v}" for k, v in headers.items()])
    c.setopt(c.COOKIE, "; ".join([f"{k}={v}" for k, v in cookies.items()]))
    c.setopt(c.SSL_VERIFYPEER, 0)  # 禁用 SSL 证书验证
    c.setopt(c.SSL_VERIFYHOST, 0)  # 禁用 SSL 主机验证
    c.perform()
    c.close()
    return buffer.getvalue()


def get_csv_gzip_str(feishu_session):
    feishu_cookie = {"session": feishu_session}

    x_csrftoken = "410de5d7edb9feffad4e6b5b1d1e1d03a84cd821-1732691376"
    referer = (
        "https://ehyg6a9wjd.feishu.cn/sheets/YBuUsM4v8hyM7ytvvKYcVYDdnTh?sheet=zUcAiZ"
    )
    token = "YBuUsM4v8hyM7ytvvKYcVYDdnTh"

    create_url = (
        "https://ehyg6a9wjd.feishu.cn/space/api/v2/sheet/sub_block"
        "?token=YBuUsM4v8hyM7ytvvKYcVYDdnTh"
        "&block_token=block_7265897292027625475_3823605879_30427_a%2Cblock_7265897292027625475_3285309363_30530_a"
        "&schema_version=1"
        "&blockIds=block_7265897292027625475_3823605879_30427_a"
        "&blockIds=block_7265897292027625475_3285309363_30530_a"
    )
    create_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "x-csrftoken": x_csrftoken,
        "referer": referer,
        "accept": "application/json, text/plain, */*",
        "Accept-Encoding": "",  # 设置为空字符串以明文传输
    }

    create_response = make_request(
        url=create_url,
        headers=sanitize_headers(create_headers),
        cookies=feishu_cookie,
    )

    if create_response is None or len(create_response) < 1000:
        print("get_csv_gzip_str failed")
        if create_response:
            print(create_response.decode("utf-8", errors="replace"))
            with open("create_response_error.json", "w", encoding="utf-8") as f:
                f.write(create_response.decode("utf-8", errors="replace"))
        return None

    decompressed_str = create_response.decode("utf-8", errors="replace")
    return decompressed_str


if __name__ == "__main__":
    gzip_str = get_csv_gzip_str("XN0YXJ0-9cds88cb-e2b6-464b-8ad3-472a59911186-WVuZA")

    if gzip_str:
        try:
            cvs_dict = parse_csv_gzip_to_str(json.loads(gzip_str))
            lang = to_lang_code(cvs_dict)
            json_str = json.dumps(cvs_dict, indent=4, ensure_ascii=False)
            print(json_str)
        except Exception as e:
            print(f"Failed to process gzip_str: {e}")
    else:
        print("Request failed")
