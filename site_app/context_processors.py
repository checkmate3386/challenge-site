"""Valeurs partagées par les gabarits."""
from django.conf import settings

from .loaders import donnees_site, nombre_trails, annees_archives


def site_context(request):
    return {
        "site": donnees_site(),
        "site_url": settings.SITE_URL,
        "nombre_trails": nombre_trails(),
        "annees_archives": annees_archives(),
    }
