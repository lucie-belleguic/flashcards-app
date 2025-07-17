import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from flashcard_db import StatsManager

# Configuration de la mise en page de la page Streamlit
st.set_page_config(page_title="Statistiques", page_icon="📊", layout="wide")

# Initialisation des gestionnaires
sm = StatsManager()
print("\n Gestionnaires initialisés avec succès.")
print("\n")

# ================================================
# ========= Titre de la page principale ==========
# ================================================
st.markdown(
    "<h1 style='text-align: center;'>📊 Statistiques de vos révisions</h1>",
    unsafe_allow_html=True,
)
st.divider()

# ================================================
# ===== Configuration de la page principale  =====
# ================================================

# Récupération des données
stats = sm.get_stats()

# Affichage des résultats
if not stats:
    st.warning("Aucune statistique enregistrée.")
else:
    df = pd.DataFrame(
        stats, columns=["ID", "Bonnes réponses", "Mauvaises réponses", "Date"]
    )
    # Convertion de la date au format YYYY-MM-JJ
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values(by="Date")
    df = df[["Date", "Bonnes réponses", "Mauvaises réponses"]]

    # Calcul du taux de réussite quotidient
    df["Taux de réussite (%)"] = (
        df["Bonnes réponses"] / (df["Bonnes réponses"] + df["Mauvaises réponses"]) * 100
    ).round(1)

    # Dernière ligne du DataFrame
    dernier_jour = df.iloc[-1]

    # Affichage du résumé du jour
    st.markdown(f"### 🧾 Résumé du jour — {dernier_jour['Date']}")
    col1, col2, col3, _ = st.columns(4)
    col1.metric("✅ Bonnes réponses", dernier_jour["Bonnes réponses"])
    col2.metric("❌ Mauvaises réponses", dernier_jour["Mauvaises réponses"])
    col3.metric("🎯 Taux de réussite", f"{dernier_jour['Taux de réussite (%)']:.1f} %")

    st.markdown("### 📋 Tableau des performances quotidiennes")
    st.dataframe(df, use_container_width=True)

    # Création de la figure Plotly
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Bonnes réponses"],
            mode="lines+markers",
            name="Bonnes réponses",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Mauvaises réponses"],
            mode="lines+markers",
            name="Mauvaises réponses",
        )
    )

    # Mise en forme
    fig.update_layout(
        yaxis_title="Nombre de réponses",
        xaxis=dict(tickangle=45),
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=80),
    )

    # Affichage dans Streamlit
    st.markdown("### 📈 Évolution des performances quotidiennes")
    st.plotly_chart(fig, use_container_width=True)
