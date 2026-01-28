import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")
st.title("🚀 GEO Specialist: Content Optimizer")

st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 1.0, 0.7, 0.1)

if api_key:
    try:
        # We forceren hier ALLES: de API versie en de transport methode
        genai.configure(api_key=api_key, transport='rest')
        
        # DEBUG: Laat zien welke modellen beschikbaar zijn voor deze key
        if st.sidebar.checkbox("Toon beschikbare modellen (Debug)"):
            models = [m.name for m in genai.list_models()]
            st.sidebar.write(models)

        # We proberen de meest stabiele naamgeving zonder prefix
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        target_url = st.text_input("Target URL")
        ref_urls = st.text_area("Referentie URL's (één per regel)")
        keywords = st.text_area("Keywords & Focus")

        if st.button("Start GEO-Optimalisatie"):
            if target_url:
                with st.spinner('Bezig met genereren...'):
                    # Simpele prompt om verbinding te testen
                    prompt = f"Optimaliseer deze pagina voor GEO: {target_url}. Gebruik ToV: {ref_urls}. Focus op: {keywords}."
                    
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
            else:
                st.warning("Voer een Target URL in.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je Gemini API Key in.")
