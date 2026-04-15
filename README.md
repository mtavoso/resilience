
# Résilience

## Présentation du projet

Le projet Résilience a pour objectif de mettre en réseau des personnes et des communautés dans une logique d'entre-aide.

Le projet permettra librement à chacune et chacun de s'ajouter à la base de données et de créer des communautés. Les personnes peuvent par ailleurs déclarer faire partie de communautés et/ou avoir des liens avec d'autres personnes. Les communautés peuvent déclarer avoir des liens avec d'autres communautés. Les liens sont unidirectionnels et portent une description. Par exemple : Alice déclare un lien vers Bob, avec pour description Bob est mon voisin.

Toute personne membre d'une communauté peut administrer toutes les informations de cette communauté, il peut agir dans la base en tant que "la communauté".

Une personne peut s'opposer à la présence d'une autre personne dans la communauté. Si plus de la moitié des membres de la communauté est opposé à la présence d'une autre personne, alors celle-ci ne fait plus partie de la communauté.

La base contient des savoir-faire. Chacun peut ajouter un savoir-faire. Chaque personne ou communauté peut déclarer posséder un savoir-faire, avec un certain degré (de 1 à 5).

Chacun peut proposer des services (qui peuvent être en lien avec ces savoir-faire). Ces services sont proposés : sans-contre partie ; en contre partie d'un autre service identifié, ou non identifié (à discuter) ; commercialement (contre une somme en monnaie Ğ1 https://fr.wikipedia.org/wiki/%C4%9E1). Les personnes et communauté possèdent éventuellement des comptes en Ğ1, on stocke dans la base la liste de leurs clés publiques.

Les personnes et communauté peuvent s'échanger des messages. Un message est la propriété intégrale de son expéditeur. Il s'adresse à un expéditeur et peut faire référence à un autre message.

Les personnes peuvent se localiser avec des coordonnées géographiques sous un format du type 49.41957, 2.82377. On sera capable de produire un lien du type : https://www.openstreetmap.org/#map=17/49.41957/2.82243 (où 17 est ici le niveau de zoom).

**Fonctions spécialisées**
On proposera au moins les trois vues suivantes :

- Vue communauté : permet pour chaque personne d'avoir la liste des communautés auxquelles il déclare appartenir avec un booléen qui détermine si la personne est exclue ou non.

- Vue message : permet de visualiser chaque message en ajoutant l'identifiant du message d'origine lorsque le message s'inscrit dans un fil historique. Par exemple si C → B → A alors on veut voir la référence à A lorsqu'on affiche C.

- Vue proches : permet de visualiser les communautés et personnes proches de chaque personne et communauté (à une distance inférieure à 1km)

## Contribution personnelle
Implication majoritairement dans la création du modèle et dans son implémentation sur POSTGRE. Le sujet comprend le développement d'une application python, réalisée par Skander Saad.

## Membres du projet: 
- Matys Tavoso
- Gaspard Oliveira
- Ryad Meziane
- Skander Saad

