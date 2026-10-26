"""Tests des loaders et des routes générées."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import Client, SimpleTestCase, override_settings

from site_app import loaders
from site_app.templatetags.site_tags import nombre_en_lettres, with_base_path


class LoadersTests(SimpleTestCase):
    def test_charge_nombre_de_trails_exemple(self):
        self.assertEqual(loaders.nombre_trails(), 8)

    def test_valide_le_lien_du_site_de_course(self):
        self.assertEqual(loaders._url_externe("https://exemple.fr/course"), "https://exemple.fr/course")
        self.assertEqual(loaders._url_externe("javascript:alert(1)"), "")

    def test_na_est_omis_et_fichier_absent_est_signale(self):
        with tempfile.TemporaryDirectory() as dossier:
            racine = Path(dossier)
            (racine / "resultats.json").write_text(
                json.dumps([{"nom": "Course test", "hommes": "NA", "femmes": "", "mixte": "absent.pdf"}]),
                encoding="utf-8",
            )
            with patch.object(loaders, "CONTENT_DIR", racine):
                resultat = loaders.resultats_valides("resultats.json")
        self.assertEqual(resultat[0]["fichiers"], {"hommes": "", "femmes": "", "mixte": ""})

    def test_detecte_et_trie_les_annees(self):
        with tempfile.TemporaryDirectory() as dossier:
            archives = Path(dossier) / "archives"
            (archives / "2024").mkdir(parents=True)
            (archives / "2026").mkdir()
            (archives / "notes").mkdir()
            with patch.object(loaders, "CONTENT_DIR", Path(dossier)):
                annees = loaders.annees_archives()
        self.assertEqual(annees, ["2026", "2024"])

    def test_date_remise_est_formatee_en_francais(self):
        self.assertEqual(loaders.format_date_francaise("2026-12-12"), "samedi 12 décembre 2026")

    def test_remplace_les_variables_du_reglement(self):
        reglement = loaders.reglement_valide()
        self.assertIn("8 courses", reglement["introduction"])
        self.assertIn("samedi 12 décembre 2026", reglement["articles"][3]["texte"])

    def test_nombre_de_trails_est_ecrit_en_lettres(self):
        self.assertEqual(nombre_en_lettres(7), "sept")
        self.assertEqual(nombre_en_lettres(21), "vingt et un")
        self.assertEqual(nombre_en_lettres(71), "soixante et onze")

    @override_settings(SITE_BASE_PATH="challenge-trail")
    def test_ajoute_le_sous_chemin_aux_liens_django(self):
        self.assertEqual(with_base_path("/trails/"), "/challenge-trail/trails/")
        self.assertEqual(with_base_path("/challenge-trail/trails/"), "/challenge-trail/trails/")

    @override_settings(SITE_BASE_PATH="challenge-trail", STATIC_URL="/challenge-trail/static/")
    def test_rend_des_liens_de_navigation_et_statiques_avec_sous_chemin(self):
        reponse = Client().get("/")
        self.assertContains(reponse, 'href="/challenge-trail/trails/"')
        self.assertContains(reponse, 'href="/challenge-trail/static/css/site.css"')
