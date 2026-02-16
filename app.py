import streamlit as st
from datetime import timedelta, datetime
import pandas as pd

# 1. CONFIGURATION & STYLE VINTAGE
st.set_page_config(page_title="Agnel'Plan", page_icon="🐑", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, p, label, span { color: #4A3728 !important; font-family: 'Georgia', serif; }
    .stButton>button { 
        background-color: #4A3728; color: #FDFBF7; border-radius: 5px; 
        border: none; font-weight: bold; width: 100%;
    }
    .stExpander { border: 1px solid #D1C4B9; background-color: #F9F7F2; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# EN-TÊTE
st.title("🐑 Agnel'Plan")
st.write("*Carnet de bergerie*")

# 2. PARAMÈTRES DU LOT (ÉCRAN PRINCIPAL)
with st.container():
    c1, c2, c3 = st.columns([2, 2, 1])
    nom_lot = c1.text_input("Nom du lot", value="Lot Printemps")
    date_debut_lutte = c2.date_input("Début lutte", datetime.now())
    nb_cycles = c3.number_input("Cycles", min_value=1, value=2)

# 3. RÉGLAGES AVANCÉS & ÉVÉNEMENTS PERSO
with st.expander("⚙️ Réglages avancés & Événements personnalisés"):
    st.write("**Délais standards (jours) :**")
    col_r1, col_r2 = st.columns(2)
    d_echo = col_r1.number_input("Écho (J+ fin lutte)", value=45)
    d_flush = col_r1.number_input("Flushing (J- début MB)", value=20)
    d_sevrage = col_r2.number_input("Sevrage (J+ début MB)", value=70)
    d_vente = col_r2.number_input("Vente (J+ début MB)", value=90)
    
    st.divider()
    st.write("**Ajouter un événement spécifique :**")
    if 'customs' not in st.session_state:
        st.session_state.customs = []
    
    c_nom = st.text_input("Nom (ex: Tonte, Vermifuge)")
    cx1, cx2, cx3 = st.columns([2, 1, 1])
    c_ref = cx1.selectbox("Référence", ["Avant Mise bas", "Après Mise bas"])
    c_jours = cx2.number_input("Jours", value=10)
    if cx3.button("Ajouter"):
        if c_nom:
            st.session_state.customs.append({"nom": c_nom, "ref": c_ref, "jours": c_jours})
            st.rerun()

# 4. CALCULS
duree_lutte = nb_cycles * 16
date_fin_lutte = date_debut_lutte + timedelta(days=duree_lutte)
date_mb_deb = date_debut_lutte + timedelta(days=147)
date_mb_fin = date_fin_lutte + timedelta(days=152)

# Préparation de la liste finale
plan_data = [
    {"E": "🚀 Lutte", "D": f"Du {date_debut_lutte.strftime('%d/%m')} au {date_fin_lutte.strftime('%d/%m')}", "start": date_debut_lutte, "end": date_fin_lutte},
    {"E": "🩺 Échographie", "D": (date_fin_lutte + timedelta(days=d_echo)).strftime('%d/%m/%Y'), "start": date_fin_lutte + timedelta(days=d_echo)},
    {"E": "🌾 Flushing", "D": (date_mb_deb - timedelta(days=d_flush)).strftime('%d/%m/%Y'), "start": date_mb_deb - timedelta(days=d_flush)},
    {"E": "🐣 Mises bas", "D": f"Du {date_mb_deb.strftime('%d/%m')} au {date_mb_fin.strftime('%d/%m')}", "start": date_mb_deb, "end": date_mb_fin},
    {"E": "🍼 Sevrage", "D": (date_mb_deb + timedelta(days=d_sevrage)).strftime('%d/%m/%Y'), "start": date_mb_deb + timedelta(days=d_sevrage)},
    {"E": "💰 Vente", "D": (date_mb_deb + timedelta(days=d_vente)).strftime('%d/%m/%Y'), "start": date_mb_deb + timedelta(days=d_vente)},
]

# Ajout des personnalisés
for ev in st.session_state.customs:
    delta = timedelta(days=ev['jours'])
    d_ev = (date_mb_deb - delta) if ev['ref'] == "Avant Mise bas" else (date_mb_deb + delta)
    plan_data.append({"E": f"⭐ {ev['nom']}", "D": d_ev.strftime('%d/%m/%Y'), "start": d_ev})

# 5. AFFICHAGE DU TABLEAU
st.divider()
st.subheader(f"📅 Planning : {nom_lot}")
df_display = pd.DataFrame([{"Événement": item["E"], "Date / Période": item["D"]} for item in plan_data])
st.table(df_display)

# 6. EXPORT ICS
def create_ics():
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//AgnelPlan//FR", "CALSCALE:GREGORIAN"]
    for item in plan_data:
        ics.append("BEGIN:VEVENT")
        ics.append(f"SUMMARY:{item['E']} - {nom_lot}")
        ics.append(f"DTSTART;VALUE=DATE:{item['start'].strftime('%Y%m%d')}")
        end_date = item.get('end', item['start']) + timedelta(days=1)
        ics.append(f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}")
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

if st.session_state.customs:
    if st.button("🗑️ Effacer les événements personnalisés"):
        st.session_state.customs = []
        st.rerun()
