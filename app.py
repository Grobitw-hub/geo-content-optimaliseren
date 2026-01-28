import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# 1. Pagina Configuratie
st.set_page_config(page_title="GEO Content Optimizer (Pro)", page_icon="🚀", layout="wide")
st.title("🚀 GEO Specialist: Content Optimizer (Pro)")

# 2. Sidebar Instellingen
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit", 0.0, 1.0, 0.7, 0.1)

# Hulpfunctie om het juiste model te laden
def load_model(api_key):
    genai.configure(api_key=api_key, transport='rest')
    
    # Configuratie specifiek voor Gemini 1.5 PRO
    # We gebruiken de tool-naam die hoort bij versie 1.5: 'google_search_retrieval'
    try:
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-pro-latest',
            tools=[{'google_search_retrieval': {}}], 
            generation_config={"temperature": temp_value}
        )
        return model, "Gemini 1.5 Pro"
    except Exception:
        # Fallback: Als Pro niet mag, pak dan Flash
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash-latest',
            tools=[{'google_search_retrieval': {}}],
            generation_config={"temperature": temp_value}
        )
        return model, "Gemini 1.5 Flash (Fallback)"

if api_key:
    try:
        # Initialiseer model
        model, model_name = load_model(api_key)
        st.sidebar.success(f"Verbonden met: {model_name}")

        # 3. Input Velden
        col1, col2 = st.columns(2)
        with col1:
            target_url = st.text_input("Target URL (Het artikel)")
            keywords = st.text_area("Keywords & Focus")
        with col2:
            ref_urls = st.text_area("Referentie URL's (Tone of Voice)")

        # 4. De Uitvoerende Knop
        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner(f'{model_name} is aan het denken en zoekt online...'):
                    try:
                        # De Prompt
                        prompt = f"""
                        JE BENT EEN SENIOR GEO SPECIALIST.
                        Je taak is het herschrijven van content voor Generative Engine Optimization.
                        
                        BRONNEN:
                        - Analyseer URL: {target_url}
                        - Tone of Voice URL's: {ref_urls}
                        - Keywords: {keywords}
                        
                        STRUCTUUR EISEN (STRIKT):
                        1. H1: Pakkende titel.
                        2. Direct na H1: Een sectie 'Kernvragen' (3 Q&A's).
                        3. Body: Gebruik H2 en H3.
                        4. Entity-Dense: Eerste 50 woorden na elke kop moeten vol feiten zitten.
                        5. Opmaak: Korte alinea's, bulletpoints waar mogelijk.
                        6. Footer: Feitentabel + CC-BY licentie vermelding.
                        
                        Output: Markdown.
                        """
                        
                        # API Aanroep
                        response = model.generate_content(prompt)
                        
                        # Resultaat Tonen
                        st.markdown("---")
                        st.subheader("Resultaat")
                        st.markdown(response.text)
                        st.download_button("Download Markdown", response.text, "geo-artikel.md")

                    except exceptions.InvalidArgument as e:
                        # Vangt specifiek de 'google_search' vs 'retrieval' fouten af
                        st.error(f"Instellingsfout bij Google: {e}")
                        st.warning("Probeer de pagina te verversen.")
                    except Exception as e:
                        st.error(f"Algemene fout: {e}")
            else:
                st.warning("Vul minimaal de Target URL en Referentie URL's in.")
                
    except Exception as e:
        st.error(f"Kon niet verbinden met API: {e}")
else:
    st.info("Voer je API Key in.")
