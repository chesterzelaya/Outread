import ast
import numpy as np
import pandas as pd
import streamlit as st
import openai
import os
from bs4 import BeautifulSoup
import requests as r
import streamlit.components.v1 as components
from pdfminer.high_level import extract_text
import re

#openai.api_key =  st.secrets["OPENAI_API_KEY"]


@st.cache_data
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
    output_summary = response["choices"][0]["message"]["content"]
    return output_summary

@st.cache_data
def processLead(user_prompt, lead_content):
    system_prompt = "You are an extremely intelligent and concise consultant seeking to understand the different problems industry professionals face. You are scheduling meetings with these professionals and must deliberately prepare to ask insightful questions." 
    document_prompt = "Take a deep breath. You will accurately answer questions about the following profile: " + lead_content
    model = "gpt-4"

    out = oai_summarize(document_prompt, user_prompt, system_prompt, model)
    return out

@st.cache_data
def extract_text_from_pdf(pdf_path):
    string = extract_text(pdf_path)
    cleaned_text = re.sub(r'\n+', '\n', string)
    return cleaned_text

def main():

    st.markdown("<h1 style='text-align: center;'><a href='https://berkeley.streamlit.app/' style='text-decoration: none; color: inherit;'>Outread 🚀</a></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; color: #ccc;'>10 second espionage for your next meeting</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
        
    uploaded_file = col1.file_uploader("✨Insert the lead's .pdf file", type="pdf")

    if uploaded_file is not None:
        person_query = extract_text_from_pdf(uploaded_file)

    company_query = col2.text_input("✨ Insert Company Data (get from Perplexity)", placeholder="", key='person')

    col1.markdown("<h3 margin-top: -10px; color: #000;'>What do you want to know about the lead?</h3>", unsafe_allow_html=True)
    lead_skills = (col1.checkbox("Skills"),"\n 1) What are the lead's skills?")
    lead_industry = (col1.checkbox("Industry Details"), "\n 2) What industries do the user know?")
    lead_emo = (col1.checkbox("Emotional Abouts"),"\n 3) What are the emotional motivations of this lead?" )
    lead_prob = (col1.checkbox("Potential Problems"), "\n 4) What are potential problems this lead may have exposure to?")
    lead_list = [lead_skills,lead_industry, lead_emo, lead_prob]


    col2.markdown("<h3 margin-top: -10px; color: #000;'>What do you want to know about the lead's company?</h3>", unsafe_allow_html=True)
    company_dets = (col2.checkbox("Company Details"),"1) What is the company's overview")
    company_cust = (col2.checkbox("Customer Segment"), "2) Who are the company's target customers or customer segment?")
    company_prob = (col2.checkbox("Company Problems"),"3) What problems could this company interface throughout their mission?")
    company_list = [company_dets, company_cust, company_prob]

    lead_prompt = "Answer the following questions:"
    for i in range(len(lead_list)):
        if lead_list[i][0]:
            lead_prompt += lead_list[i][1]
    
    company_prompt = "Answer the following questions:"
    for i in range(len(company_list)):
        if company_list[i][0]:
            company_prompt += company_list[i][1]

    #button actions
    if st.button("🦹🏼 Get Espionage", key="centered"):
        st.write(lead_prompt, company_prompt)
            
        
if __name__ == "__main__":
    main()