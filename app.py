import streamlit as st
from pdfminer.high_level import extract_text
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

@st.cache_data()
def extract_text_from_pdf(pdf_path):
    string = extract_text(pdf_path)
    cleaned_text = re.sub(r'\n+', '\n', string)
    return cleaned_text

@st.cache_data()
def oai_summarize(document_prompt, user_prompt, system_prompt, model, temp=.7, tokens=750):
    response = openai.ChatCompletion.create(
          model=model,
          messages=[{"role": "system", "content": system_prompt},
                    {"role": "user", "content": document_prompt},
                    {"role": "user", "content": user_prompt}],
          temperature=temp,
          max_tokens=tokens,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
    output_summary = response['choices'][0]['message']['content']
    return output_summary



@st.cache_data()
def processLead(user_prompt, lead_content):
    system_prompt = "You are an extremely intelligent and concise consultant seeking to understand the different problems industry professionals face. You are scheduling meetings with these professionals and must deliberately prepare to ask insightful questions." 
    document_prompt = "Take a deep breath. You will accurately answer questions about the following profile: " + lead_content
    model = "gpt-4"  # Ensure the correct model is specified here
    out = oai_summarize(document_prompt, user_prompt, system_prompt, model)
    return out

def process_analysis(prompt, content):
    analysis = processLead(prompt, content)
    return analysis

def main():
    st.markdown("<h1 style='text-align: center;'><a href='https://berkeley.streamlit.app/' style='text-decoration: none; color: inherit;'>Outread 🚀</a></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; color: #ccc;'>10 second espionage for your next meeting</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    uploaded_file = col1.file_uploader("✨Insert the lead's .pdf file", type="pdf")

    company_query = col2.text_input("✨ Insert Company Data (get from Perplexity)", placeholder="", key='person')

    lead_skills = col1.checkbox("Skills")
    lead_industry = col1.checkbox("Industry Details")
    lead_emo = col1.checkbox("Emotional Abouts")
    lead_prob = col1.checkbox("Potential Problems")
    lead_quest = col1.checkbox("Helpful Questions")

    company_dets = col2.checkbox("Company Details")
    company_cust = col2.checkbox("Customer Segment")
    company_prob = col2.checkbox("Company Problems")

    # Generate prompts based on checkboxes
    lead_prompt = "Answer the following questions about the lead diligently and concisely:\n"
    if lead_skills:
        lead_prompt += "1) What are the lead's skills?\n"
    if lead_industry:
        lead_prompt += "2) What industries does the lead know?\n"
    if lead_emo:
        lead_prompt += "3) What are the emotional motivations of this lead?\n"
    if lead_prob:
        lead_prompt += "4) What are potential problems this lead may have exposure to?\n"
    if lead_quest:
        lead_prompt += "5) Given the information from the lead's LinkedIn profile, generate questions that delve deep into their industry expertise and experiences. The goal is to reveal potential systemic challenges, inefficiencies, and areas of concern within their industry. Frame these questions in a way that encourages detailed responses and insights.?\n"

    company_prompt = "Answer the following questions about the company:\n"
    if company_dets:
        company_prompt += "1) What is the company's overview?\n"
    if company_cust:
        company_prompt += "2) Who are the company's target customers or customer segments?\n"
    if company_prob:
        company_prompt += "3) What problems could this company interface throughout their mission?\n"

    # Button actions
    if st.button("🦹🏼 Get Espionage", key="centered"):
        if uploaded_file:
            person_query = extract_text_from_pdf(uploaded_file)
            lead_analysis = process_analysis(lead_prompt, person_query)
            st.write(lead_analysis)
        if company_query:
            company_analysis = process_analysis(company_prompt, company_query)
            st.write(company_analysis)
        

if __name__ == "__main__":
    main()
