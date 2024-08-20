# Bâton Bagarre

## Description du Projet

**Bâton Bagarre** est un jeu d'action en 2D développé en Python à l'aide de la bibliothèque PyGame. Le jeu met en scène un stickman dont l'objectif est de protéger un feu de divers ennemis qui tentent de l'éteindre. Le feu s'éteint progressivement, réduisant la visibilité du joueur. Le stickman peut raviver le feu en intéragissant avec, mais cela prend du temps et doit également combattre les ennemis pour les empêcher de détruire le feu.

### Objectif

Le but principal du jeu est de survivre le plus longtemps possible en gardant le feu allumé. Le jeu se termine lorsque le feu est complètement éteint, et la visibilité est réduite à zéro. Le joueur doit donc jongler entre combattre les ennemis et réparer le feu pour maintenir une zone de lumière suffisante.

## Installation and run

Pour pouvoir lancer le jeu il vous faut python version supérieur 3.12

Telechargez l'archive la plus récente

Decompressez l'archive dans le repertoire de votre choix

Dans un terminal, naviguez jusqu'à l'emplacement de l'archive décompresée

Executez la commande suivante

`python run.py`

Cela va initialiser un nouvel environnement python, installer les dependance puis executez le jeu


## Requirements Fonctionnels

1. **Gestion du Feu :**
    - Le feu doit réduire de taille au fil du temps.
    - Le stickman peut raviver le feu en intéragissant avec, à condition qu'il ne soit pas complètement éteint.
    - Si le feu est complètement éteint, il n'est pas possible de le rallumer et le jeu se termine.

2. **Ennemis :**
    - Les ennemis doivent apparaître et se diriger vers le feu.
    - Les ennemis doivent pouvoir être éliminés par le stickman.
    - Le nombre et la puissance des ennemis doit augmenter en difficulté au fil du temps.
    - Si un ennemi attaque le feu, l'intensité du feu diminuera par acoups très rapidement.

3. **Stickman :**
    - Le stickman doit être contrôlable par le joueur.
    - Le stickman doit pouvoir se déplacer et attaquer les ennemis.
    - Le stickman doit pouvoir réparer le feu en intéragissant avec.
    - Le stickman est invincible.

4. **Effet de Lumière :**
    - La zone de lumière visible doit diminuer à mesure que le feu s’éteint.
    - Les bords de l'écran doivent devenir progressivement plus sombres en fonction de la taille du feu.

5. **Interface Utilisateur :**
    - Afficher un compteur de temps ou un score indiquant combien de temps le joueur a survécu.
    - Indiquer visuellement le temps de vie restant du feu.

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

🔥 **Protégez le feu, sauvez l'avenir !** 🔥

Plongez dans une bataille palpitante avec notre nouveau jeu de stickman où votre objectif est de défendre un précieux feu contre des vagues incessantes d'ennemis. Chaque attaque diminue non seulement la vie du feu, mais aussi la visibilité de l'écran, rendant chaque seconde cruciale!

✨ **Êtes-vous prêt à relever le défi ?** ✨

Rejoignez-nous maintenant et testez vos compétences dans cette aventure intense ! Découvrez plus sur notre landing page et préparez-vous à sauver le feu avant qu'il ne soit trop tard.

👉 [Découvrez le jeu ici !](https://raynobrak.github.io/baton-bagarre-game)
