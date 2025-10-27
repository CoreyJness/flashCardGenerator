from playwright.async_api import async_playwright
from google import generativeai as genai
import asyncio
import os

##Function that gathers study information from the encyclopedia
async def gatherMaterials():
    subject = input('What would you like to study? ')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.encyclopedia.com/", wait_until="domcontentloaded")
        await page.keyboard.press('Tab')
        await page.keyboard.press('Tab')
        await page.keyboard.press('Tab')
        await page.keyboard.type(subject)
        await page.wait_for_timeout(1000)
        await page.keyboard.down('Enter')
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

# Run the async function and store the result
page_data = asyncio.run(gatherMaterials())



# Define format instructions
print("\nChoose output format:")
print("1. Quizlet")
print("2. Kahoot")
print("3. Gimkit")
format_choice = input("Enter your choice (1-3): ")
format_instructions = {
    "1": {
        "name": "Quizlet",
        "instruction": """Format the output EXACTLY as follows for Quizlet import:
- Each flashcard on a new line
- Format: term, definition
- Use a comma to separate term and definition
- Example:
Tyrannosaurus Rex, A large carnivorous dinosaur from the Late Cretaceous period
Triceratops, A herbivorous dinosaur with three horns and a large frill"""
    },
    "2": {
        "name": "Kahoot",
        "instruction": """YOU MUST START THE CSV WITH THIS EXACT HEADER LINE (copy it exactly):
    Headers:    Question - max 95 characters,Answer 1 - max 60 characters,Answer 2 - max 60 characters,Answer 3 - max 60 characters,Answer 4 - max 60 characters,Time limit (sec) - 5,10,20,30,60,90 or 120 secs,Correct answer(s) - choose at least one

    Then add your questions below the header, one per line:
    - Questions max 95 characters
    - Four answer options, each max 60 characters  
    - Time limit: 20
    - Correct answer: single number 1, 2, 3, or 4

    Complete example:
    Question - max 95 characters,Answer 1 - max 60 characters,Answer 2 - max 60 characters,Answer 3 - max 60 characters,Answer 4 - max 60 characters,Time limit (sec) - 5,10,20,30,60,90 or 120 secs,Correct answer(s) - choose at least one
    What period did T-Rex live in?,Cretaceous,Jurassic,Triassic,Cambrian,20,1
    Which dinosaur had three horns?,Triceratops,Stegosaurus,Brachiosaurus,Velociraptor,20,1

    DO NOT forget the header line!"""
    },
    "3": {
        "name": "Gimkit",
        "instruction": """Format the output EXACTLY as follows for Gimkit import (CSV format):
- First line must be: Question,Incorrect Answer 1,Incorrect Answer 2,Incorrect Answer 3
- Each subsequent line: question,wrong answer 1,wrong answer 2,correct answer
- The correct answer goes in the 4th column
- Example:
Question,Incorrect Answer 1,Incorrect Answer 2,Incorrect Answer 3
What period did T-Rex live in?,Jurassic,Triassic,Cretaceous
Which dinosaur had three horns?,Stegosaurus,Brachiosaurus,Triceratops"""
    }
}
selected_format = format_instructions.get(format_choice, format_instructions["1"])




# Configure Gemini API (set your API key as environment variable)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
# Create the model
model = genai.GenerativeModel('gemini-2.5-pro')
# Create flashcards
response = model.generate_content(
    f"""You are a quiz writing expert. Create at least 10 questions about {page_data['subject']} based on the content provided.

{selected_format['instruction']}

Do not include any introductions, explanations, or conclusions. Output ONLY the formatted data ready for import into {selected_format['name']}.

Content to create questions from:
{page_data['content'][:4000]}"""
)

print(response.text)