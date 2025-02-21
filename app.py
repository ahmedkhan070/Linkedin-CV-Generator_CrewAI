import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, ScrapeWebsiteTool, FileWriterTool
from crewai import LLM
from dotenv import load_dotenv
from textfileconvertor import convert_md_to_docx
import time

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title="LinkedIn Tailored CV Generator - Powered by CrewAI", layout="wide")

# Add CrewAI logo and Image
st.image("crewai_logo.svg", width=200)
st.logo("crewai_logo.svg")

# Sidebar for project guide
st.sidebar.title("Project Guide")
st.sidebar.info("""
1. Enter the LinkedIn Job Post URL.
2. Upload your basic information as a `.txt` file.
3. Click **Generate CV** and wait for processing.
4. Download your tailored CV and interview material in `.docx` format.
""")

# UI Layout
st.title("LinkedIn Tailored CV Generator - Powered by CrewAI")
col1, col2 = st.columns(2)
with col1:
    linkedin_url = st.text_input("Enter LinkedIn Job Post URL")
with col2:
    uploaded_file = st.file_uploader("Upload your information (.txt file)", type=["txt"])

if st.button("Generate CV"):
    if not linkedin_url or not uploaded_file:
        st.error("Please provide both a LinkedIn URL and an information file.")
    else:
        with st.spinner("Processing your request..."):
            time.sleep(2)  # Simulating processing delay

            # Read user info
            user_info = uploaded_file.read().decode("utf-8")

            # Initialize LLM
            llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.7, api_key=GEMINI_API_KEY)
            
            # Initialize tools
            scrape_tool = ScrapeWebsiteTool()
            read_info_tool = FileReadTool(file_path="user_info.txt")
            
            # Save user info temporarily
            with open("user_info.txt", "w") as f:
                f.write(user_info)
            
            # Define the scraping agent
            Scraper = Agent(
                role="LinkedIn Job Post Scraper",
                goal="Extract job details from LinkedIn job post.",
                backstory="An expert web scraper capable of extracting key job details from a LinkedIn job post",
                tools=[scrape_tool],
                llm=llm
            )
            
            # Define the analysis agent
            FileReader = Agent(
                role="User Data Reader",
                goal="Read user details from a text file.",
                backstory="A diligent reader, ensuring accurate extraction of user details.",
                verbose=True,
                tools=[read_info_tool],
                llm=llm
            )
            
            # Define the writer agent
            Writer = Agent(
                role="CV Writer",
                goal="Write a compelling CV tailored to the job description and user information.",
                backstory="An expert CV writer with experience in tailoring resumes based on job descriptions.",
                llm=llm
            )
            
            # Agent 4: Interview Preparer
            interview_preparer = Agent(
                role="Engineering Interview Preparer",
                goal="Create interview questions and talking points "
                    "based on the resume and job requirements",
                verbose=True,
                backstory=(
                    "Your role is crucial in anticipating the dynamics of "
                    "interviews. With your ability to formulate key questions "
                    "and talking points, you prepare candidates for success, "
                    "ensuring they can confidently address all aspects of the "
                    "job they are applying for."
                ),
                llm=llm
            )

            # Define tasks
            scrape_task = Task(
                description="Scrape job details from the given LinkedIn URL.",
                agent=Scraper,
                expected_output="Extract job title, description and qualifications required"
            )

            filereader_task = Task(
                description="Analyze the job description and extract key skills and requirements.",
                expected_output="Extract user details like name, skills, and experience.", 
                agent=FileReader
            )

            write_task = Task(
                description="Generate a CV based on the analyzed job description and user info.",
                agent=Writer,
                expected_output="A professional CV as markdown file with # used for headings.", 
                output_file="tailored_resume.md",
                context=[scrape_task, filereader_task]
            )
            
            interview_preparation_task = Task(
                description=(
                    "Create a set of potential interview questions and talking "
                    "points based on the tailored resume and job requirements. "
                    "Utilize tools to generate relevant questions and discussion "
                    "points. Make sure to use these question and talking points to "
                    "help the candidate highlight the main points of the resume "
                    "and how it matches the job posting."
                ),
                expected_output=(
                    "A document containing key questions and talking points "
                    "that the candidate should prepare for the initial interview."
                ),
                output_file="interview_materials.md",
                context=[scrape_task, filereader_task],
                agent=interview_preparer
            )

            # Create crew and execute tasks
            crew = Crew(agents=[Scraper, FileReader, Writer, interview_preparer], tasks=[scrape_task, filereader_task, write_task, interview_preparation_task])
            try:
                crew.kickoff()
            except Exception as e:
                st.error(f"An error occurred while generating the CV: {str(e)}. Please try again later.")
                st.stop()
            
            # Convert Markdown to Word Document with formatting
            doc_path = convert_md_to_docx("tailored_resume.md")
            interview_doc_path = convert_md_to_docx("interview_materials.md")
            
            # download button for cv
            st.success("CV Generation Completed!")
            with open(doc_path, "rb") as f:
                st.download_button("Download CV", f, file_name="Formatted_CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            
            # download button for interview materials
            with open(interview_doc_path, "rb") as f:
                st.download_button("Download Interview Material", f, file_name="Interview_Material.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

