# Ensure correct SQLite version (needed for ChromaDB)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool, ScrapeWebsiteTool
from dotenv import load_dotenv
from textfileconvertor import convert_md_to_docx

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title="LinkedIn Tailored CV Generator", layout="wide")

# Display CrewAI logo
st.image("crewai_logo.svg", width=200)

# Sidebar guide
st.sidebar.title("Project Guide")
st.sidebar.info("""
1. Enter the LinkedIn Job Post URL.
2. Upload your basic information as a `.txt` file.
3. Click **Generate CV** and wait for processing.
4. Download your tailored CV and interview materials in `.docx` format.
""")

# UI Inputs
st.title("LinkedIn Tailored CV Generator - Powered by CrewAI")
linkedin_url = st.text_input("Enter LinkedIn Job Post URL")
uploaded_file = st.file_uploader("Upload your information (.txt file)", type=["txt"])

# Initialize session state to persist file downloads
if "cv_ready" not in st.session_state:
    st.session_state.cv_ready = False
if "interview_ready" not in st.session_state:
    st.session_state.interview_ready = False

# Generate CV Button
if st.button("Generate CV"):
    if not linkedin_url or not uploaded_file:
        st.error("Please provide both a LinkedIn URL and an information file.")
    else:
        with st.spinner("Processing your request..."):
            time.sleep(2)  # Simulating delay

            # Read user info
            user_info = uploaded_file.read().decode("utf-8")

            # Save user info temporarily
            with open("user_info.txt", "w") as f:
                f.write(user_info)

            # Initialize LLM
            llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.7, api_key=GEMINI_API_KEY)

            # Initialize tools
            scrape_tool = ScrapeWebsiteTool()
            read_info_tool = FileReadTool(file_path="user_info.txt")

            # Define Agents
            Scraper = Agent(
                role="LinkedIn Job Post Scraper",
                goal="Extract job details from LinkedIn job post.",
                backstory="Expert web scraper capable of extracting key job details.",
                tools=[scrape_tool],
                llm=llm
            )

            FileReader = Agent(
                role="User Data Reader",
                goal="Read user details from a text file.",
                backstory="Ensures accurate extraction of user details.",
                verbose=True,
                tools=[read_info_tool],
                llm=llm
            )

            Writer = Agent(
                role="CV Writer",
                goal="Write a compelling CV tailored to the job description and user information.",
                backstory="Expert CV writer with experience in tailoring resumes.",
                llm=llm
            )

            InterviewPreparer = Agent(
                role="Interview Preparer",
                goal="Create interview questions based on the resume and job requirements.",
                verbose=True,
                backstory="Prepares candidates with key questions and talking points for success.",
                llm=llm
            )

            # Define Tasks
            scrape_task = Task(
                description="Scrape job details from the LinkedIn URL.",
                agent=Scraper,
                expected_output="Extract job title, description, and qualifications."
            )

            filereader_task = Task(
                description="Analyze the job description and extract key skills.",
                expected_output="Extract user details like name, skills, and experience.",
                agent=FileReader
            )

            write_task = Task(
                description="Generate a CV based on job description and user info.",
                agent=Writer,
                expected_output="A professional CV in markdown format.",
                output_file="tailored_resume.md",
                context=[scrape_task, filereader_task]
            )

            interview_task = Task(
                description="Create interview questions based on resume and job requirements.",
                expected_output="Document containing key questions and talking points.",
                output_file="interview_materials.md",
                context=[scrape_task, filereader_task],
                agent=InterviewPreparer
            )

            # Execute tasks
            crew = Crew(agents=[Scraper, FileReader, Writer, InterviewPreparer], tasks=[scrape_task, filereader_task, write_task, interview_task])
            try:
                crew.kickoff()
            except Exception as e:
                st.error(f"Error generating the CV: {str(e)}")
                st.stop()

            # Convert Markdown to Word Document
            cv_path = convert_md_to_docx("tailored_resume.md",output_docx="Formatted_CV.docx")
            interview_path = convert_md_to_docx("interview_materials.md",output_docx="Formatted_Interview_Material.docx")

            # Read files separately to prevent overwriting
            with open(cv_path, "rb") as cv_file:
                st.session_state.cv_content = cv_file.read()
                st.session_state.cv_ready = True

            with open(interview_path, "rb") as interview_file:
                st.session_state.interview_content = interview_file.read()
                st.session_state.interview_ready = True

            st.success("CV and Interview Materials generated successfully!")

# Download Buttons (Always Visible if Files Ready)
if st.session_state.cv_ready:
    st.download_button(
        "Download CV",
        st.session_state.cv_content,
        file_name="Formatted_CV.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if st.session_state.interview_ready:
    st.download_button(
        "Download Interview Material",
        st.session_state.interview_content,
        file_name="Interview_Material.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
