"""Vues des pages statiques."""
from django.shortcuts import render

from .loaders import (
    annees_archives,
    donnees_site,
    membres_valides,
    partenaires_valides,
    reglement_valide,
    resultats_valides,
    trails_valides,
)


def accueil(request):
    return render(request, "pages/accueil.html")


def a_propos(request):
    return render(request, "pages/a_propos.html")


def trails(request):
    return render(request, "pages/trails.html", {"trails": trails_valides()})


def partenaires(request):
    return render(request, "pages/partenaires.html", {"partenaires": partenaires_valides()})


def membres(request):
    return render(request, "pages/membres.html", {"membres": membres_valides()})


def contacts(request):
    return render(request, "pages/contacts.html")


def reglement(request):
    return render(request, "pages/reglement.html", {"reglement": reglement_valide()})


def resultats(request):
    return render(
        request,
        "pages/resultats.html",
        {"titre_page": "Résultats", "courses": resultats_valides("resultats/resultats.json")},
    )


def archives(request):
    return render(request, "pages/archives.html", {"annees": annees_archives()})


def archive_annee(request, annee):
    if annee not in annees_archives():
        return render(request, "pages/resultats.html", {"titre_page": "Archives", "courses": []})
    return render(
        request,
        "pages/resultats.html",
        {
            "titre_page": f"Résultats {annee}",
            "courses": resultats_valides(f"archives/{annee}/resultats.json"),
        },
    )
