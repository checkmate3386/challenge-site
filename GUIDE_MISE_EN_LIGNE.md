# Mettre le site en ligne gratuitement

Le projet génère des fichiers HTML/CSS/JS. Il n'a pas besoin d'un serveur Django en fonctionnement après la génération : l'hébergement statique est gratuit, rapide et simple à maintenir.

## Option 1 — GitHub Pages (recommandée)

### Première publication

1. Créez un dépôt sur GitHub, par exemple `challenge-trail`.
2. Envoyez-y tous les fichiers du projet et poussez la branche `main`.
3. Dans `content/site.json`, définissez `SITE_URL` et `SITE_BASE_PATH` selon l'adresse publiée :
   - pour `https://mon-compte.github.io/challenge-trail/`, mettez `"SITE_URL": "https://mon-compte.github.io"` et `"SITE_BASE_PATH": "challenge-trail"`;
   - pour un dépôt GitHub Pages racine, utilisez `"SITE_URL": "https://mon-compte.github.io"` et `"SITE_BASE_PATH": ""`;
   - pour un nom de domaine personnalisé, utilisez son adresse canonique dans `SITE_URL` et laissez `"SITE_BASE_PATH": ""`.
4. Dans les réglages du dépôt, ouvrez **Settings → Pages**, puis sélectionnez **GitHub Actions** comme source.
5. Ouvrez l'onglet **Actions** et attendez la fin du workflow « Construire et publier le site ». Le lien du site apparaît dans **Settings → Pages**.

Les prochaines modifications envoyées sur `main` reconstruisent et publient automatiquement le site. Un build local équivalent se fait avec :

```sh
python -m pip install -r requirements.txt
python manage.py distill-local dist --force --collectstatic
```

Le dossier `dist/` est celui qui est effectivement publié.

Le build publie aussi `robots.txt` et `sitemap.xml`. Le plan de site recense les pages et les éditions archivées ; `SITE_URL` dans `content/site.json` doit correspondre au domaine canonique réellement utilisé. Après publication, vérifiez `https://votre-domaine/sitemap.xml`, puis déclarez cette adresse dans Google Search Console (et dans Bing Webmaster Tools si vous l'utilisez). L'envoi du plan de site facilite la découverte des pages, mais ne garantit pas leur indexation : publiez du contenu utile et distinct, reliez les pages entre elles et vérifiez les éventuelles erreurs d'exploration dans ces outils.

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

Sur Render, laissez `SITE_BASE_PATH` vide et définissez `SITE_URL` sur l'adresse publique du site (son sous-domaine Render ou votre domaine personnalisé).

## Modifier puis republier

Modifiez les fichiers de contenu sous `content/` (JSON, images et PDF), puis poussez les changements vers GitHub. N'éditez pas les fichiers générés dans `dist/` : ils seront recréés à chaque publication. Les instructions pour mettre à jour les courses, partenaires, membres et archives sont détaillées dans le [README](./README.md).
