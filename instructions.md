
## Contexte

Je suis développeur Python (je ne connais pas bien le front). Je veux refaire le site du
"Challenge Trail Sud Toulousain" (https://www.challengetrailsudtoulousain.com/) avec Django.
Le code doit rester simple, commenté en français, facile à modifier par moi.

## Contraintes techniques (IMPORTANT)

1. Hébergement gratuit depuis GitHub = site STATIQUE (GitHub Pages ou Cloudflare Pages / Netlify).
   Django ne tourne pas sur GitHub Pages. Donc :
   - Utilise Django + **django-distill** pour générer le site en HTML statique dans `dist/`
     (commande : `python manage.py distill-local dist --force`).
   - Toutes les pages dynamiques (nombre de trails, archives par année…) sont calculées
     **au moment du build** en lisant les JSON.
   - Ajoute un workflow GitHub Actions `.github/workflows/deploy.yml` qui : installe les
     dépendances, lance le build, déploie `dist/` sur GitHub Pages.
2. Gère le sous-chemin de GitHub Pages (`/nom-du-repo/`) : variable `SITE_BASE_PATH` dans
   `config/site.json`, et usage de `{% static %}` / `{% url %}` partout (jamais de liens en dur).
3. Pas de base de données, pas de JavaScript lourd, pas de framework front : HTML + CSS
   (variables CSS, flexbox/grid) + un peu de JS vanilla uniquement pour le menu mobile.
4. Dépendances minimales dans `requirements.txt` (Django, django-distill, Pillow si besoin).
5. Design moderne mais classique, **mobile-first** : menu hamburger, images responsives,
   boutons/zones cliquables ≥ 44 px, police lisible, bon contraste.
6. Tous les chemins de fichiers dans les JSON sont relatifs à la racine du dossier `content/`.
7. Les erreurs de données (champ manquant, fichier introuvable) ne doivent pas casser le build :
   afficher un avertissement dans la console et ignorer l'entrée.

## Structure de projet attendue

```
challenge_site/
├── manage.py
├── requirements.txt
├── README.md                  (comment ajouter une course, un partenaire, une année d'archive, déployer)
├── .github/workflows/deploy.yml
├── config/                    (projet Django : settings, urls)
├── site_app/                  (app Django : views, loaders, templates, static)
│   ├── loaders.py             (toute la lecture des JSON/dossiers, fonctions courtes et commentées)
│   ├── templates/
│   └── static/css, static/js
└── content/                   (SEUL dossier que je modifie au quotidien)
    ├── site.json              (titre, base path, date de la soirée de remise des prix, emails…)
    ├── reglement.json         (liste d'articles en texte avec variables {date_remise} et {nb_courses})
    ├── logo/logo.png          
    ├── illustrations/apropos.jpg
    ├── contact/contact.jpeg
    ├── Ntrails/trails.json + affiches/
    ├── partenaires/partenaires.json + logos/
    ├── membres/membres.json + photos/
    ├── resultats/resultats.json + fichiers de résultats
    └── archives/<année>/resultats.json + fichiers
```

## Pages et règles de contenu

### Menu (ordre)
Accueil · À propos · {N} Trails · Partenaires · Membres · Contacts · Règlement · Résultats · Archives

- `{N}` = nombre d'objets dans `content/Ntrails/trails.json` (ex. "7 Trails", "8 Trails").
- Le menu Archives n'apparaît que s'il existe au moins un sous-dossier année ; il affiche un sous-menu
  (ou une liste de boutons sur la page) avec une entrée par année, triées de la plus récente à la plus ancienne.

### Accueil
Logo du challenge + texte exact :
"7 courses de 9 à 12 KMS — 7 lieux différents, vallonnés accessibles à tous ! Bienvenue sur le site
du challenge Trail Sud Toulousain."
Le "7" doit venir du nombre de trails (variable), pas écrit en dur.

### À propos
Image `illustrations/apropos.jpg` + texte :
"À PROPOS DU CHALLENGE — Découvrez notre challenge trail du Sud Toulousain, né de la passion de
fervent(e)s amateurs de course en plein air ! Sept associations sportives et clubs d'athlétisme se
sont unis pour offrir une expérience unique. Avec des distances de 9 à 12 kms, ce challenge est
accessible à tous, des débutants aux coureurs expérimentés. Rejoignez-nous pour partager la joie de
la course et vivre des moments inoubliables en pleine nature !"
Puis encart "REJOIGNEZ NOTRE CHALLENGE" :
"Pour participer au challenge, n'hésitez pas à contacter chaque responsable de trails, ou
directement Christophe ou Michel. Ils seront ravis de vous aider et de vous donner toutes les
informations nécessaires pour que vous puissiez vous engager dans cette aventure."
Le texte "Sept" doit aussi être calculé à partir du nombre de trails (en lettres).

### {N} Trails
`content/Ntrails/trails.json` : liste d'objets, un par trail, dans l'ordre du fichier.
Champs : `affiche` (chemin jpg/jpeg/gif/png/pdf), `nom`, `description`, `date`, `lieu`.
- Image : afficher en carte ; si PDF : bouton "Voir l'affiche (PDF)" qui ouvre le PDF dans un nouvel onglet.
- Fournis un `trails.json` d'exemple avec 7 entrées fictives + un fichier `trails.schema.md`
  décrivant chaque champ.

### Partenaires
`content/partenaires/partenaires.json` : liste d'objets `{ "logo": "...", "texte": "..." }`.
Grille responsive de cartes (logo + texte court). Fournis un JSON d'exemple.

### Membres
`content/membres/membres.json` : liste d'objets
`{ "photo", "role", "course", "email", "telephone" }`.
Cartes avec photo ronde, rôle, course, lien `mailto:` et `tel:` cliquables.
Si la photo est absente ou vide : avatar par défaut. Fournis un JSON d'exemple.

### Contacts
Image `contact/contact.jpeg` + texte :
"INFOS par TRAIL : Contactez le responsable du Trail souhaité. Et pour vous aider :
Christophe Coustouzy — christophe.coustouzy@live.fr — Tel : 06.46.11.34.46
Michel Blattes — michel.blattes@gmail.com — Tel : 06.29.52.86.62"
Ces coordonnées doivent venir de `content/site.json` (liste `contacts`), avec liens `mailto:` / `tel:`.

### Règlement du challenge
Source : `content/reglement.json` (introduction + liste d'articles, texte simple modifiable).
Variables remplacées au build :
- `{date_remise}` ← champ `date_remise_prix` de `site.json` (formatée en français, ex.
  "vendredi 12 décembre 2025" ; stocker en ISO `2025-12-12`).
- `{nb_courses}` ← nombre de trails dans `trails.json`.
Texte de départ (à mettre dans le JSON) :
- Introduction : "Règlement du challenge. {nb_courses} courses sont membres du challenge, 1 seul format de distance par course."
- Art. 1 : "Le challenge prendra en compte 5 des meilleures courses sur {nb_courses}."
- Art. 2 : "Il récompensera à égalité masculin, féminin, les 3 premiers et premières au scratch, mais aussi le premier et première de chaque catégorie de CA à M9."
- Art. 3 : "Le et la plus assidus seront aussi récompensés (prise en compte des {nb_courses} courses). Le club le plus représenté tout au long du challenge aura sa récompense."
- Art. 4 : "Une soirée de remise des récompenses sera organisée le {date_remise}, avec repas et animation. Les lauréats, organisateurs et partenaires seront invités."
- Art. 5 : "La gestion du challenge sera réalisée par la société CHRONO START. Un classement intermédiaire à l'issue de chaque course sera diffusé sur le site internet du challenge."
- Art. 6 : "La participation de chaque personne à ce challenge implique l'acceptation totale du règlement, ainsi que l'acceptation du règlement interne de chaque course à laquelle elle participera."
(Corrige la formulation "chaque catégorie catégorie" de l'original.)

### Résultats courses et challenge
`content/resultats/resultats.json` : liste d'objets (ordre du fichier respecté) :
```json
{ "nom": "Trail de ...", "hommes": "resultats/xxx_hommes.pdf", "femmes": "NA", "mixte": "resultats/xxx_mixte.pdf" }
```
- Pour chaque course : le nom + jusqu'à 3 boutons (icône + libellé "Classement hommes / femmes / mixte").
- Un champ égal à "NA" (ou vide / absent) → le bouton n'est pas affiché.
- Un lien vers un fichier inexistant → bouton non affiché + avertissement au build.
- Les fichiers s'ouvrent dans un nouvel onglet.

### Archives
Dossier `content/archives/<année>/` contenant un `resultats.json` au **même format** que la page
Résultats + les fichiers de résultats.
- Au build, détecte automatiquement tous les sous-dossiers dont le nom est une année (4 chiffres).
- Génère une page `archives/<année>/` par dossier + une page d'index `archives/` listant les années.
- Aucune modification de code nécessaire pour ajouter une année.
- Réutilise le même template/composant que la page Résultats.

## Qualité attendue
- Un seul template `base.html` (header, menu, footer) + un template par page ; composants réutilisables
  via `{% include %}`.
- CSS dans un seul fichier avec variables (`--couleur-principale`…) pour changer facilement la charte.
- Balises `<title>`, meta description, `alt` sur toutes les images, `lang="fr"`, favicon.
- Images en `loading="lazy"`.
- README en français avec : installation, lancement local (`python manage.py runserver`), build
  statique, déploiement GitHub Pages, comment ajouter trail / partenaire / membre / année d'archive.
- Tests simples (pytest ou `manage.py test`) : chargement des JSON, gestion de "NA", détection des années.

## Méthode et étapes à faire une par une
1. "Crée l'arborescence, requirements.txt, settings, base.html, CSS mobile-first et le menu dynamique
   (nombre de trails + années d'archives). Pas encore les autres pages."
2. "Ajoute loaders.py et les pages Accueil, À propos, Contacts."
3. "Ajoute les pages Trails, Partenaires, Membres avec leurs JSON d'exemple."
4. "Ajoute Règlement (variables), Résultats et Archives dynamiques."
5. "Ajoute django-distill, le build statique et le workflow GitHub Actions + README."
6. "Relis tout, lance les tests, corrige les warnings."

A la fin fais un moi un fichier explicatif pour m'expliquer comment le mettre en ligne sur un site gratuit comme render
