# Mettre le site en ligne gratuitement

Le projet génère des fichiers HTML/CSS/JS. Il n'a pas besoin d'un serveur Django en fonctionnement après la génération : l'hébergement statique est gratuit, rapide et simple à maintenir.

## Option 1 — GitHub Pages (recommandée)

### Première publication

1. Créez un dépôt sur GitHub, par exemple `challenge-trail`.
2. Envoyez-y tous les fichiers du projet et poussez la branche `main`.
3. Dans `content/site.json`, définissez la valeur `SITE_BASE_PATH` :
   - pour `https://mon-compte.github.io/challenge-trail/`, mettez `"SITE_BASE_PATH": "challenge-trail"`;
   - pour un dépôt GitHub Pages racine ou un nom de domaine personnalisé, laissez `"SITE_BASE_PATH": ""`.
4. Dans les réglages du dépôt, ouvrez **Settings → Pages**, puis sélectionnez **GitHub Actions** comme source.
5. Ouvrez l'onglet **Actions** et attendez la fin du workflow « Construire et publier le site ». Le lien du site apparaît dans **Settings → Pages**.

Les prochaines modifications envoyées sur `main` reconstruisent et publient automatiquement le site. Un build local équivalent se fait avec :

```sh
python -m pip install -r requirements.txt
python manage.py distill-local dist --force --collectstatic
```

Le dossier `dist/` est celui qui est effectivement publié.

## Option 2 — Render Static Site

1. Poussez le projet sur GitHub.
2. Dans Render, choisissez **New → Static Site**, puis connectez votre dépôt.
3. Réglez la branche sur `main`.
4. Utilisez comme **Build Command** :

   ```sh
   pip install -r requirements.txt && python manage.py distill-local dist --force --collectstatic
   ```

5. Utilisez `dist` comme **Publish Directory**.
6. Cliquez sur **Create Static Site**. Render fournit un sous-domaine `onrender.com` et relance le build à chaque mise à jour du dépôt.

Sur Render, laissez `SITE_BASE_PATH` vide : l'adresse du site n'utilise pas le préfixe d'un dépôt GitHub.

## Modifier puis republier

Modifiez les fichiers de contenu sous `content/` (JSON, images et PDF), puis poussez les changements vers GitHub. N'éditez pas les fichiers générés dans `dist/` : ils seront recréés à chaque publication. Les instructions pour mettre à jour les courses, partenaires, membres et archives sont détaillées dans le [README](./README.md).
