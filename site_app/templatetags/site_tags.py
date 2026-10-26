"""Filtres d'affichage réutilisables."""
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def initiales(texte):
    mots = [mot for mot in str(texte).split() if mot]
    return "".join(mot[0] for mot in mots[:2]).upper() or "?"


@register.filter
def nombre_en_lettres(nombre):
    try:
        valeur = int(nombre)
    except (TypeError, ValueError):
        return str(nombre)
    unites = (
        "zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit",
        "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
    )
    speciaux = {17: "dix-sept", 18: "dix-huit", 19: "dix-neuf"}
    dizaines = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 60: "soixante"}
    if valeur < 0 or valeur > 99:
        return str(nombre)
    if valeur < 17:
        return unites[valeur]
    if valeur in speciaux:
        return speciaux[valeur]
    if valeur in dizaines:
        return dizaines[valeur]
    if valeur < 70:
        dizaine, unite = divmod(valeur, 10)
        mot = dizaines[dizaine * 10]
        return f"{mot} et un" if unite == 1 else f"{mot}-{unites[unite]}"
    if valeur < 80:
        reste = valeur - 60
        return "soixante-dix" if reste == 10 else (
            f"soixante et onze" if reste == 11 else f"soixante-{speciaux.get(reste, unites[reste])}"
        )
    if valeur < 90:
        reste = valeur - 80
        return "quatre-vingts" if reste == 0 else (
            f"quatre-vingt-{unites[reste]}" if reste < 10 else f"quatre-vingt-{speciaux[reste]}"
        )
    reste = valeur - 80
    return f"quatre-vingt-{speciaux.get(reste, unites[reste])}"


@register.filter
def with_base_path(url):
    """Ajoute le préfixe GitHub Pages aux URL produites par le tag url."""
    prefixe = getattr(settings, "SITE_BASE_PATH", "")
    if prefixe and str(url).startswith("/") and not str(url).startswith(f"/{prefixe}/"):
        return f"/{prefixe}{url}"
    return url
