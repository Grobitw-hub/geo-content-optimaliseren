import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")
st.title("🚀 GEO Specialist: Content Optimizer")

st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 1.0, 0.7, 0.1)

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We gebruiken hier de meest veilige naam die in elke regio werkt
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        target_url = st.text_input("Target URL")
        ref_urls = st.text_area("Referentie URL's (één per regel)")
        keywords = st.text_area("Keywords & Focus")

        if st.button("Start GEO-Optimalisatie"):
            if target_url:
                with st.spinner('Bezig met genereren...'):
                    # We maken de prompt expliciet zodat de AI weet wat hij moet doen
                    # ook zonder de 'search' tool die de 404's kan veroorzaken.
                    prompt = f"""
                    Herschrijf de content van de volgende pagina voor GEO (Generative Engine Optimization): {target_url}
                    
                    GEBRUIK DEZE RICHTLIJNEN:
                    1. Tone of Voice gebaseerd op: {ref_urls}
                    2. Focus op keywords: {keywords}
                    3. Structuur: H1 -> Kernvragen Q&A -> H2/H3.
                    4. Entity-dense openings (40-50 woorden) na elke heading.
                    5. Korte alinea's en front-loading van informatie.
                    6. Tabel met feiten aan het eind + CC-BY licentie.
                    
                    Output in Markdown format.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("Download resultaat", response.text, file_name="geo-artikel.md")
            else:
                st.warning("Voer een Target URL in.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je Gemini API Key in de zijbalk in.")
