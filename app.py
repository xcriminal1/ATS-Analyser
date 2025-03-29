import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from fpdf import FPDF

# Load all environment variables
load_dotenv()

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Function to save response as PDF
def save_response_as_pdf(response_text, file_path):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'ATS Evaluation', 0, 1, 'C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(10)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Evaluation')
    pdf.chapter_body(response_text)
    pdf.output(file_path)

# Prompt Templates
input_prompt_template = """
Act as a highly skilled and experienced Applicant Tracking System (ATS) with in-depth knowledge of the tech 
industry, including software engineering, data science, data analysis, big data engineering, and related fields. 
Your task is to evaluate the provided resume against the given job description.
Responsibilities:
Evaluation: Assess the resume for alignment with the job description, considering key qualifications, experiences, and skills.
Competitiveness: Recognize the competitive job market and offer precise, constructive feedback to improve the resume.
Scoring: Assign a percentage match score based on the job description (JD) and the resume.
Keyword Analysis: Identify missing keywords and skills that are critical for the job description.
Output Structure:
ATS score of Resume : "xx%" 

Match Percentage: "xx%"

Text Readability: "xx%"

Wrong Keywords: "xx%"

Wrong Skills: "xx%"
Missing Keywords: [List of missing keywords if any JD is provided in the input]
Profile Summary: [short summary of strengths and weaknesses]
Instructions:
Provide a professional  evaluation focusing on the candidate's fit for the role based on the input JD if provied if not provied then what roles the candidate can fit for .
Highlight specific areas where the resume aligns or falls short of the job requirements.
Offer actionable recommendations for improving the resume to better match the job description.
Data:
Resume: {resume_text}
Job Description: {job_description}
"""

input_prompt1_template = """
You are an experienced Technical Human Resource Manager with expertise in Data Science, Full Stack Development, Web Development, Big Data Engineering, 
DevOps, Data Analysis, UI/UX Design, and Product Management. Your task is to review the provided resume against the job description for these profiles.
Responsibilities:
Evaluation: Assess whether the candidate's profile aligns with the job description, considering key qualifications, experiences, and skills.
Strengths and Weaknesses: Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Scoring: Provide a match percentage of the resume with the job description.
Output Structure:
JD Match: "xx%"
Strengths: [List of strengths]
Weaknesses: [List of weaknesses]
Profile Summary: [Detailed summary of the candidate's fit for the role]
Instructions:
Offer a detailed and professional evaluation focusing on the candidate's alignment with the role.
Clearly indicate areas where the resume meets or does not meet the job requirements.
Provide actionable recommendations for enhancing the resume.
Data:
Resume: {resume_text}
Job Description: {job_description}
"""

input_prompt3_template = """
Improved Input Prompt for ATS Scanner:
You are a highly skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the provided resume against the given job description.
Responsibilities:
Evaluation: Assess the resume for alignment with the job description, considering key qualifications, experiences, and skills.
Scoring: Assign a percentage match score based on the job description (JD) and the resume.
Keyword Analysis: Identify missing keywords and skills that are critical for the job description.
Output Structure:
Percentage Match: "xx%"
Ats Score: "xx%"
Missing Keywords: [List of missing keywords]
Overall Thoughts: [Detailed summary of the resume's strengths and weaknesses]
Data:
Resume: {resume_text}
Job Description: {job_description}
"""
input_prompt4_template = """ Improve the provided resume by incorporating strong action verbs to enhance the 
impact of each bullet point and section. Ensure that each experience and skill statement starts with 
a dynamic action verb to convey a sense of accomplishment and proactivity. Additionally, if a resume
 summary is not present, create a concise and compelling resume summary that effectively highlights the candidate's key 
 qualifications, experiences(if any), and career goals. Use the information
 from the existing resume to craft this summary, ensuring it aligns with the overall tone and content of the resume. """

## Streamlit app
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif;
}
.header {
    font-size: 50px;
    font-weight: bold;
}            
.custom-container {

    padding: 5px;
    border-radius: 5px;
}
.div.sttext_area {
    font-size: 20px;
    font-weight: bold;
    padding: 5px;
}                 
</style>
<div class="header">🚀 Smart ATS Analyzer</div>
 <div class="custom-container">
    <p>Boost Your Resume's Visibility with Our Advanced ATS Evaluation Tool!</p>
</div>          
""", unsafe_allow_html=True)
# st.text("Boost Your Resume's Visibility with Our Advanced ATS Evaluation Tool!")
job_description = st.text_area("🔍 Job Description", "Paste the job description here to match with your resume.")
uploaded_file = st.file_uploader("📄 Upload Your Resume", type="pdf", help="Upload your resume in PDF format for a thorough evaluation.")


col1, col2, col3, col4 = st.columns(4)
st.markdown("""
<style>
 body {
    font-family: 'Arial', sans-serif;
}           
div.stButton > button:first-child {
    background-color: #000; /* Black background */
    color: #fff; /* White text */
    border: 1px solid #000; /* Black border */
    border-radius: 4px;
    padding: 12px 40px;
    font-size: 13px;
    font-weight: 300;
    box-shadow: #fff 4px 4px 0 0, #000 4px 4px 0 1px;
}
div.stButton > button:hover {
    background-color: #444; /* Darker grey */
    color: #fff;
}
div.stButton > button:active {
    box-shadow: rgba(0, 0, 0, .125) 0 3px 5px inset;
    transform: translate(2px, 2px);
}
div.stButton > button:focus {
    outline: none;
}
</style>
""", unsafe_allow_html=True)

with col1:

    submit = st.button("Check ATS Score")
with col2:
    submit1 = st.button("About the Resume")
with col3:
    submit3 = st.button("Percentage Match")
with col4:
    submit4 = st.button("Improve the Resume")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(resume_text=resume_text, job_description=job_description)
        response = get_gemini_response(input_prompt)
        st.subheader("Response")
        st.write(response)
        save_response_as_pdf(response, "ATS_Score_Response.pdf")
        st.success("The response has been saved as a PDF.")
        with open("ATS_Score_Response.pdf", "rb") as file:
            st.download_button(label="Download the PDF", data=file, file_name="ATS_Score_Response.pdf", mime="application/pdf")
    else:
        st.write("Please upload the resume.")

elif submit1:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt1 = input_prompt1_template.format(resume_text=resume_text, job_description=job_description)
        response = get_gemini_response(input_prompt1)
        st.subheader("The Response is")
        st.write(response)
        save_response_as_pdf(response, "ATS_Score_Response.pdf")
        st.success("The response has been saved as a PDF.")
        with open("ATS_Score_Response.pdf", "rb") as file:
            st.download_button(label="Download the PDF", data=file, file_name="ATS_Score_Response.pdf", mime="application/pdf")
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt3 = input_prompt3_template.format(resume_text=resume_text, job_description=job_description)
        response = get_gemini_response(input_prompt3)
        st.subheader("The Response is")
        st.write(response)
        save_response_as_pdf(response, "ATS_Score_Response.pdf")
        st.success("The response has been saved as a PDF.")
        with open("ATS_Score_Response.pdf", "rb") as file:
            st.download_button(label="Download the PDF", data=file, file_name="ATS_Score_Response.pdf", mime="application/pdf")
    
    else:
        st.write("Please upload the resume.")

elif submit4:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt4 = input_prompt4_template.format(resume_text=resume_text, job_description=job_description)
        response = get_gemini_response(input_prompt4)
        st.subheader("The Response is")
        st.write(response)
        save_response_as_pdf(response, "Imoroved_Resume_Response.pdf")
        st.success("The response has been saved as a PDF.")
        with open("Imoroved_Resume_Response.pdf", "rb") as file:
            st.download_button(label="Download the PDF", data=file, file_name="Imoroved_Resume_Response.pdf", mime="application/pdf")   
    else:
        st.write("Please upload the resume.")             

# Add footer with developer details
import streamlit as st

st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
       
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: offwhite !important;
        font-family: 'Poppins', sans-serif;
    }
    .footer p {
        margin: 0;
        font-size: 20px;
    }
    .footer a {
        text-decoration: none;
        color: #555;
        margin: 0 10px;
    }
    .footer a:hover {
        color: white;
    }
    .footer .social-icons {
        font-size: 24px; /* Increase icon size for better visibility */
    }
    .footer .social-icons i {
        margin: 0 10px; /* Add spacing between icons */
    }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <div class="footer">
        <p>Developed by Anubhav Raj</p>
        <p class="social-icons">
            <a href="https://github.com/Anubhx" target="_blank"><i class="fab fa-github"></i></a>
            <a href="https://linkedin.com/in/anubhax/" target="_blank"><i class="fab fa-linkedin"></i></a>
            <a href="mailto:anubhav0427@gmail.com"><i class="fas fa-envelope"></i></a>
        </p>
    </div>
""", unsafe_allow_html=True)
