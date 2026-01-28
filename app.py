import streamlit as st
import google.generativeai as genai

# Pagina configuratie
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀", layout="wide")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je blogartikelen zodat LLM's (Gemini, ChatGPT) ze optimaal begrijpen en citeren.")

# Zijbalk
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 1.0, 0.7, 0.1)

# Debug optie
debug_mode = st.sidebar.checkbox("Toon beschikbare modellen (Debug)")

if api_key:
    try:
        # Configuratie
        genai.configure(api_key=api_key, transport='rest')
        
        if debug_mode:
            models = [m.name for m in genai.list_models()]
            st.sidebar.write(models)

        # We gebruiken de universele naam voor de zoek-tool
        model = genai.GenerativeModel(
            model_name='models/gemini-2.0-flash',
            tools=[{'google_search_retrieval': {}}],
            generation_config={"temperature": temp_value}
        )
        
        # Invoer velden
        col1, col2 = st.columns(2)
        with col1:
            target_url = st.text_input("Target URL (Het te verbeteren artikel)")
            keywords = st.text_area("Keywords & Focuspunten")
        with col2:
            ref_urls = st.text_area("Referentie URL's (één per regel)")

        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner('Gemini analyseert de bronnen...'):
                    try:
                        prompt = f"""
                        JE BENT EEN SENIOR GEO SPECIALIST.
                        Transformeer dit artikel: {target_url}
                        
                        RICHTLIJNEN:
                        - Gebruik de Tone of Voice van: {ref_urls}
                        - Focus op keywords: {keywords}
                        - Structuur: 1x H1 -> 'Kernvragen beantwoord' Q&A (3x) -> H2/H3.
                        - Entity-dense openings (40-50 woorden) na elke heading.
                        - Korte alinea's (max 3-4 zinnen).
                        - Tabel met feiten aan het eind + CC-BY licentie.
                        
                        Output in Markdown.
                        """
                        
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.subheader("Resultaat")
                        st.markdown(response.text)
                        
                        st.download_button("Download Markdown", response.text, file_name="geo-artikel.md")
                    except Exception as e:
                        st.error(f"Fout tijdens genereren: {e}")
            else:
                st.warning("Vul alle URL's in.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je API Key in de zijbalk in.")
