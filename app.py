import streamlit as st
import google.generativeai as genai

st.title("GEO Content Optimizer - Stabiele Versie")
api_key = st.sidebar.text_input("API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Gebruik 1.5 Flash voor maximale stabiliteit
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    url = st.text_input("URL")
    if st.button("Optimaliseer"):
        # We laten de tools even weg om te kijken of de basis werkt
        res = model.generate_content(f"Herschrijf dit artikel voor GEO: {url}")
        st.write(res.text)
