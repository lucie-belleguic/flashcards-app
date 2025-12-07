# 🃏 **Flashcards**

## *Application de révision interactive*

Bienvenue dans mon projet **Flashcards**, une application interactive de révision conçue pour **préparer les entretiens de Data Scientist, Data Analyst ou Ingénieur IA**.

L'application permet de s'entraîner sur des questions réparties par thème, avec un suivi statistique et une logique de sélection intelligente pour favoriser la mémorisation.   
La base actuelle contient des questions orientées Data/IA, fournies à titre d'exemple, mais l'application peut être utilisée pour tout autre domaine : révision de langues, cours d’histoire, culture générale, etc.  
Il est possible d’ajouter facilement vos propres thèmes et cartes via l’interface ou directement en base de données.

---

## 🚀 Fonctionnalités principales

- 📚 Révision de questions par thème (SQL, Python, ML, etc.)
- ⚖️ Sélection des cartes pondérée selon les erreurs passées
- 📈 Statistiques de progression par jour et par thème
- 🛠️ Interface interactive via **Streamlit**
- 💾 Sauvegarde des données en **SQLite**
- 🧠 Système d’auto-évaluation des réponses

---

## 🧰 Stack technique

- **Python**
- **SQLite** (via `sqlite3`)
- **Streamlit** pour l’interface web
- **Pandas** pour la manipulation de données
- Architecture orientée objet (OOP)

---

## 🛠️ Installation

1. **Cloner le dépôt**

```bash
git clone https://github.com/lucie-belleguic/flashcards-app.git
cd flashcards-app
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Lancer l'application**

```bash
streamlit run home.py
```

4. **Accéder à l'application**
   - Ouvrir votre navigateur à l'adresse : `http://localhost:8501`

---

## 🎮 Utilisation

### Page principale (Home)

- Interface de révision des flashcards
- Configuration des préférences d'apprentissage
- Affichage des questions et saisie des réponses
- Validation immédiate avec feedback

### Statistiques

- Graphiques de performance
- Suivi des taux de réussite
- Analyse des progrès dans le temps

### Paramètres

- Gestion des thèmes (modification, ajout, suppression)
- Gestion des flashcards (consultation, modification, ajout, suppression)

---

## 📁 Structure du projet

```
flashcards-app/
├── pages/
│   ├── 1_statistiques.py    # Page des statistiques et graphiques
│   └── 2_parametres.py      # Page de configuration
├── flashcard_db.py          # Classes et méthodes pour la base de données
├── flashcards.db            # Base de données SQLite (inclut des exemples)
├── home.py                  # Interface principale Streamlit
├── requirements.txt         # Dépendances Python
├── README.md                # Fichier de présentation du projet
├── LICENSE                  # Fichier de licence (MIT)
└── .gitignore               # Fichiers à ignorer par Git
```
---

## 🗃️ Base de données

L'application utilise une base de données SQLite avec les tables suivantes :

- **cards** : Stockage des questions, réponses et métadonnées des flashcards
- **themes** : Catégories et thématiques d'organisation des cartes
- **stats** : Données de performance et statistiques d'apprentissage

La base de données est pré-remplie avec des exemples de flashcards pour une démonstration immédiate.

---

## ⚙️ Fonctionnalités techniques

- **Architecture modulaire** : Séparation claire entre logique métier et interface
- **Gestion d'état** : Utilisation des sessions Streamlit pour la persistance
- **Visualisations interactives** : Graphiques dynamiques avec Plotly
- **Base de données relationnelle** : Conception normalisée et optimisée

---

## 🚀 Déploiement

Cette application peut être déployée sur :

- **Streamlit Cloud** (recommandé)

---

## 🔭 Développement futur

Améliorations possibles :
- Système de révision espacée (algorithme de Leitner)
- Analyse automatique des réponses
- Import/export de jeux de flashcards
- Mode multijoueur

---

## 🎓 Contexte

Ce projet a été développé dans le cadre d'une formation en développement Python. Il démontre :

- La conception et l'implémentation d'une base de données
- Le développement d'une interface utilisateur moderne
- L'intégration de visualisations de données
- Les bonnes pratiques de développement Python

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENCE pour plus de détails.

