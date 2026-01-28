import streamlit as st
import google.generativeai as genai

# Pagina configuratie
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀", layout="wide")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je blogartikelen voor maximale vindbaarheid in LLM's en AI Overviews.")

# Zijbalk voor instellingen
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 1.0, 0.7, 0.1)

if api_key:
    try:
        # Configuratie met stabiele transportmethode
        genai.configure(api_key=api_key, transport='rest')
        
        # We gebruiken Gemini 2.0 Flash uit jouw lijst met de Search tool geactiveerd
        model = genai.GenerativeModel(
            model_name='models/gemini-2.0-flash',
            tools=[{'google_search_retrieval': {}}],
            generation_config={"temperature": temp_value}
        )
        
        # Gebruikersinvoer
        col1, col2 = st.columns(2)
        
        with col1:
            target_url = st.text_input("Target URL (Het te verbeteren artikel)", placeholder="https://...")
            keywords = st.text_area("Belangrijke Keywords & Focuspunten", placeholder="Bijv: AI content creatie, SEO strategie 2026")
            
        with col2:
            ref_urls = st.text_area("Referentie URL's voor Tone of Voice (één per regel)", placeholder="https://...")

        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner('De AI analyseert de bronnen en herschrijft de content...'):
                    # De uitgebreide GEO-prompt gebaseerd op jouw expert-regels
                    prompt = f"""
                    JE BENT EEN SENIOR GEO SPECIALIST (Generative Engine Optimization). 
                    Je taak is om het blogartikel op {target_url} te transformeren zodat LLM's het optimaal begrijpen en citeren.
                    
                    GEBRUIK DEZE BRONNEN:
                    - Analyseer de structuur en inhoud van: {target_url}
                    - Extraheer en hanteer de Tone of Voice van deze voorbeelden: {ref_urls}
                    - Integreer deze keywords op een natuurlijke manier: {keywords}
                    
                    STRIKTE GEO-RICHTLIJNEN VOOR STRUCTUUR:
                    1. LOGISCHE HIERARCHIE: Gebruik exact één H1. Gebruik H2 voor hoofdthema's en H3 voor subdetails.
                    2. Q&A KNOWLEDGE SNAPSHOT: Plaats direct onder de H1 een sectie 'Kernvragen beantwoord' met 3 kritieke vragen en bondige antwoorden (max 40 woorden per stuk).
                    3. ENTITY-DENSE OPENINGS: De eerste 40 tot 50 woorden na ELKE heading (H2/H3) moeten de belangrijkste entiteiten (onderwerpen, merken, begrippen) expliciet benoemen. Vermijd vage inleidingen.
                    4. KORTE PARAGRAFEN: Elke alinea mag maximaal 3-4 zinnen bevatten (hoge Flesch Reading Ease).
                    5. FRONT-LOADING: Zet de belangrijkste definitie of het antwoord direct bovenaan elke sectie.
                    6. LIJSTEN & TABELLEN: Zet complexe informatie om in een <ul>, <ol> of <table>.
                    7. SEMANTISCHE CUES: Gebruik gids-woorden zoals "In essentie", "Belangrijkste takeaway", "Stap 1".
                    8. FOOTER: Sluit af met een kleine tabel met feiten, de tekst "Laatst bijgewerkt op 28-01-2026" en een "Licentie: CC-BY" note.
                    
                    Lever het resultaat op in een prachtig opgemaakte Markdown tekst.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.subheader("Geoptimaliseerd Artikel")
                    st.markdown(response.text)
                    
                    # Download optie
                    st.download_button(
                        label="Download als Markdown bestand",
                        data=response.text,
                        file_name="geo-geoptimaliseerd-artikel.md",
                        mime="text/markdown"
                    )
            else:
                st.warning("Vul alstublieft de Target URL en de Referentie URL's in.")
                
    except Exception as e:
        st.error(f"Er is een configuratiefout opgetreden: {e}")
        st.info("Tip: Controleer of je API-key gekoppeld is aan een project in Google AI Studio.")
else:
    st.info("Voer je Gemini API Key in de zijbalk in om de tool te starten.")
