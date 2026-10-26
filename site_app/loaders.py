"""Lecture et validation souple des fichiers de contenu."""
import json
import re
from datetime import date
from pathlib import Path

from django.conf import settings

CONTENT_DIR = settings.CONTENT_DIR


def lire_json(chemin, valeur_secours):
    """Lit un JSON et signale les erreurs sans interrompre le build."""
    try:
        with (CONTENT_DIR / chemin).open(encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        if not isinstance(donnees, type(valeur_secours)):
            raise ValueError("format de données inattendu")
        return donnees
    except (OSError, json.JSONDecodeError, ValueError) as erreur:
        print(f"Avertissement : {chemin} ignoré ({erreur}).")
        return valeur_secours


def donnees_site():
    return lire_json("site.json", {})


def nombre_trails():
    return len(trails())


def trails():
    return [entree for entree in lire_json("Ntrails/trails.json", []) if isinstance(entree, dict)]


def _fichier_contenu(chemin):
    """Valide qu'un chemin de JSON reste dans content/ et pointe vers un fichier."""
    if not isinstance(chemin, str) or not chemin.strip():
        return None
    racine = CONTENT_DIR.resolve()
    cible = (CONTENT_DIR / chemin).resolve()
    if not cible.is_relative_to(racine) or not cible.is_file():
        print(f"Avertissement : fichier de contenu introuvable ou invalide : {chemin}")
        return None
    return chemin.replace("\\", "/")


def chemin_media(chemin):
    """Retourne le chemin statique d'un média disponible, ou une chaîne vide."""
    return _fichier_contenu(chemin) or ""


def trails_valides():
    valides = []
    for trail in trails():
        champs = ("nom", "description", "date", "lieu")
        if any(not trail.get(champ) for champ in champs):
            print(f"Avertissement : trail incomplet ignoré : {trail.get('nom', '(sans nom)')}")
            continue
        affiche = _fichier_contenu(trail.get("affiche", ""))
        valides.append({**trail, "affiche_url": affiche or ""})
    return valides


def partenaires_valides():
    partenaires = lire_json("partenaires/partenaires.json", [])
    resultat = []
    for partenaire in partenaires:
        if not isinstance(partenaire, dict) or not partenaire.get("texte"):
            print("Avertissement : partenaire incomplet ignoré.")
            continue
        resultat.append({
            **partenaire,
            "logo_url": _fichier_contenu(partenaire.get("logo", "")) or "",
        })
    return resultat


def membres_valides():
    membres = lire_json("membres/membres.json", [])
    resultat = []
    for membre in membres:
        if not isinstance(membre, dict) or not membre.get("role") or not membre.get("course"):
            print("Avertissement : membre incomplet ignoré.")
            continue
        resultat.append({
            **membre,
            "photo_url": _fichier_contenu(membre.get("photo", "")) or "",
        })
    return resultat


def resultats_valides(chemin_json):
    """Ne conserve que les résultats dont le document existe."""
    resultat = []
    for entree in lire_json(chemin_json, []):
        if not isinstance(entree, dict) or not entree.get("nom"):
            print(f"Avertissement : résultat incomplet ignoré dans {chemin_json}.")
            continue
        fichiers = {}
        for genre in ("hommes", "femmes", "mixte"):
            valeur = entree.get(genre, "")
            fichiers[genre] = (
                _fichier_contenu(valeur)
                if isinstance(valeur, str) and valeur.strip() and valeur.upper() != "NA"
                else ""
            ) or ""
        resultat.append({**entree, "fichiers": fichiers})
    return resultat


def annees_archives():
    dossier = CONTENT_DIR / "archives"
    if not dossier.is_dir():
        return []
    annees = [
        entree.name
        for entree in dossier.iterdir()
        if entree.is_dir() and re.fullmatch(r"\d{4}", entree.name)
    ]
    return sorted(annees, reverse=True)


def format_date_francaise(iso):
    """Formate une date ISO en français sans dépendre de la locale du système."""
    try:
        valeur = date.fromisoformat(iso)
    except (TypeError, ValueError):
        print(f"Avertissement : date de remise invalide : {iso}")
        return iso or ""
    jours = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
    mois = (
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre",
    )
    return f"{jours[valeur.weekday()]} {valeur.day} {mois[valeur.month - 1]} {valeur.year}"


def reglement_valide():
    contenu = lire_json("reglement.json", {})
    variables = {
        "date_remise": format_date_francaise(donnees_site().get("date_remise_prix", "")),
        "nb_courses": str(nombre_trails()),
    }

    def remplacer(texte):
        if not isinstance(texte, str):
            return ""
        for nom, valeur in variables.items():
            texte = texte.replace("{" + nom + "}", valeur)
        return texte

    introduction = contenu.get("introduction", "")
    if not isinstance(introduction, str) or not introduction:
        print("Avertissement : introduction du règlement manquante.")
    articles = contenu.get("articles", [])
    if not isinstance(articles, list):
        print("Avertissement : articles du règlement invalides.")
        articles = []
    articles_valides = []
    for article in articles:
        if not isinstance(article, dict) or not isinstance(article.get("texte"), str):
            print("Avertissement : article incomplet ignoré dans le règlement.")
            continue
        articles_valides.append({
            "titre": article.get("titre", "") if isinstance(article.get("titre", ""), str) else "",
            "texte": remplacer(article["texte"]),
        })
    return {
        "introduction": remplacer(introduction),
        "articles": articles_valides,
    }
