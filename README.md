# Flash Card Generator 🎴

An automated flashcard generation tool that creates study materials on any subject by scraping educational content and using AI to generate practice questions.

## 🌟 Features

- **Automated Content Gathering**: Uses Playwright to scrape educational content from Encyclopedia.com
- **AI-Powered Question Generation**: Leverages Google Gemini to summarize and convert content into flashcard-style questions
- **Multiple Export Formats**: Compatible with popular edTech platforms:
  - Kahoot
  - Quizlet
  - Gimkit
- **Subject Flexibility**: Generate flashcards for any topic you want to study

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Playwright**: Browser automation for web scraping
- **Encyclopedia.com**: Primary source for educational content
- **Google Gemini API**: AI-powered content summarization and question generation
- **Custom formatters**: Export utilities for various quiz platforms

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Internet connection for content scraping

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/CoreyJness/flashCardGenerator.git
cd flashCardGenerator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Set up your API keys:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## 💻 Usage

1. Run the program:
```bash
python main.py
```

2. Enter the subject you want to create flashcards for

3. Choose your preferred export format (Kahoot, Quizlet, or Gimkit)

4. The program will:
   - Search Encyclopedia.com for relevant content
   - Extract and process the information
   - Generate flashcard questions using Gemini
   - Export in your chosen format

## 📁 Project Structure

```
flashCardGenerator/
├── main.py                 # Main application entry point
├── .gitignore
└── README.md             # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect Encyclopedia.com's terms of service and use rate limiting to avoid overloading their servers.

## 📧 Contact

Corey Jones - [@CoreyJness](https://github.com/CoreyJness)

Project Link: [https://github.com/CoreyJness/flashCardGenerator](https://github.com/CoreyJness/flashCardGenerator)

---

**Happy Studying! 📚**
