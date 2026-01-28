import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")
st.title("🚀 GEO Specialist: Content Optimizer")

st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 2.0, 0.7, 0.1)

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We gebruiken hier de meest specifieke stabiele naam voor de beta API
        # Dit lost de 404 error op
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest', 
            generation_config={"temperature": temp_value}
        )
        
        # ... rest van je input velden ...
        
        target_url = st.text_input("Target URL")
        ref_url_1 = st.text_input("Referentie URL 1")
        ref_url_2 = st.text_input("Referentie URL 2")
        keywords = st.text_area("Keywords & Focus")

        if st.button("Start GEO-Optimalisatie"):
            if target_url and ref_url_1:
                with st.spinner('Bezig met genereren...'):
                    # Omdat we de search tool even parkeren voor stabiliteit, 
                    # vragen we de AI om de structuur te optimaliseren op basis van de URL's.
                    prompt = f"""
                    STRIKT DEZE GEO-RICHTLIJNEN VOLGEN:
                    Herschrijf het artikel van deze URL: {target_url} 
                    Gebruik de Tone of Voice van deze voorbeelden: {ref_url_1} en {ref_url_2}.
                    Focus op keywords: {keywords}

                    STRUCTUUR EISEN:
                    1. Eén duidelijke H1.
                    2. 'Kernvragen beantwoord' sectie (3x Q&A) direct onder de H1.
                    3. Gebruik H2 en H3 logisch.
                    4. Eerste 50 woorden na elke heading MOETEN vol zitten met entiteiten.
                    5. Korte paragrafen.
                    6. Sluit af met een feitabel en CC-BY licentie.
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("Download Markdown", response.text, file_name="geo-artikel.md")
            else:
                st.warning("Vul de URL's in.")
                
    except Exception as e:
        st.error(f"Er is iets misgegaan met de configuratie: {e}")
else:
    st.info("Voer je API Key in.")
