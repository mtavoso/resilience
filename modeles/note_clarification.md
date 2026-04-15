Nous détaillerons ci-après les différents éléments qui apparaîtront dans notre modèle relationnel de données, ainsi que les contraintes à prendre en compte.  
Cette note de clarification se base sur les besoins exprimés dans l'énoncé.

---

###### Personne :
- prénom

=> fait partie de [Communauté] ( * - * ) (il peut donc l'administrer)  
en tant que Membre :  
=> vote contre Membre ( 1 - 1 )  
=> a des liens avec [Personne] ( * - * ) avec *description* et *unidirectionnel*  
=> possède [Savoir faire] ( * - 1 ) avec *degré ∈ ⟦1; 5⟧*  
=> propose [Service] ( * - * )  
=> possède [Compte_Ğ1] ( * - * )  
=> expédie [Message] ( 1 - * )  
=> est à [Position] ( * - 1 )  
=> crée [Communauté] ( 1 - * )

---

###### Communauté :
- nom

=> a des liens avec [Communauté] ( * - * ) avec *description* et *unidirectionnel*  
=> possède [Savoir faire] ( * - 1 ) avec *degré ∈ ⟦1; 5⟧*

---

###### Savoir faire :
- intitulé (clé)

---

###### Service :
- statut : {sans contrepartie ; en contrepartie d'un autre service ; commercial}  
- somme : Ğ1 (seulement si *statut : commercial*)

=> en lien avec [Savoir faire] ( * - * )  
=> en contrepartie de [Service] ( 1 - 1 ) (il faut que tous les deux aient le *statut : en contrepartie d'un autre service*)

---

###### Compte_Ğ1 :
- clés publiques : liste de clés publiques (agrégation)

---

###### Message :
- contenu

=> fait référence à [Message] ( * - 0..1 )  
=> est destiné à [Personne] ( * - 1 ) XOR => est destiné à [Communauté] ( * - 1 )

---

###### Position :
- longitude  
- latitude  
- (longitude, latitude) (clé)
