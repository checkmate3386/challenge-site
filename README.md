# Challenge Trail Sud Toulousain

Site vitrine en Django, pré-rendu en HTML avec django-distill. Aucun serveur Django ni base de données n'est nécessaire pour le site publié.

## Installation et aperçu local

1. Installez Python 3.10 ou supérieur.
2. Dans le dossier du projet, installez les dépendances : `python -m pip install -r requirements.txt`.
3. En développement local, lancez le site : `python manage.py runserver`.
4. Ouvrez <http://127.0.0.1:8000/>.

## Génération statique

```sh
python manage.py distill-local dist --force --collectstatic
```

Le dossier `dist/` contient le site prêt à publier. Les pages sont calculées à partir des fichiers JSON au moment de la génération. Les messages d'avertissement signalent les entrées incomplètes ou les médias manquants sans interrompre le build.

## Publication gratuite sur GitHub Pages

1. Créez un dépôt GitHub et poussez le projet sur sa branche `main`.
2. Pour un dépôt de projet (URL `https://utilisateur.github.io/nom-du-repo/`), renseignez `"SITE_BASE_PATH": "nom-du-repo"` dans `content/site.json`. Pour un domaine racine, laissez la valeur vide.
3. Dans **Settings → Pages**, sélectionnez **GitHub Actions** comme source de publication.
4. Chaque push sur `main` lance `.github/workflows/deploy.yml` et publie le contenu de `dist/`.

## Mise en ligne sur Render

GitHub Pages héberge directement le site statique et est donc la solution la plus simple. Pour Render, créez un service **Static Site**, connectez le dépôt, utilisez `pip install -r requirements.txt && python manage.py distill-local dist --force --collectstatic` comme commande de build et `dist` comme répertoire de publication. Render relance cette génération à chaque push. Laissez `SITE_BASE_PATH` vide sur Render (le domaine n'a pas de sous-chemin de dépôt).

## Modifier le contenu (dossier `content/`)

Tous les chemins de médias des JSON sont relatifs à `content/`. Par exemple, `Ntrails/affiches/trail.jpg` désigne `content/Ntrails/affiches/trail.jpg`.

- **Ajouter/modifier un trail** : éditez `content/Ntrails/trails.json`. Conservez les champs `nom`, `description`, `date`, `lieu`; `affiche` peut être vide ou pointer vers une image/PDF. L'ordre JSON est l'ordre d'affichage. Le format est décrit dans `content/Ntrails/trails.schema.md`.
- **Ajouter un partenaire** : ajoutez un objet `{ "logo": "partenaires/logos/nom.png", "texte": "Nom du partenaire" }` à `content/partenaires/partenaires.json`. Le logo est facultatif.
- **Ajouter un membre** : ajoutez un objet avec `photo`, `role`, `course`, `email` et `telephone` dans `content/membres/membres.json`. La photo est facultative ; courriel et téléphone deviennent des liens directs.
- **Ajouter une année d'archive** : créez `content/archives/2025/resultats.json` et placez-y les fichiers référencés. Toute sous-répertoire dont le nom est composé de quatre chiffres est détecté et ajouté automatiquement.
- **Contacts, date et sous-chemin** : modifiez `content/site.json`. La date de remise doit être au format ISO `AAAA-MM-JJ`. Les coordonnées des contacts sont listées dans `contacts`.
- **Résultats** : éditez `content/resultats/resultats.json` (ou le JSON d'archive). Les valeurs `NA`, vides ou absentes masquent le bouton associé. Les liens vers des fichiers absents sont avertis et masqués.
- **Règlement** : modifiez `content/reglement.json`. Les variables `{nb_courses}` et `{date_remise}` sont remplacées lors du build.

Les JSON d'exemple sont fictifs et servent de modèle de mise en page ; remplacez-les par les informations vérifiées avant publication.

## Tests

Lancez les tests avec `python manage.py test`.
