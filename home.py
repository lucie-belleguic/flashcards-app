import streamlit as st
import pandas as pd
import os
import random

from flashcard_db import (
    Database,
    FlashcardManager,
    ThemeManager,
    StatsManager,
    FlashcardApp,
)

# Configuration de la mise en page de la page Streamlit
st.set_page_config(page_title="Accueil", page_icon=":house:", layout="wide")

# Création de la base si elle n'existe pas encore
if not os.path.exists("flashcards.db"):
    print("Base de données non trouvée. Initialisation...")
    db = Database()
    db.init_db()
else:
    print("Base de données déjà existante.")

# Initialisation des gestionnaires
fm = FlashcardManager()
tm = ThemeManager()
sm = StatsManager()
fa = FlashcardApp()
print("\n Gestionnaires initialisés avec succès.")
print("\n")

# ================================================
# ========= Titre de la page principale ==========
# ================================================
st.markdown(
    "<h1 style='text-align: center;'>🃏 Flashcards Application</h1>",
    unsafe_allow_html=True,
)
st.divider()

# ================================================
# ====== Configuration de la barre latérale ======
# ================================================
themes = tm.get_all_themes()
theme_names = [t[1] for t in themes]

st.sidebar.title("Configuration du quizz")
st.sidebar.write("###")

st.sidebar.subheader("📚 Thèmes du quizz")
# Sélection des thèmes
themes_selection = st.sidebar.multiselect(
    "Sélectionnez les thèmes à travailler :", options=theme_names
)
st.sidebar.write("###")

st.sidebar.subheader("🎯 Nombre de questions du quizz")
# Choix du nombre de questions àn poser
nb_questions = st.sidebar.slider(
    "Nombre de questions à poser :", min_value=1, max_value=20, value=5
)


# ================================================
# ===== Configuration de la page principale  =====
# ================================================

# Centrer le contenu avec des colonnes
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Sélectionnez les thèmes puis lancez le quizz")

    # Initialisation des variables de session
    if "carte_active" not in st.session_state:
        st.session_state.carte_active = None
    if "cartes_quizz" not in st.session_state:
        st.session_state.cartes_quizz = []
    if "nb_reponses" not in st.session_state:
        st.session_state.nb_reponses = 0
    if "reponse_visible" not in st.session_state:
        st.session_state.reponse_visible = False

    # Lancement du quizz
    if st.button("🎲 Lancer le quizz!"):
        if themes_selection:
            # Récupère les IDs des thèmes sélectionnés
            theme_ids = [t[0] for t in themes if t[1] in themes_selection]
            # Récupérer toutes les cartes correspondant à une liste d'identifiants de thème
            all_cards = fa.get_cards_by_themes(theme_ids)

            if not all_cards:
                st.warning("Aucune carte trouvée pour ces thèmes.")
            else:
                tirage = random

                # Tirage des cartes au sort parmis la sélection et en fonction de la probabilité
                tirage = fa.pick_card_weighted(cartes=all_cards, k=nb_questions)
                print(
                    f"{nb_questions} cartes tirées au sort parmis les thèmes sélectionnés."
                )
                st.session_state.cartes_quizz = tirage
                st.session_state.nb_reponses = 0
                st.session_state.carte_active = st.session_state.cartes_quizz[0]
                st.session_state.reponse_visible = False
                st.success(f"{len(tirage)} carte(s) tirée(s) pour le quizz.")
        else:
            st.warning("Veuillez sélectionner au moins un thème.")

    # Affichage d'une question si une carte est active
    if st.session_state.carte_active:
        carte = st.session_state.carte_active
        st.markdown(f"**❓ Question {carte[0]} :** {carte[1]}")

        # Champ de réponse libre
        user_input = st.text_input("Votre réponse :", key="reponse_utilisateur")

        # Bouton pour afficher la réponse
        if st.button("Voir la réponse"):
            st.session_state.reponse_visible = True

        if st.session_state.reponse_visible:
            st.markdown(f"**✔️ Réponse attendue :** {carte[2]}")
            is_correct = st.radio(
                "Aviez-vous juste ?", options=["Oui", "Non"], horizontal=True
            )

            if st.button("📥 Valider"):
                correct_bool = is_correct == "Oui"
                fa.sm.update_stats(correct_bool)
                fa.sm.update_card_probability(carte[0], correct_bool)
                st.success("Réponse enregistrée ✅")

                st.session_state.nb_reponses += 1
                if st.session_state.nb_reponses < len(st.session_state.cartes_quizz):
                    st.session_state.carte_active = st.session_state.cartes_quizz[
                        st.session_state.nb_reponses
                    ]
                    st.session_state.reponse_visible = False
                    st.rerun()
                else:
                    st.success("🎉 Quizz terminé !")
                    st.session_state.carte_active = None
                    st.session_state.cartes_quizz = []
                    st.session_state.nb_reponses = 0
