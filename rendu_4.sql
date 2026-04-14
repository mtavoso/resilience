
--Retournent respectivement le nombre de service gratuits, commerciaux et echanges

SELECT COUNT(*) FROM Service_gratuit;
SELECT COUNT(*) FROM Service_commercial;
SELECT COUNT(*) FROM Service_echange;


--Retourne le nom prenom de toutes les personnes qui savent coudre
SELECT (p.nom, p.prenom) FROM Personne p JOIN Maitrise_personnelle mp ON  mp.personne=p.id WHERE mp.savoir='coudre' ;

 



--Retourne les personnes et leur localisation
SELECT prenom, nom, position_long, position_lat
FROM Personne;

--Retourne le nom d’une communauté avec le nom, prénom de son créateur.
SELECT Communaute.nom, Personne.prenom, Personne.nom
FROM Communaute
JOIN Personne ON Communaute.createur = Personne.id;

--Retourne les services proposes par des personnes
SELECT Personne.prenom, Personne.nom, Service.nom
FROM Proposition_service
JOIN Personne ON Proposition_service.personne = Personne.id
JOIN Service ON Proposition_service.service = Service.service_id;

--Retourne les messages envoyes par une communaute
SELECT Message.message, Communaute.nom, Personne.prenom, Personne.nom
FROM Message
JOIN Communaute ON Message.expediteur_commu = Communaute.id
JOIN Personne ON Message.receveur_personne = Personne.id;

--Retourne les types de liens existants entre communautes
SELECT c1.nom, c2.nom, Lien_intercommunautaire.description
FROM Lien_intercommunautaire
JOIN Communaute c1 ON communaute1 = c1.id
JOIN Communaute c2 ON communaute2 = c2.id;


--Retourne le nombre de membres de chaque communaute
SELECT Communaute.nom, COUNT(Membre.id)
FROM Communaute
LEFT JOIN Membre ON Communaute.id = Membre.communaute
GROUP BY Communaute.nom;

--Retourne le total du solde disponible pour chaque compte
SELECT Compte_G1.id, SUM(Cle_publique.solde)
FROM Compte_G1
JOIN Cle_publique ON Cle_publique.compte = Compte_G1.id
GROUP BY Compte_G1.id;



--Retourne le nombre de competences dont une personne dispose
SELECT Personne.id, COUNT(Maitrise_personnelle.savoir)
FROM Personne
LEFT JOIN Maitrise_personnelle ON Personne.id = Maitrise_personnelle.personne
GROUP BY Personne.id;

--Retourne la maitrise moyenne des competences dont une personne dispose
SELECT Personne.id, AVG(Maitrise_personnelle.rang)
FROM Personne
JOIN Maitrise_personnelle ON Personne.id = Maitrise_personnelle.personne
GROUP BY Personne.id;


--Retourne la liste des personnes capables d’effectuer un service (lie a un savoir faire)
SELECT Personne.prenom, Personne.nom, Service.nom
FROM Service
JOIN Necessite_savoir ON Service.service_id = Necessite_savoir.service
JOIN Maitrise_personnelle ON Necessite_savoir.savoir = Maitrise_personnelle.savoir
JOIN Personne ON Maitrise_personnelle.personne = Personne.id;

--Retourne les services pour lesquels la personne 1 est competente
SELECT Service.nom
FROM Service
JOIN Necessite_savoir ON Service.service_id = Necessite_savoir.service
JOIN Maitrise_personnelle ON Maitrise_personnelle.savoir = Necessite_savoir.savoir
WHERE Maitrise_personnelle.personne = 1;

--Retourne les contenus des messages ainsi que le nom et prenom de leur expediteur
SELECT Message.message, Personne.prenom, Personne.nom
FROM Message
JOIN Personne ON Message.expediteur_personne = Personne.id;


--Retourne le nom, prenom des personnes ainsi que leurs savoirs et maitrise de ces derniers
SELECT Personne.prenom, Personne.nom, Maitrise_personnelle.savoir, Maitrise_personnelle.rang
FROM Personne
JOIN Maitrise_personnelle ON Personne.id = Maitrise_personnelle.personne;



