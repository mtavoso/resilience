Nous détaillerons ci-après les différents éléments qui apparaiteront dans notre modèle relational de données, ainsi que les contraintes à prendre en comptes.
Cette note de clarification se base sur les besoins exprimés dans l'énoncé.

---
###### Personne :
- prénom

=> fait partie de [Communauté]] ( * - * ) (il peut donc l'administrer)<br>
	en tant que Membre :<br>
		=>vote contre Membre ( 1 - 1 )<br>
=> a des liens avec [Personne]] ( * - * ) avec *description* et *unidirectionnel*<br>
=> possède [Savoir faire]] ( * - 1 ) avec *degré ∈ ⟦1; 5⟧* <br>
=> propose [Service]] ( * - * )<br>
=> possède [Compte_Ğ1]] ( * - * )<br>
=> expédie [Message|Message]] ( 1 - * )<br>
=> est à [Position]]  ( * - 1 )<br>
=> crée [Communauté]] ( 1 - * )<br>

---
###### Communauté :
- nom<br>
=> a des liens avec [Communauté]] ( * - * ) avec *description* et *unidirectionnel*<br>
=> possède [Savoir faire]] ( * - 1 ) avec *degré ∈ ⟦1; 5⟧* <br>

---
###### Savoir faire :
- intitulé (clé)<br>

---
###### Service :
- statut : {sans contrepartie ; en contrepartie d'un autre service ; commercial}<br>
- somme : Ğ1 (seulement si *statut : commercial*)<br>

=> en lien avec [Savoir faire]] ( * - * )<br>
=> en contrepartie de [Service]] ( 1 - 1 ) (il faut que tout les deux aient le *statut : en contrepartie d'un autre service*)<br>

---
###### Compte_Ğ1 :
- clés publiques : liste de clés publique (agrégation)<br>

---
###### Message :
- contenu<br>

=> fait référence à [Message]] ( * - 0..1 )<br>
=> est destiné à [Personne]] ( * - 1 ) XOR => est destiné à [Communauté]] ( * - 1 )<br>

---

###### Position :
- longitude<br>
- latitude<br>
- (longitude, latitude) (clé)<br>
