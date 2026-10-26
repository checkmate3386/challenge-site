# Format de `trails.json`

Le fichier contient un tableau JSON. Chaque objet représente une course, dans l'ordre où elle doit apparaître.

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `affiche` | chaîne | non | Chemin relatif à `content/` vers une image (JPG, JPEG, PNG, AVIF, GIF) ou un PDF. Une chaîne vide masque l'affiche. |
| `nom` | chaîne | oui | Nom public de la course. |
| `description` | chaîne | oui | Courte présentation de la course. |
| `date` | chaîne | oui | Date à afficher, par exemple `15 mars`. |
| `lieu` | chaîne | oui | Commune de départ. |
| `site_web` | chaîne | non | URL HTTP ou HTTPS du site de la course. Laisser vide si la course n'a pas de site connu. |

Exemple : `{"affiche":"Ntrails/affiches/course.avif","nom":"Trail des Coteaux","description":"Une boucle nature.","date":"15 mars","lieu":"Saint-Lys","site_web":"https://exemple.fr"}`.

Les affiches image sont ajustées au cadre sans être recadrées. Cliquer dessus ouvre le fichier image en grand dans un nouvel onglet.
