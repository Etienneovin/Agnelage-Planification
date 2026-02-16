import streamlit as st
from datetime import timedelta, datetime
import pandas as pd

# 1. STYLE VINTAGE
st.set_page_config(page_title="Agnel'Plan", page_icon="🐑")

st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, p, label { color: #4A3728 !important; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #4A3728; color: #FDFBF7; border-radius: 5px; border: none; }
    .stTable { border: 1px solid #4A3728; }
    </style>
    """, unsafe_allow_html=True)

# 2. EN-TÊTE
st.title("🐑 Agnel'Plan")
st.write("*Carnet de bergerie — Style Tachainville*")
st.divider()

# 3. SAISIE DU LOT
col1, col2 = st.columns(2)
with col1:
    nom_lot = st.text_input("Nom du lot", value="Lot Printemps")
    date_debut = st.date_input("Date début lutte", datetime.now())
with col2:
    nb_cycles = st.number_input("Nombre de cycles", min_value=1, max_value=4, value=2)
    st.caption(f"Durée : {nb_cycles * 16} jours")

# 4. CALCULS ÉPURÉS
date_fin_l = date_debut + timedelta(days=nb_cycles * 16)
date_mb_deb = date_debut + timedelta(days=147)
date_mb_fin = date_fin_l + timedelta(days=152)

# Événements clés
planning = [
    {"Étape": "🚀 Lutte", "Date": f"Du {date_debut.strftime('%d/%m')} au {date_fin_l.strftime('%d/%m')}"},
    {"Étape": "🩺 Échographie", "Date": (date_fin_l + timedelta(days=45)).strftime('%d/%m/%Y')},
    {"Étape": "🌾 Flushing", "Date": (date_mb_deb - timedelta(days=20)).strftime('%d/%m/%Y')},
    {"Étape": "🐣 Mises bas", "Date": f"Du {date_mb_deb.strftime('%d/%m')} au {date_mb_fin.strftime('%d/%m')}"},
    {"Étape": "🍼 Sevrage", "Date": (date_mb_deb + timedelta(days=70)).strftime('%d/%m/%Y')},
    {"Étape": "💰 Vente agneaux", "Date": (date_mb_deb + timedelta(days=90)).strftime('%d/%m/%Y')},
]

# 5. AFFICHAGE
st.subheader(f"📅 Planning : {nom_lot}")
st.table(pd.DataFrame(planning))

# 6. EXPORT AGENDA
def create_ics():
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//AgnelPlan//FR"]
    for p in planning:
        ics.append("BEGIN:VEVENT")
        ics.append(f"SUMMARY:{p['Étape']} ({nom_lot})")
        # Note: Pour simplifier l'export, on utilise la date de début de chaque étape
        d_val = date_debut # Valeur par défaut
        ics.append(f"DTSTART;VALUE=DATE:{date_debut.strftime('%Y%m%d')}") 
        ics.append("END:VEVENT")
    ics.append("END:VCALENDAR")
    return "\n".join(ics)

st.download_button(
    label="📲 Enregistrer dans mon agenda",
    data=create_ics(),
    file_name=f"Planning_{nom_lot}.ics",
    mime="text/calendar",
    use_container_width=True
)
