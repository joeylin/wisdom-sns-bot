from typing import List


def cookie_to_dict(cookies: str) -> dict:
    row_cookie = cookies.split(';')
    row_dict = dict()
    for i in row_cookie:
        if i == '':
            continue
        row = i.strip().split('=', 1)
        if len(row) == 2:
            row_dict[row[0].strip()] = row[1].strip()
    return row_dict


def cookies_to_str(cookies: List) -> str:
    cookie_strs = [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
    final_str = "; ".join(cookie_strs)
    return final_str


def headers_to_dict(headers: str) -> dict:
    row_header = headers.split('\n')
    row_dict = dict()
    for i in row_header:
        if i == '':
            continue
        row = i.strip().split(':', 1)
        if len(row) == 0:
            continue
        if row[0] == '':
            continue
        row_dict[row[0].strip()] = row[1].strip()
    return row_dict
