"""Vues des pages statiques."""
from xml.etree import ElementTree

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .loaders import (
    annees_archives,
    donnees_site,
    membres_valides,
    partenaires_valides,
    reglement_valide,
    resultats_valides,
    trails_valides,
)


def sitemap_xml(request):
    """Expose toutes les URL de pages réellement générées par le site."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    sitemap = ElementTree.Element(f"{{{namespace}}}urlset")
    chemins = [
        reverse("accueil"),
        reverse("a_propos"),
        reverse("trails"),
        reverse("partenaires"),
        reverse("membres"),
        reverse("contacts"),
        reverse("reglement"),
        reverse("resultats"),
        reverse("archives"),
        *(
            reverse("archive_annee", kwargs={"annee": annee})
            for annee in annees_archives()
        ),
    ]
    prefixe = f"{settings.SITE_BASE_PATH}/" if settings.SITE_BASE_PATH else ""
    for chemin in chemins:
        entree = ElementTree.SubElement(sitemap, f"{{{namespace}}}url")
        emplacement = ElementTree.SubElement(entree, f"{{{namespace}}}loc")
        emplacement.text = f"{settings.SITE_URL}/{prefixe}{chemin.lstrip('/')}"

    contenu = ElementTree.tostring(sitemap, encoding="utf-8", xml_declaration=True)
    return HttpResponse(contenu, content_type="application/xml; charset=utf-8")


def robots_txt(request):
    """Autorise l'exploration des pages et indique le plan de site."""
    prefixe = f"{settings.SITE_BASE_PATH}/" if settings.SITE_BASE_PATH else ""
    contenu = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {settings.SITE_URL}/{prefixe}sitemap.xml\n"
    )
    return HttpResponse(contenu, content_type="text/plain; charset=utf-8")


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
