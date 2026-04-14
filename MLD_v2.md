
###### Personne :
>Personne(#id: int, prénom:text, nom: text, position=>Localisation,)

>Lien_interpersonnel(#personne1=>Personne,#personne2=>Personne, description: text)

>Maîtrise_personnelle(#personne=>Personne,#savoir_faire=>Savoir_faire, rang : ⟦1; 5⟧)

###### Membre :
>Membre(#id : int,personne=>Personne,communauté=>Communauté ,vote_contre=>Membre) personne NOT NULL, communauté NOT NULL


###### Communauté
>Communauté(#id: int, nom:text, position=>Localisation, createur=>Personne) avec createur NOT NULL

>Lien_intercommunautaire(#communauté1=>Communauté,#communauté2=>Communauté, description: text) avec communaute1<>communaute2

>Maîtrise_communautaire(#communauté=>Communauté,#savoir_faire=>Savoir_faire, rang : ⟦1; 5⟧)

  
###### Ğ1 :
>Compte(#id: int, propriétaire1=> Personne, propriétaire2=> Communauté) avec propriétaire1 NOT NULL XOR  propriétaire2 NOT NULL

>Clé_publique(#id: int, solde: float, compte=>Compte) avec solde>=0


###### Message :
>Message(#id: int, message: text, expediteur_personne => Personne, expediteur_commu => Communauté, receveur_personne => Personne, receveur_commu => Communauté, ref=>Message) avec (Expéditeur1 NOT NULL XOR Expéditeur2 NOT NULL) AND (Receveur1 NOT NULL XOR Receveur2 NOT NULL)


###### Localisation :
>Localisation(#longitude:float,#latitude:float)


###### Service :
//Héritage par référence, afin de lier simplement à Savoir_faire : 

>Service(#service_id : int, nom : text)

>Service_gratuit(#service=>Service)

>Service_commercial(#service=>Service, somme : int)

>Service_échangé(#service=>Service, contrepartie=>Service_échangé) //contrepartie peut être nulle en cas de contrepartie indéterminée.

>Proposition_service(#personne=>Personne,#service=>Service)
  
###### Savoir_faire :

>Savoir_faire(#intitulé : text)

>Necessite_savoir(#savoir=>Savoir_faire, #service=>Service)

