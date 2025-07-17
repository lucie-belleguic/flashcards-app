import streamlit as st
import pandas as pd
from flashcard_db import FlashcardManager, ThemeManager

# Configuration de la mise en page de la page Streamlit
st.set_page_config(page_title="Paramètres", page_icon="🛠️", layout="wide")

# Initialisation des gestionnaires
fm = FlashcardManager()
tm = ThemeManager()
print("\n Gestionnaires initialisés avec succès.")
print("\n")

# ================================================
# ========= Titre de la page principale ==========
# ================================================
st.markdown(
    "<h1 style='text-align: center;'>🛠️ Paramètres</h1>",
    unsafe_allow_html=True,
)
st.divider()

# ================================================
# ============= Gestion de l'état UI =============
# ================================================

if "show_modif_theme" not in st.session_state:
    st.session_state.show_modif_theme = False

if "show_add_theme" not in st.session_state:
    st.session_state.show_add_theme = False

if "show_delete_theme" not in st.session_state:
    st.session_state.show_delete_theme = False

if "show_modif_card" not in st.session_state:
    st.session_state.show_modif_card = False

if "show_add_card" not in st.session_state:
    st.session_state.show_add_card = False

if "show_delete_card" not in st.session_state:
    st.session_state.show_delete_card = False

if "card_id_to_modify" not in st.session_state:
    st.session_state.card_id_to_modify = None

if "card_id_to_delete" not in st.session_state:
    st.session_state.card_id_to_delete = None

if "show_get_card" not in st.session_state:
    st.session_state.show_get_card = False

if "card_id_to_get" not in st.session_state:
    st.session_state.card_id_to_get = None

# ================================================
# ============= Gestion des thèmes ===============
# ================================================

st.markdown("## **Gestion des thèmes**")

themes = tm.get_all_themes()
theme_names = [t[1] for t in themes]

_, col1, _, col2, _, col3, _ = st.columns((1, 3, 1, 3, 1, 3, 1))

#########################################################
# Bouton pour afficher le formulaire de modification d'un thème
with col1:
    if st.button("Modifier un thème"):
        st.session_state.show_modif_theme = True

# Formulaire de modification d'un thème
if st.session_state.show_modif_theme:
    st.markdown("#### Modifier un thème")
    with st.form("form_modif_theme"):
        theme_to_modify = st.selectbox("Choisissez un thème à modifier", theme_names)
        new_theme = st.text_input("Nouveau nom du thème")
        submitted = st.form_submit_button("Valider la modification")

        if submitted:
            id_theme = [t[0] for t in themes if t[1] == theme_to_modify][0]
            tm.update_theme(id_theme, new_theme=new_theme)
            st.success(f"Thème modifié : {theme_to_modify} → {new_theme}")
            st.session_state.show_modif_theme = False
            st.rerun()  # Recharge avec le nouveau thème

#########################################################
# Bouton pour afficher le formulaire d'ajout d'un thème
with col2:
    if st.button("Ajouter un thème"):
        st.session_state.show_add_theme = True

# Formulaire d'ajout d'un thème
if st.session_state.show_add_theme:
    st.markdown("#### Ajouter un thème")
    with st.form("form_add_theme"):
        new_theme = st.text_input("Nouveau thème")
        submitted = st.form_submit_button("Valider la modification")

        if submitted:
            tm.create_theme(theme=new_theme)
            st.success(f"Thème ajouté : {new_theme}")
            st.session_state.show_add_theme = False
            st.rerun()  # Recharge avec le nouveau thème

#########################################################
# Bouton pour afficher le formulaire de suppression d'un thème
with col3:
    if st.button("Supprimer un thème"):
        st.session_state.show_delete_theme = True

# Formulaire de suppression d'un thème
if st.session_state.show_delete_theme:
    st.markdown("#### Supprimer un thème")
    with st.form("form_delete_theme"):
        theme_to_delete = st.selectbox("Choisissez un thème à supprimer", theme_names)
        submitted = st.form_submit_button("Valider la suppression")

        if submitted:
            id_theme = [t[0] for t in themes if t[1] == theme_to_delete][0]
            tm.delete_theme(id_theme)
            st.success(f"Thème supprimé : {theme_to_delete}")
            st.session_state.show_delete_theme = False
            st.rerun()  # Recharge sans l'ancien thème

# ================================================
# ============= Gestion des cartes ===============
# ================================================

st.markdown("## **Gestion des cartes**")

cards = fm.get_all_cards()
nb_cards = fm.get_number_of_cards()
card_ids = [c[2] for c in cards]

#########################################################
# Afficher le contenu d'une carte
_, col1, _ = st.columns((1, 3, 9))

# Bouton pour afficher le contenu d'une carte
with col1:
    if st.button("Afficher une carte"):
        st.session_state.show_get_card = True

# Formulaire de sélection de la carte à modifier
if st.session_state.show_get_card and st.session_state.card_id_to_get is None:
    st.markdown("#### Afficher une carte")
    with st.form("form_get_card"):
        id_card_to_get = st.number_input(
            "Numéro de la carte à afficher",
            min_value=1,
            step=1,
        )
        check = st.form_submit_button("Afficher")

        if check:
            card = fm.get_card(id_card_to_get)
            if card:
                st.session_state.card_id_to_get = id_card_to_get
                st.rerun()
            else:
                st.error("❌ Aucune carte ne correspond à cet identifiant.")

# Affichage de la carte sélectionnée
if st.session_state.card_id_to_get is not None:
    card = fm.get_card(st.session_state.card_id_to_get)
    theme_of_card = tm.get_theme(card[4])[1]

    st.markdown(f"**🆔 Numéro de la carte :** {card[0]}")
    st.markdown(f"**❓ Question :** {card[1]}")
    st.markdown(f"**✔️ Réponse :** {card[2]}")
    st.markdown(f"**📚 Thème :** {card [4]} - {theme_of_card}")

    if st.button("Fermer l'affichage"):
        st.session_state.card_id_to_get = None
        st.session_state.show_get_card = False
        st.rerun()

#########################################################

_, col1, _, col2, _, col3, _ = st.columns((1, 3, 1, 3, 1, 3, 1))

#########################################################
# Bouton pour afficher le formulaire de modification d'une carte
with col1:
    if st.button("Modifier une carte"):
        st.session_state.show_modif_card = True

# Formulaire de sélection de la carte à modifier
if st.session_state.show_modif_card:
    st.markdown("#### Modifier une carte")
    with st.form("form_modif_card"):
        id_card_to_modif = st.number_input(
            "Numéro de la carte à modifier",
            min_value=1,
            step=1,
        )
        check = st.form_submit_button("Vérifier")

        if check:
            st.markdown("**Vérifiez les informations de la carte avant de valider :**")
            card = fm.get_card(id_card_to_modif)
            if card:
                st.session_state.card_id_to_modify = id_card_to_modif
                st.rerun()
            else:
                st.error("❌ Aucune carte ne correspond à cet identifiant.")

# Formulaire de modification (après vérification)
if st.session_state.card_id_to_modify is not None:
    card = fm.get_card(st.session_state.card_id_to_modify)
    theme_of_card = tm.get_theme(card[4])[1]

    st.markdown("#### Modifier la carte sélectionnée")
    with st.form("form_update_card"):
        st.markdown(f"**🆔 Numéro de la carte :** {card[0]}")
        st.markdown(f"**❓ Question :** {card[1]}")
        st.markdown(f"**✔️ Réponse :** {card[2]}")
        st.markdown(f"**📚 Thème :** {card [4]} - {theme_of_card}")

        new_question = st.text_input(
            "Nouvelle question (laisser vide pour ne pas modifier)"
        )
        new_answer = st.text_input(
            "Nouvelle réponse (laisser vide pour ne pas modifier)"
        )
        new_theme = st.selectbox(
            "Nouveau thème (laissez le même pour ne pas changer)",
            options=theme_names,
            index=theme_names.index(theme_of_card),
        )

        submitted = st.form_submit_button("Valider la modification")

        if submitted:
            # Déduire les champs à modifier uniquement si remplis
            update_kwargs = {}

            if new_question.strip():
                update_kwargs["question"] = new_question

            if new_answer.strip():
                update_kwargs["reponse"] = new_answer

            if new_theme != theme_of_card:
                new_id_theme = [t[0] for t in themes if t[1] == new_theme][0]
                update_kwargs["id_theme"] = new_id_theme

            if update_kwargs:
                fm.update_card(id=card[0], **update_kwargs)
                st.success(f"Numéro de la carte supprimée : {id_card_to_modif}")
            else:
                st.info("Aucun champ modifié. La carte reste inchangée.")

            st.session_state.card_id_to_modify = None
            st.session_state.show_modif_card = False
            st.rerun()

#########################################################
# Bouton pour afficher le formulaire d'ajout d'une carte
with col2:
    if st.button("Ajouter une carte"):
        st.session_state.show_add_card = True

# Formulaire d'ajout d'une carte
if st.session_state.show_add_card:
    st.markdown("#### Ajouter une carte")
    with st.form("form_add_card"):
        question = st.text_input("Nouvelle question")
        reponse = st.text_input("Réponse")
        theme_of_card = st.selectbox(
            "Choisissez le thème correspondant à la carte", theme_names
        )
        id_theme_of_card = [t[0] for t in themes if t[1] == theme_of_card][0]
        submitted = st.form_submit_button("Valider la modification")

        if submitted:
            fm.create_card(
                question=question, reponse=reponse, id_theme=id_theme_of_card
            )
            st.success(f"Question ajoutée : {question}")
            st.session_state.show_add_card = False
            st.rerun()  # Recharge avec la nouvelle question

#########################################################
# Bouton pour afficher le formulaire de suppression d'une carte
with col3:
    if st.button("Supprimer une carte"):
        st.session_state.show_delete_card = True

# Formulaire de sélection de la carte à modifier
if st.session_state.show_delete_card:
    st.markdown("#### Supprimer une carte")
    with st.form("form_delete_card"):
        id_card_to_delete = st.number_input(
            "Numéro de la carte à supprimer",
            min_value=1,
            step=1,
        )
        check = st.form_submit_button("Vérifier")

        if check:
            st.markdown("**Vérifiez les informations de la carte avant de valider :**")
            card = fm.get_card(id_card_to_delete)
            if card:
                st.session_state.card_id_to_delete = id_card_to_delete
                st.rerun()
            else:
                st.error("❌ Aucune carte ne correspond à cet identifiant.")

# Formulaire de modification (après vérification)
if st.session_state.card_id_to_delete is not None:
    card = fm.get_card(st.session_state.card_id_to_delete)
    theme_of_card = tm.get_theme(card[4])[1]

    st.markdown("#### Supprimer la carte sélectionnée")
    with st.form("form_confirm_delete"):
        st.markdown(f"**🆔 Numéro de la carte :** {card[0]}")
        st.markdown(f"**❓ Question :** {card[1]}")
        st.markdown(f"**✔️ Réponse :** {card[2]}")
        st.markdown(f"**📚 Thème :** {card [4]} - {theme_of_card}")

        submitted = st.form_submit_button("Valider la suppression")

        if submitted:
            fm.delete_card(st.session_state.card_id_to_delete)
            st.success(
                f"Numéro de la carte supprimée : {st.session_state.card_id_to_delete}"
            )
            st.session_state.card_id_to_delete = None
            st.session_state.show_delete_card = False
            st.rerun()
