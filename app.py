import streamlit as st
import google.generativeai as genai

# Pagina configuratie voor een professionele uitstraling
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀", layout="wide")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je blogartikelen zodat LLM's (Gemini, ChatGPT) ze optimaal begrijpen en citeren.")

# Zijbalk voor instellingen en API beheer
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 1.0, 0.7, 0.1)

# Debug optie voor jou als beheerder
debug_mode = st.sidebar.checkbox("Toon beschikbare modellen (Debug)")

if api_key:
    try:
        # Configuratie met stabiele transportmethode
        genai.configure(api_key=api_key, transport='rest')
        
        if debug_mode:
            models = [m.name for m in genai.list_models()]
            st.sidebar.write(models)

        # We gebruiken Gemini 2.0 Flash met de NIEUWE zoekfunctie naamgeving
        model = genai.GenerativeModel(
            model_name='models/gemini-2.0-flash',
            tools=[{'google_search': {}}],
            generation_config={"temperature": temp_value}
        )
        
        # Gebruikersinvoer velden
        col1, col2 = st.columns(2)
        
        with col1:
            target_url = st.text_input("Target URL (Het te verbeteren artikel)", placeholder="https://www.jouwdomein.nl/blog-artikel")
            keywords = st.text_area("Belangrijke Keywords & Focuspunten", placeholder="Bijv: AI content creatie, SEO strategie 2026")
            
        with col2:
            ref_urls = st.text_area("Referentie URL's voor Tone of Voice (één per regel)", placeholder="https://www.voorbeeld.nl/goede-stijl")

        # De actieknop
        if st.button("Start GEO-Optimalisatie", use_container_width=True):
            if target_url and ref_urls:
                with st.spinner('Gemini 2.0 analyseert de bronnen en herschrijft de content...'):
                    try:
                        # De prompt met jouw specifieke GEO-regels
                        prompt = f"""
                        JE BENT EEN SENIOR GEO SPECIALIST (Generative Engine Optimization). 
                        Je taak is om het blogartikel op {target_url} te transformeren zodat LLM's het optimaal begrijpen en citeren.
                        
                        GEBRUIK DEZE BRONNEN:
                        1. Analyseer de volledige inhoud van: {target_url}
                        2. Gebruik de Tone of Voice van deze voorbeelden: {ref_urls}
                        3. Integreer deze keywords natuurlijk: {keywords}
                        
                        STRIKTE GEO-RICHTLIJNEN VOOR STRUCTUUR:
                        - LOGISCHE HIERARCHIE: Gebruik exact één H1. Gebruik H2 voor hoofdthema's en H3 voor subdetails.
                        - Q&A KNOWLEDGE SNAPSHOT: Plaats direct onder de H1 een sectie 'Kernvragen beantwoord' in Q&A format (3 vragen + antwoorden van max 40 woorden).
                        - ENTITY-DENSE OPENINGS: De eerste 40 tot 50 woorden na ELKE heading (H2/H3) moeten de belangrijkste entiteiten (onderwerpen, merken, begrippen) expliciet benoemen.
                        - KORTE PARAGRAFEN: Elke alinea mag maximaal 3-4 zinnen bevatten (focus op Flesch Reading Ease).
                        - FRONT-LOADING: Zet de belangrijkste definitie of het antwoord direct bovenaan elke sectie.
                        - LIJSTEN & TABELLEN: Zet complexe informatie om in een <ul>, <ol> of <table>.
                        - SEMANTISCHE CUES: Gebruik gids-woorden zoals "In essentie", "Belangrijkste takeaway", "Stap 1".
                        - NOISE REDUCTION: Verwijder fluff en interruptieve elementen.
                        - FOOTER: Sluit af met een kleine tabel met feiten, de datum van vandaag en een "Licentie: CC-BY" note.
                        
                        Lever het resultaat op in een prachtig opgemaakte Markdown tekst.
                        """
                        
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.subheader("Geoptimaliseerd Artikel")
                        st.markdown(response.text)
                        
                        # Download knop
                        st.download_button(
                            label="Download resultaat als Markdown",
                            data=response.text,
                            file_name="geo-artikel.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"Er ging iets mis tijdens het genereren: {e}")
                        st.info("Tip: Soms is de Google Search tool tijdelijk overbelast. Probeer het over een paar seconden opnieuw.")
            else:
                st.warning("Zorg dat je in ieder geval de Target URL en de Referentie URL's hebt ingevuld.")
                
    except Exception as e:
        st.error(f"Configuratie fout: {e}")
else:
    st.info("Voer je Gemini API Key in de zijbalk in om de tool te activeren.")
