import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Pagina instellingen
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀", layout="wide")
st.title("🚀 GEO Specialist: Content Optimizer")

# Sidebar
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit", 0.0, 1.0, 0.7, 0.1)

if api_key:
    try:
        # We forceren de stabiele REST connectie
        genai.configure(api_key=api_key, transport='rest')
        
        # OPLOSSING: We gebruiken 'gemini-flash-latest'.
        # Deze stond op plek #16 in jouw debug-lijst en werkt met de klassieke toolnaam.
        model = genai.GenerativeModel(
            model_name='models/gemini-flash-latest',
            tools=[{'google_search_retrieval': {}}], 
            generation_config={"temperature": temp_value}
        )
        
        # Input velden
        col1, col2 = st.columns(2)
        with col1:
            target_url = st.text_input("Target URL (Het te verbeteren artikel)")
            keywords = st.text_area("Keywords & Focus")
        with col2:
            ref_urls = st.text_area("Referentie URL's (Tone of Voice)")

        # Start knop
        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner('De AI analyseert de content en zoekt online...'):
                    try:
                        prompt = f"""
                        JE BENT EEN SENIOR GEO SPECIALIST.
                        Herschrijf dit artikel voor Generative Engine Optimization: {target_url}
                        
                        BRONNEN & INPUT:
                        - Tone of Voice inspiratie: {ref_urls}
                        - Belangrijke keywords: {keywords}
                        
                        STRUCTUUR EISEN:
                        1. H1 Titel: Pakkend en relevant.
                        2. 'Kernvragen' sectie: Direct na de intro 3 Q&A's.
                        3. Body: Duidelijke H2's en H3's.
                        4. Entity-Rich: Verwerk feiten en namen in de eerste 50 woorden na elke kop.
                        5. Opmaak: Korte alinea's, gebruik bulletpoints.
                        6. Footer: Feitentabel en licentie.
                        
                        Output formaat: Markdown.
                        """
                        
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.subheader("Resultaat")
                        st.markdown(response.text)
                        st.download_button("Download Markdown", response.text, "geo-artikel.md")

                    except Exception as e:
                        # Vang eventuele specifieke fouten netjes op
                        st.error(f"Fout tijdens genereren: {e}")
                        if "404" in str(e):
                             st.warning("Model niet gevonden? Check je API key rechten.")
                        if "tool" in str(e).lower():
                             st.warning("Tool fout: De zoekfunctie gaf een conflict.")
            else:
                st.warning("Vul minimaal de Target URL en Referentie URL's in.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je API Key in.")
