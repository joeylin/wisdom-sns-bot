import json
import os
import re

import requests
from playwright.async_api import Page, BrowserContext


async def zhihu_login(page: Page, context: BrowserContext):
    qrcode_file = 'file_db/zhihu_qrcode.png'
    # 先清理环境：如果之前有遗留的qrcode图片，先删除
    delete_file(qrcode_file)

    # Navigate to the desired URL
    await page.goto('https://www.zhihu.com/signin?next=%2F')
    # Wait for any dynamic content to load
    await page.wait_for_load_state("networkidle")

    img_src = await page.get_by_role("img", name="二维码").get_attribute("src")
    # 下载并保存图片
    response = requests.get(f"https:{img_src}")
    with open(qrcode_file, 'wb') as f:
        f.write(response.content)

    print(f"请扫描二维码登录: {qrcode_file}")
    # wait for log in success and redirect to home page
    await page.wait_for_url("https://www.zhihu.com/", timeout=60000)

    # 4. 在登录成功并跳转到首页后，获取cookie
    cookies = await page.context.cookies()
    print(cookies)

    with open("file_db/zhihu_cookies.json", "w") as f:
        f.write(json.dumps(cookies))

    # 登录成功之后，删除二维码登录图片
    delete_file(qrcode_file)

    return cookies


async def zhihu_load_cookies(context: BrowserContext):
    with open("file_db/zhihu_cookies.json", "r") as f:
        cookies = json.loads(f.read())
        await context.add_cookies(cookies)
        return cookies


async def zhihu_login_state_check(context: BrowserContext):
    result = await zhihu_load_cookies(context)
    page = await context.new_page()
    pattern = re.compile(r"http.*://.+?/signin.+")
    try:
        async with page.expect_navigation(url=pattern, timeout=7000) as resp:
            await page.goto("https://www.zhihu.com/",
                            wait_until='networkidle')
    except Exception as e:
        print('Did not redirect to the login page, login success.')
        await page.close()
        return result
    else:
        await page.close()
        return None


def delete_file(path: str):
    if os.path.exists(path):
        try:
            os.remove(path)
            print("文件已成功删除!")
        except Exception as e:
            print(f"错误: {e}")
