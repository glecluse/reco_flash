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

image = Image.open("image.png")

# Redimensionner l'image (diviser par 2)
new_size = (int(image.width / 1.7), int(image.height / 1.7))
resized_image = image.resize(new_size)

# Afficher l'image redimensionnée
st.image(resized_image)

st.write("""En fonction de vos réponses, l'outil vous fournira des recommandations personnalisées pour renforcer chaque aspect et vous guider dans la définition d'une vision claire et stratégique pour l'avenir de votre entreprise.""")

st.write("Prêt à commencer ?")
st.write("")

# Rediriger vers la page "main.py" en cliquant sur le bouton
if st.button("C'est parti !"):
    st.switch_page("pages/formulaire.py")  # Chemin correct vers la page



# CSS pour fixer le footer
footer_style = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            text-align: center;
            padding: 10px;
            box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
        }
    </style>
"""

# Appliquer le CSS
st.markdown(footer_style, unsafe_allow_html=True)

# Affichage du footer avec une image locale via st.image()
footer_container = st.empty()
with footer_container.container():
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.image("lpde.png", width=600)  # ✅ Chemin corrigé et compatible
    st.markdown('</div>', unsafe_allow_html=True)


