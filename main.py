from playwright.async_api import async_playwright
from google import generativeai as genai
import asyncio
import os


# -----------------------
# GATHER MATERIALS
# -----------------------
async def gatherMaterials(subject):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.encyclopedia.com/", wait_until="domcontentloaded")
        await page.keyboard.press('Tab')
        await page.keyboard.press('Tab')
        await page.keyboard.press('Tab')
        await page.keyboard.type(subject)
        await page.wait_for_timeout(1000)
        await page.keyboard.down('Enter')
        await page.wait_for_load_state('domcontentloaded')
        link = page.locator('a.gs-title').first
        await link.click()
        await page.wait_for_load_state('domcontentloaded')

        page_data = {
            'url': page.url,
            'content': await page.locator('body').text_content(),
            'subject': subject
        }

        await browser.close()
        return page_data


# -----------------------
# CHOOSE FORMAT
# -----------------------
def chooseFormat(format_choice):
    format_instructions = {
        "1": {
            "name": "Quizlet",
            "instruction": """Format the output EXACTLY as follows for Quizlet import:
- Each flashcard on a new line
- Format: term, definition
- Use a comma to separate term and definition"""
        },
        "2": {
            "name": "Kahoot",
            "instruction": """YOU MUST START WITH THIS EXACT HEADER LINE, this should be the first row (copy it exactly):
Question - Answer 1 - Answer 2 - Answer 3 - Answer 4 - Time limit (5,10,20,30,60,90 or 120) - Correct answer(s)"""
        },
        "3": {
            "name": "Gimkit",
            "instruction": """Format the output EXACTLY as follows for Gimkit import (CSV format):
Question,Incorrect Answer 1,Incorrect Answer 2,Incorrect Answer 3"""
        }
    }
    return format_instructions.get(format_choice, format_instructions["1"])


# -----------------------
# QUESTION WRITING
# -----------------------
def qWriting(page_data, selected_format):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-pro')

    response = model.generate_content(
        f"""You are a quiz writing expert. Create at least 10 questions about {page_data['subject']} based on the content provided.

{selected_format['instruction']}

Do not include any introductions, explanations, or conclusions. Output ONLY the formatted data ready for import into {selected_format['name']}.

Content to create questions from:
{page_data['content'][:4000]}"""
    )

    return response.text

