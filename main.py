import streamlit as st
from PIL import Image

# Configuration sans barre latérale
st.set_page_config(initial_sidebar_state="collapsed")

# Masquer totalement la barre latérale avec du CSS
hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.title("Évaluation de la compétitivité de votre entreprise")

st.write("""
Ce questionnaire interactif en ligne est conçu pour vous aider à évaluer le niveau de compétitivité de votre entreprise.""")

st.write("""En explorant les 4 aspects essentiels d'une organisation pérenne, il vous permettra d'identifier vos forces et les domaines à améliorer.""") 

st.write("""En fonction de vos réponses, l'outil vous fournira des recommandations personnalisées pour renforcer chaque aspect et vous guider dans la définition d'une vision claire et stratégique pour l'avenir de votre entreprise.""")

st.write("Prêt à commencer ?")
st.write("")

# Rediriger vers la page "main.py" en cliquant sur le bouton
if st.button("C'est parti !"):
    st.switch_page("pages/formulaire.py")  # Chemin correct vers la page



