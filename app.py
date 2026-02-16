import streamlit as st
from datetime import timedelta, datetime
import pandas as pd

# 1. CONFIGURATION & DESIGN AVANCÉ
st.set_page_config(page_title="Agnel'Plan", page_icon="🐑", layout="centered")

# Injection de polices et style CSS personnalisé
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap');

    .stApp { background-color: #F8F5F2; }
    
    /* Titres */
    h1 { font-family: 'Playfair Display', serif; color: #2C3E50; font-size: 3rem !important; padding-bottom: 0; }
    .subtitle { font-family: 'Playfair Display', serif; font-style: italic; color: #7F8C8D; font-size: 1.2rem; margin-bottom: 2rem; }
    
    /* Cartes d'information */
    .event-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4A5D4E;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* Bouton Principal */
    .stButton>button {
        background-color: #4A5D4E;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2rem;
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #38473b; transform: translateY(-2px); }
    
    /* Sidebar et Expander */
    .stExpander { border: none !important; background-color: #EFEBE7 !important; border-radius: 12px !important; }
    
    /* Inputs */
    div[data-baseweb="input"] { border-radius: 8px !important; border: 1px solid #D1C4B9 !important; }
    </style>
    """, unsafe_allow_html=True)

# EN-TÊTE STYLISÉ
st.markdown("<h1>Agnel'Plan</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>L'expertise bergère au service du temps</p>", unsafe_allow_html=True)

# 2. PANNEAU DE CONFIGURATION
with st.container():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        nom_lot = st.text_input("📦 Nom du lot", value="Lot Printemps")
    with c2:
        date_debut_lutte = st.date_input("📅 Début de lutte", datetime.now())
    with c3:
        nb_cycles = st.number_input("🔄 Cycles", min_value=1, value=2)

# 3. RÉGLAGES AVANCÉS DANS UN STYLE ÉPURÉ
with st.expander("⚙️ Ajuster le protocole"):
    st.markdown("<p style='font-size: 0.9rem; color: #7F8C8D;'>Modifiez les délais par défaut (en jours) :</p>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)
    d_echo = col_r1.number_input("Écho (J+ fin)", value=45)
    d_flush = col_r2.number_input("Flushing (J- MB)", value=20)
    d_sevrage = col_r3.number_input("Sevrage (J+ MB)", value=70)
    
    st.divider()
    if 'customs' not in st.session_state:
        st.session_state.customs = []
    
    c_nom = st.text_input("✏️ Note personnalisée (ex: Tonte, Pieds)")
    cx1, cx2, cx3 = st.columns([2, 1, 1])
    c_ref = cx1.selectbox("Référence", ["Avant MB", "Après MB"])
    c_jours = cx2.number_input("Nb Jours", value=10)
    if cx3.button("Ajouter à la liste"):
        if c_nom:
            st.session_state.customs.append({"nom": c_nom, "ref": c_ref, "jours": c_jours})
            st.rerun()

# 4. CALCULS LOGIQUES
d_lutte = nb_cycles * 16
date_fin_lutte = date_debut_lutte + timedelta(days=d_lutte)
date_mb_deb = date_debut_lutte + timedelta(days=147)
date_mb_fin = date_fin_lutte + timedelta(days=152)

# Liste des événements
plan = [
    {"icon": "🐏", "label": "Lutte", "date": f"Du {date_debut_lutte.strftime('%d/%m')} au {date_fin_lutte.strftime('%d/%m')}", "start": date_debut_lutte, "end": date_fin_lutte},
    {"icon": "🩺", "label": "Échographie", "date": (date_fin_lutte + timedelta(days=d_echo)).strftime('%d %b %Y'), "start": date_fin_lutte + timedelta(days=d_echo)},
    {"icon": "🌾", "label": "Flushing", "date": (date_mb_deb - timedelta(days=d_flush)).strftime('%d %b %Y'), "start": date_mb_deb - timedelta(days=d_flush)},
    {"icon": "✨", "label": "Mises bas", "date": f"Du {date_mb_deb.strftime('%d/%m')} au {date_mb_fin.strftime('%d/%m')}", "start": date_mb_deb, "end": date_mb_fin},
    {"icon": "🍼", "label": "Sevrage", "date": (date_mb_deb + timedelta(days=d_sevrage)).strftime('%d %b %Y'), "start": date_mb_deb + timedelta(days=d_sevrage)},
]

# Ajout des personnalisés
for ev in st.session_state.customs:
    d_ev = (date_mb_deb - timedelta(days=ev['jours'])) if ev['ref'] == "Avant MB" else (date_mb_deb + timedelta(days=ev['jours']))
    plan.append({"icon": "📝", "label": ev['nom'], "date": d_ev.strftime('%d %b %Y'), "start": d_ev})

# 5. AFFICHAGE STYLE "JOURNAL"
st.markdown(f"### 📋 Planning du lot : {nom_lot}")

for item in plan:
    st.markdown(f"""
        <div class="event-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.2rem; font-weight: 700; color: #2C3E50;">{item['icon']} {item['label']}</span>
                <span style="font-family: 'Lato'; color: #4A5D4E; font-weight: 700;">{item['date']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6. EXPORT ICS
def create_ics():
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//AgnelPlan//FR", "CALSCALE:GREGORIAN"]
    for p in plan:
        ics.append("BEGIN:VEVENT")
        ics.append(f"SUMMARY:{p['label']} - {nom_lot}")
        ics.append(f"DTSTART;VALUE=DATE:{p['start'].strftime('%Y%m%d')}")
        end_date = p.get('end', p['start']) + timedelta(days=1)
        ics.append(f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}")
        ics.append("END:VEVENT")
    ics.append("END:VCALENDAR")
    return "\n".join(ics)

st.divider()
st.download_button(
    label="📲 Synchroniser avec mon Agenda",
    data=create_ics(),
    file_name=f"AgnelPlan_{nom_lot}.ics",
    mime="text/calendar",
    use_container_width=True
)

if st.session_state.customs:
    if st.button("🗑️ Réinitialiser les notes"):
        st.session_state.customs = []
        st.rerun()
