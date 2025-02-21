# LinkedIn Tailored CV Generator - Powered by CrewAI

![CrewAI Logo](crewai_logo.svg)

## 🚀 Overview
This project is a **LinkedIn Tailored CV Generator** that uses **CrewAI** to extract job details from a LinkedIn job post and generate a professional, tailored CV based on the user's uploaded information. Additionally, it provides **interview preparation materials** with key questions and talking points.

## 🔥 Features
- Extracts job details from a **LinkedIn job post URL**.
- Uses user-uploaded **.txt files** to customize the CV.
- Generates a **tailored CV** in **.docx** format.
- Provides **interview questions and talking points**.
- Simple **Streamlit UI** for easy interaction.

## 🛠️ Setup & Installation
### Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewai)
- OpenAI API Key or Google Gemini API Key

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/your-username/linkedin-cv-generator.git
cd linkedin-cv-generator

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys inside the .env file
```

## 🎯 How to Use
1. **Run the Streamlit App**
```bash
streamlit run app.py
```
2. **Follow the Steps on UI:**
   - Enter the **LinkedIn Job Post URL**.
   - Upload a `.txt` file containing your **basic information (skills, experience, etc.)**.
   - Click **Generate CV**.
   - Download the generated **Formatted CV (Word Document)** and **Interview Preparation Document**.

## 🏗️ Project Structure
```
├── crewai_logo.svg          # Logo
├── app.py                   # Main Streamlit Application
├── textfileconvertor.py      # Markdown to Word Conversion Script
├── requirements.txt          # Required dependencies
├── .env.example              # Example Environment Variables
└── README.md                 # This ReadMe file
```

## 🎨 UI Preview
![App Screenshot](screenshot.png)

## 🛠️ Built With
- **Python** 🐍
- **Streamlit** 📊
- **CrewAI** 🤖
- **Google Gemini AI** 🔥

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
We welcome contributions! Feel free to fork the repository and submit a **pull request**.

## 📩 Contact
For issues or feature requests, open an issue or reach out at **your-email@example.com**.

---
**Happy Coding! 🚀**

