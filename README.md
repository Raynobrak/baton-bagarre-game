# Bâton Bagarre

## Description du Projet

**Bâton Bagarre** est un jeu d'action en 2D développé en Python à l'aide de la bibliothèque PyGame. Le jeu met en scène un stickman dont l'objectif est de protéger un feu de divers ennemis qui tentent de l'éteindre. Le feu s'éteint progressivement, réduisant la zone de lumière visible à l'écran. Le stickman peut réparer le feu, mais cela prend du temps, et il doit également combattre les ennemis pour les empêcher de détruire le feu.

### Objectif

Le but principal du jeu est de survivre le plus longtemps possible en gardant le feu allumé. À mesure que le feu s'éteint, les bords de l'écran deviennent de plus en plus sombres jusqu'à ce que la visibilité soit réduite à néant. Le jeu se termine lorsque le feu est complètement éteint, et la visibilité est réduite à zéro. Le joueur doit donc jongler entre combattre les ennemis et réparer le feu pour maintenir une zone de lumière suffisante.

## Requirements Fonctionnels

1. **Gestion du Feu :**
    - Le feu doit réduire de taille au fil du temps.
    - Le stickman peut réparer le feu, augmentant ainsi la taille de la lumière.
    - La vitesse de réparation doit être lente, nécessitant un certain temps pour être efficace.
    - Le jeu se termine lorsque le feu est complètement éteint et que la visibilité est nulle.

2. **Ennemis :**
    - Les ennemis doivent apparaître et tenter d'éteindre le feu.
    - Les ennemis doivent être détruits par le stickman pour empêcher l'extinction du feu.
    - Les ennemis doivent apparaître à des intervalles réguliers et augmenter en nombre et en difficulté au fil du temps.
    - Les ennemis doivent avoir des comportements variés (ex. : se déplacer vers le feu, attaquer le feu).

3. **Stickman :**
    - Le stickman doit être contrôlable par le joueur.
    - Le stickman doit pouvoir se déplacer et attaquer les ennemis.
    - Le stickman doit pouvoir réparer le feu en restant immobile.
    - Le stickman est invincible.

4. **Effet de Lumière :**
    - La zone de lumière visible doit diminuer à mesure que le feu s’éteint.
    - Les bords de l'écran doivent devenir progressivement plus sombres en fonction de la taille du feu.

5. **Interface Utilisateur :**
    - Afficher un compteur de temps ou un score indiquant combien de temps le joueur a survécu.
    - Indiquer visuellement la taille du feu ou l’état de la réparation.

## Requirements Non-Fonctionnels

1. **Performance :**
    - Le jeu doit fonctionner de manière fluide sur des machines ayant des spécifications minimales pour PyGame.
    - Les animations doivent être fluides et ne pas entraîner de ralentissements notables.

2. **Ergonomie :**
    - Les contrôles du stickman doivent être intuitifs et réactifs.
    - L'interface utilisateur doit être claire et facile à comprendre pour le joueur.

3. **Portabilité :**
    - Le jeu doit être exécutable sur les principales plateformes (Windows, macOS, Linux) sans modifications importantes.

4. **Documentation :**
    - La documentation du code et du jeu doit être complète et bien structurée pour faciliter les futurs développements et la maintenance.

## Mockups
<img src="Mockup/Mockup_Part1.jpg">
<img src="Mockup/Mockup_Part2.jpg">

## Landing page
Lien pour accéder à la landing page : [lien](https://raynobrak.github.io/baton-bagarre-game)
