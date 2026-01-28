import streamlit as st
import google.generativeai as genai

# Configuratie van de pagina
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je content voor LLM's zoals Gemini & ChatGPT.")

# Zijbalk voor instellingen
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 2.0, 0.7, 0.1)

# VERVANG DIT STUKJE IN JE CODE:
if api_key:
    genai.configure(api_key=api_key)
    
    # We gebruiken 'gemini-1.5-flash' voor snelheid of 'gemini-1.5-pro' voor diepgang.
    # We voegen de tool toe op de officieel ondersteunde manier voor v1beta.
    try:
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-pro-002', # Specifieke stabiele versie
          
            generation_config={"temperature": temp_value}
        )
    except Exception as e:
        st.error(f"Er is een fout bij het laden van het model: {e}")
    

    # Input velden
    target_url = st.text_input("Target URL (Te optimaliseren artikel)")
    ref_url_1 = st.text_input("Referentie URL 1 (Tone of Voice)")
    ref_url_2 = st.text_input("Referentie URL 2 (Tone of Voice)")
    keywords = st.text_area("Belangrijke Keywords & Focus")

    if st.button("Start GEO-Optimalisatie"):
        if target_url and ref_url_1:
            with st.spinner('De AI leest de pagina\'s en herschrijft je artikel...'):
                # Hier staan je exacte instructies uit de screenshot
                system_prompt = f"""
                JE BENT EEN SENIOR GEO SPECIALIST.
                Herschrijf het artikel van {target_url} op basis van de ToV van {ref_url_1} en {ref_url_2}.
                
                GEBRUIK DEZE GEO-RICHTLIJNEN:
                - LOGISCHE HIERARCHIE: Eén H1. H2's voor hoofdthema's, H3's voor subthema's.
                - Q&A KNOWLEDGE SNAPSHOT: Direct onder de H1 een sectie 'Kernvragen beantwoord' met 3 Q&A's.
                - ENTITY-DENSE OPENINGS: De eerste 40-50 woorden na elke heading MOETEN entiteiten bevatten.
                - KORTE PARAGRAFEN: Max 3-4 zinnen.
                - KEYWORDS: Integreer deze natuurlijk: {keywords}
                - AFSLUITING: Feitentabel + CC-BY licentie.
                """
                
                response = model.generate_content(system_prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # Download knop voor de klant
                st.download_button("Download als Markdown", response.text, file_name="geo-artikel.md")
        else:
            st.warning("Vul a.u.b. de Target URL en minimaal één Referentie URL in.")
else:
    st.info("Voer je Gemini API Key in de zijbalk in om de tool te activeren.")
