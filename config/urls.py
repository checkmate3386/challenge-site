"""Routes des pages exportées par django-distill."""
from django_distill import distill_path

from site_app import views
from site_app.loaders import annees_archives


def annees_a_exporter():
    return ({"annee": annee} for annee in annees_archives())


urlpatterns = [
    distill_path("", views.accueil, name="accueil"),
    distill_path("a-propos/", views.a_propos, name="a_propos"),
    distill_path("trails/", views.trails, name="trails"),
    distill_path("partenaires/", views.partenaires, name="partenaires"),
    distill_path("membres/", views.membres, name="membres"),
    distill_path("contacts/", views.contacts, name="contacts"),
    distill_path("reglement/", views.reglement, name="reglement"),
    distill_path("resultats/", views.resultats, name="resultats"),
    distill_path("archives/", views.archives, name="archives"),
    distill_path(
        "archives/<str:annee>/",
        views.archive_annee,
        name="archive_annee",
        distill_func=annees_a_exporter,
    ),
]
