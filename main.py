import asyncio

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from core.utils import cookies_to_str
from core.zhihu.zhihu_login import zhihu_login, zhihu_login_state_check
from core.zhihu.zhihu_operator import ZhiHuOperator


async def main():
    # Launch the Playwright instance
    async with async_playwright() as p:
        device = p.devices["Desktop Chrome"]
        # Launch the browser of the current browser_type
        browser = await p.chromium.launch()

        # Create new context
        context = await browser.new_context(**device)

        # Create new page within the context
        page = await context.new_page()

        # Apply stealth to the page
        await stealth_async(page)

        cookies = await zhihu_login_state_check(context)
        if cookies is None:
            cookies = await zhihu_login(page, context)

        cookie_str = cookies_to_str(cookies)
        print(cookie_str)

        # with open("articles/AI-tech.txt", "r", encoding="utf-8") as f:
        #     article_content = f.read()
        #     operator = ZhiHuOperator(cookie_str)
        #     result = operator.publish_content(tags="AI技术",
        #                                       title="AI Agent如何重构知识工作者的职业",
        #                                       content=article_content)
        #     print(result)

        await page.goto("https://zhuanlan.zhihu.com/write")
        await page.wait_for_load_state("networkidle")

        # await page.get_by_placeholder("请输入标题（最多 100 个字）").click()
        # await page.get_by_placeholder("请输入标题（最多 100 个字）").fill("请输入标题")

        # Take a screenshot of the page and save it with the browser_type name
        await page.screenshot(path="screenshot/screenshot_publish.png", full_page=True)
        print("Screenshot captured successfully.")

        # Close the browser
        # await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
