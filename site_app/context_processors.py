"""Valeurs partagées par les gabarits."""
from .loaders import donnees_site, nombre_trails, annees_archives


def site_context(request):
    return {
        "site": donnees_site(),
        "nombre_trails": nombre_trails(),
        "annees_archives": annees_archives(),
    }
