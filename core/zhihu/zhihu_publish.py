from playwright.async_api import Page, BrowserContext


async def zhihu_publish(page: Page, title: str, content: str):
    await page.goto("https://zhuanlan.zhihu.com/write")
    await page.wait_for_load_state("networkidle")

    await page.get_by_placeholder("请输入标题（最多 100 个字）").click()
    await page.get_by_placeholder("请输入标题（最多 100 个字）").fill(title)

    await page.locator(".DraftEditor-root").click()
    await page.get_by_role("textbox").nth(1).fill(content)

    await page.get_by_role("button", name="添加话题").click()
    await page.wait_for_load_state("networkidle")

    source = await page.locator(".Popover-content .css-lwqucw").all_inner_texts()


