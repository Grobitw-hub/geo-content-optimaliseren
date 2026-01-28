import streamlit as st
import google.generativeai as genai

# Pagina instellingen
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀", layout="wide")
st.title("🚀 GEO Specialist: Content Optimizer")

# Sidebar
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit", 0.0, 1.0, 0.7, 0.1)

if api_key:
    try:
        # Configuratie
        genai.configure(api_key=api_key, transport='rest')
        
        # OPLOSSING: We luisteren naar de foutmelding.
        # 1. We pakken Gemini 2.0 Flash (je betaalde key kan dit aan).
        # 2. We gebruiken 'google_search' in plaats van '_retrieval'.
        model = genai.GenerativeModel(
            model_name='models/gemini-2.0-flash',
            tools=[{'google_search': {}}], 
            generation_config={"temperature": temp_value}
        )
        
        col1, col2 = st.columns(2)
        with col1:
            target_url = st.text_input("Target URL (Het te verbeteren artikel)")
            keywords = st.text_area("Keywords & Focus")
        with col2:
            ref_urls = st.text_area("Referentie URL's (Tone of Voice)")

        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner('Bezig met analyseren en herschrijven...'):
                    try:
                        prompt = f"""
                        JE BENT EEN SENIOR GEO SPECIALIST.
                        Optimaliseer dit artikel voor AI-zoekmachines (GEO): {target_url}
                        
                        INPUT:
                        - Tone of Voice inspiratie: {ref_urls}
                        - Keywords: {keywords}
                        
                        EISEN:
                        1. Eén H1, gevolgd door een 'Kernvragen' Q&A sectie (3 vragen).
                        2. Gebruik H2/H3 met informatiedichte eerste alinea's (entiteiten).
                        3. Korte alinea's, heldere structuur.
                        4. Sluit af met een feitentabel en licentie.
                        
                        Output: Markdown.
                        """
                        
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.subheader("Resultaat")
                        st.markdown(response.text)
                        st.download_button("Download Markdown", response.text, "geo-artikel.md")

                    except Exception as e:
                        # Hier vangen we specifieke fouten op
                        st.error(f"Foutmelding: {e}")
                        st.info("Als je 'Unknown field' ziet, moet je de requirements.txt updaten.")
            else:
                st.warning("Vul alle velden in.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je API Key in.")
