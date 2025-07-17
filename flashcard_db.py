import sqlite3
import random
from datetime import datetime


class Database:
    # === Initialisation d'une nouvelle instance de Database ===
    def __init__(self, db_name="flashcards.db"):
        self.db_name = db_name  # Stocke le nom de la base comme attribut d’objet

    # === Connection à la base ===
    def connect(self):
        # Créer une connexion à la base de données
        conn = sqlite3.connect(self.db_name)
        print("Connexion à la base de données réussie")
        # Active la vérification des clés étrangères
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # === Création des tables et insertion des thèmes ===
    def init_db(self):
        # Créer une connexion à la base de données
        conn = self.connect()
        # Créer un curseur pour exécuter les requêtes SQL
        cursor = conn.cursor()

        # Création des tables
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY,
        question TEXT,
        reponse TEXT,
        probabilite REAL,
        id_theme INTEGER, FOREIGN KEY (id_theme) REFERENCES themes(id_theme) ON DELETE RESTRICT
        );
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS themes (
        id_theme INTEGER PRIMARY KEY,
        theme TEXT
        );
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY,
        bonnes_reponses INTEGER,
        mauvaises_reponses INTEGER,
        date DATE
        );
        """
        )

        # Insertion des thèmes dans la table "themes"
        cursor.executemany(
            "INSERT OR IGNORE INTO themes (id_theme, theme) VALUES (?, ?)",
            [
                (1, "SQL"),
                (2, "Python et Pandas"),
                (3, "Machine Learning"),
                (4, "Visualisation de données"),
            ],
        )

        # Valider les modifications et fermer la connexion avec la base
        conn.commit()
        conn.close()
        print("Tables créées avec succès")


class FlashcardManager(Database):
    # la classe FlashcardManager hérite de la classe Database
    # === Fonctions CRUD pour les Flashcards ===
    def create_card(self, question, reponse, id_theme):
        # Créer une carte
        try:
            conn = self.connect()
            c = conn.cursor()
            probabilite = 0.5  # Probabilité fixée à 0.5 à la création de la carte
            c.execute(
                """
                INSERT INTO cards (question, reponse, probabilite, id_theme)
                VALUES (?, ?, ?, ?)
            """,
                (question, reponse, probabilite, id_theme),
            )
            conn.commit()
            print("✅ Carte crée avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la création de la carte : {e}")

        finally:
            conn.close()

    def get_card(self, id):
        # Récupérer une carte
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM cards WHERE id = ?", (id,))
            result = c.fetchone()
            if result is None:
                raise ValueError(f"⚠️ Carte avec l'id {id} introuvable.")
            else:
                print(f"✅ Carte avec l'id {id} récupérée avec succès.")
            return result

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération de la carte : {e}")
            return None

        finally:
            conn.close()

    def update_card(
        self, id, question=None, reponse=None, probabilite=None, id_theme=None
    ):
        # Mise à jour d'une carte
        try:
            conn = self.connect()
            c = conn.cursor()

            # Dictionnaire des champs à mettre à jour
            fields = {
                "question": question,
                "reponse": reponse,
                "probabilite": probabilite,
                "id_theme": id_theme,
            }
            # Filtrer uniquement ceux qui ne sont pas None
            updates = {k: v for k, v in fields.items() if v is not None}

            if not updates:
                print("⚠️ Aucun champ à mettre à jour.")
                return

            # Vérification de la probabilité si fournie
            if "probabilite" in updates:
                if not (0.1 <= updates["probabilite"] <= 1.0):
                    raise ValueError(
                        "❌ La probabilité doit être comprise entre 0.1 et 1.0."
                    )

            # Construction dynamique de la requête SQL
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [id]

            query = f"UPDATE cards SET {set_clause} WHERE id = ?"
            c.execute(query, values)
            # Si on modifie par exemple les champs reponse et probabilite, on obtient quelque chose équivalent à :
            # c.execute("UPDATE cards SET reponse = ?, probabilite = ? WHERE id = ?",(reponse, probabilite, id))

            if c.rowcount == 0:
                raise ValueError(f"⚠️ Carte avec l'id {id} introuvable.")

            conn.commit()
            print(f"✅ Carte avec l'id {id} mise à jour avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la mise à jour de la carte : {e}")

        finally:
            conn.close()

    def delete_card(self, id):
        # Supprimer une carte de la table cards
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("DELETE FROM cards WHERE id = ?", (id,))

            if c.rowcount == 0:
                raise ValueError(f"⚠️ Carte avec l'id {id} introuvable.")

            conn.commit()
            print(f"✅ Carte {id} supprimée avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de ... : {e}")

        finally:
            conn.close()

    def get_all_cards(self):
        # Récupérer toutes les cartes
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM cards")
            results = (
                c.fetchall()
            )  # Liste de tuples (id, question, reponse, probabilite, id_theme)

            if not results:
                print("⚠️ Aucune carte trouvée.")
                return []
            else:
                print(f"✅ {len(results)} carte(s) récupérée(s) avec succès.")
                return results

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des cartes : {e}")
            return []

        finally:
            conn.close()

    def get_number_of_cards(self):
        # Comptage des cartes
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM cards")
            result = c.fetchone()
            print("✅ Cartes comptées avec succès.")
            return result[0]

        except sqlite3.Error as e:
            print(f"❌ Erreur lors du comptage des cartes : {e}")
            return 0

        finally:
            conn.close()

    def get_cards_by_theme(self, id_theme):
        # Récupérer les cartes appartenant à un thème en particulier
        try:
            conn = self.connect()
            c = conn.cursor()

            # Vérifier si le thème existe
            c.execute("SELECT 1 FROM themes WHERE id_theme=?", (id_theme,))
            theme_exists = c.fetchone()
            if not theme_exists:
                print(f"⚠️ Le thème avec l'id {id_theme} n'existe pas.")
                return None

            c.execute("SELECT * FROM cards WHERE id_theme=?", (id_theme,))
            results = (
                c.fetchall()
            )  # Liste de tuples (id, question, reponse, probabilite, id_theme)

            if not results:
                print(f"⚠️ Aucune carte trouvée pour le thème {id_theme}.")
                return []
            else:
                print(
                    f"✅ {len(results)} carte(s) récupérée(s) pour le thème {id_theme}."
                )
                return results

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des cartes par thème : {e}")
            return []

        finally:
            conn.close()


class ThemeManager(Database):
    # la classe ThemeManager hérite de la classe Database
    # === Fonctions CRUD pour les Thèmes ===
    def create_theme(self, theme):
        # Créer un thème
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO themes (theme)
                VALUES (?)
            """,
                (theme,),
            )
            conn.commit()
            print("✅ Thème créé avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la création du thème : {e}")

        finally:
            conn.close()

    def get_theme(self, id_theme):
        # Récupérer un thème
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM themes WHERE id_theme = ?", (id_theme,))
            result = c.fetchone()

            if result is None:
                raise ValueError(f"⚠️ Thème avec l'id {id_theme} introuvable.")
            else:
                print(f"✅ Thème avec l'id {id_theme} récupéré avec succès.")

            return result

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération du thème : {e}")
            return None

        finally:
            conn.close()

    def update_theme(self, id_theme, new_theme=None):
        # Mise à jour d'un thème
        try:
            conn = self.connect()
            c = conn.cursor()

            # Dictionnaire des champs à mettre à jour
            fields = {
                "theme": new_theme,
            }
            # Filtrer uniquement ceux qui ne sont pas None
            updates = {k: v for k, v in fields.items() if v is not None}

            if not updates:
                print("⚠️ Aucun champ à mettre à jour.")
                return

            # Construction dynamique de la requête SQL
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [id_theme]

            query = f"UPDATE themes SET {set_clause} WHERE id_theme = ?"
            c.execute(query, values)

            if c.rowcount == 0:
                raise ValueError(f"⚠️ Thème avec l'id {id_theme} introuvable.")

            conn.commit()
            print(f"✅ Thème avec l'id {id_theme} mise à jour avec : {new_theme}")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la mise à jour du thème : {e}")

        finally:
            conn.close()

    def delete_theme(self, id_theme):
        # Supprimer un thème de la table themes
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("DELETE FROM themes WHERE id_theme = ?", (id_theme,))

            if c.rowcount == 0:
                raise ValueError(f"⚠️ Thème avec l'id {id_theme} introuvable.")

            conn.commit()
            print(f"✅ Thème {id_theme} supprimé avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de ... : {e}")

        finally:
            conn.close()

    def get_all_themes(self):
        # Récupérer tous les thèmes
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM themes")
            results = c.fetchall()  # Liste de tuples (id_theme, theme)

            if not results:
                print("⚠️ Aucun thème trouvé.")
                return []
            else:
                print(f"✅ {len(results)} thème(s) récupéré(s) avec succès.")
                return results

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des thèmes : {e}")
            return None

        finally:
            conn.close()


class StatsManager(Database):
    # la classe StatsManager hérite de la classe Database
    # === Fonctions CRUD pour les Statistiques ===
    def update_stats(self, is_correct):
        #
        try:
            conn = self.connect()
            c = conn.cursor()
            # Récupération et formatage de la date du jour
            today = datetime.now().strftime("%Y-%m-%d")

            # Vérifier s’il y a déjà des stats pour aujourd’hui
            c.execute("SELECT * FROM stats WHERE date=?", (today,))
            result = (
                c.fetchone()
            )  # Liste de tuples (id, bonnes_reponses, mauvaises_reponses, date)

            if result is None:
                print(
                    "pas d'entrée pour la date du jour. Création d'une nouvelle entrée."
                )

                bonnes_reponses = 1 if is_correct else 0
                mauvaises_reponses = 0 if is_correct else 1

                c.execute(
                    """
                    INSERT INTO stats (bonnes_reponses, mauvaises_reponses, date)
                    VALUES (?, ?, ?)
                    """,
                    (bonnes_reponses, mauvaises_reponses, today),
                )
                conn.commit()
                print("✅ Statistiques du jour créées avec succès.")

            else:
                id = result[0]
                bonnes_reponses = result[1]
                mauvaises_reponses = result[2]

                if is_correct:
                    bonnes_reponses += 1
                else:
                    mauvaises_reponses += 1

                c.execute(
                    """ 
                        UPDATE stats SET bonnes_reponses=?, mauvaises_reponses=? WHERE id=?
                        """,
                    (bonnes_reponses, mauvaises_reponses, id),
                )

                conn.commit()
                print(f"✅ Statistiques avec l'id {id} mises à jour avec succès.")

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la mise à jour des statistiques : {e}")

        finally:
            conn.close()

    def update_card_probability(self, card_id, is_correct):
        #
        try:
            conn = self.connect()
            c = conn.cursor()

            # Récupération de la probabilité actuelle
            c.execute("SELECT probabilite FROM cards WHERE id=?", (card_id,))
            result = c.fetchone()

            if result is None:
                raise ValueError(f"⚠️ Carte avec l'id {card_id} introuvable.")

            proba = result[0]

            # Mise à jour selon la réponse
            if is_correct:
                proba = 0.9 * proba
            else:
                proba = 1.1 * proba

            # Encadrer la probabilité entre 0.1 et 1.0
            proba = max(0.1, min(proba, 1.0))

            # Mise à jour dans la base
            c.execute("UPDATE cards SET probabilite=? WHERE id=?", (proba, card_id))
            conn.commit()
            print(
                f"✅ Probabilité de la carte {card_id} mise à jour à {round(proba, 3)}."
            )

        except sqlite3.Error as e:
            print(f"❌ Erreur SQLite lors de la mise à jour de la probabilité : {e}")

        except ValueError as ve:
            print(ve)

        finally:
            conn.close()

    def get_stats(self):
        # Récupérer les statistiques
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM stats ORDER BY date ASC")
            results = (
                c.fetchall()
            )  # Liste de tuples (id, bonnes_reponses, mauvaises_reponses, date)

            if not results:
                print("⚠️ Aucune entrée trouvée.")
                return []
            else:
                print(f"✅ {len(results)} entrée(s) récupérée(s) avec succès.")
                return results

        except sqlite3.Error as e:
            print(f"❌ Erreur lors de la récupération des statistiques : {e}")
            return []

        finally:
            conn.close()


class FlashcardApp:
    def __init__(self):
        self.fm = FlashcardManager()
        self.tm = ThemeManager()
        self.sm = StatsManager()

    def get_cards_by_themes(self, theme_ids):
        """
        Récupère toutes les cartes correspondant à une liste d'identifiants de thème.
        """
        cards = []
        for theme_id in theme_ids:
            cards.extend(self.fm.get_cards_by_theme(theme_id))
        return cards

    def pick_card_weighted(self, cartes, k=1):
        """
        Tire k carte(s) pondérée(s) en fonction de la probabilité :
        plus la probabilité est haute, plus la carte a de chances d'être tirée.
        Si k=1, renvoie une carte unique. Sinon, une liste de cartes.
        """
        if not cartes:
            print("❌ Aucune carte disponible.")
            return None

        # Utiliser la probabilité comme poids (plus elle est haute, plus c’est tiré)
        poids = [c[3] for c in cartes]
        total = sum(poids)

        # Uniformisation des poids en cas de probabilités nulles (évite les erreurs avec random.choice)
        if total == 0:
            poids = [1.0] * len(cartes)  # fallback

        # Empêche de tirer plus de cartes qu'on en a
        k = min(k, len(cartes))

        tirage = random.choices(cartes, weights=poids, k=k)

        return tirage

    def ask_question(self, carte):
        print(f"\n Question : {carte[1]}")
        input("Appuyez sur Entrée pour voir la réponse...")
        print(f"✅ Réponse : {carte[2]}")
        rep = input("Aviez-vous bon ? (o/n) : ").strip().lower()
        return rep == "o"
