DROP TABLE IF EXISTS Proposition_service CASCADE;
DROP TABLE IF EXISTS Service_echange CASCADE;
DROP TABLE IF EXISTS Service_commercial CASCADE;
DROP TABLE IF EXISTS Service_gratuit CASCADE;
DROP TABLE IF EXISTS Necessite_savoir CASCADE;
DROP TABLE IF EXISTS Service CASCADE;
DROP TABLE IF EXISTS Message CASCADE;
DROP TABLE IF EXISTS Compte_G1 CASCADE;
DROP TABLE IF EXISTS Maitrise_personnelle CASCADE;
DROP TABLE IF EXISTS Maitrise_communautaire CASCADE;
DROP TABLE IF EXISTS Lien_interpersonnel CASCADE;
DROP TABLE IF EXISTS Lien_intercommunautaire CASCADE;
DROP TABLE IF EXISTS Membre CASCADE;
DROP TABLE IF EXISTS Communaute CASCADE;
DROP TABLE IF EXISTS Savoir_faire CASCADE;
*/

CREATE TABLE IF NOT EXISTS Personne (
  id SERIAL PRIMARY KEY,
  prenom VARCHAR(255),
  nom VARCHAR(255),
  mot_de_passe VARCHAR(255),
  localisation JSON
);

CREATE TABLE IF NOT EXISTS Savoir_faire (
  intitule VARCHAR PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Lien_interpersonnel (
  personne1 INT REFERENCES Personne(id),
  personne2 INT REFERENCES Personne(id),
  description TEXT,
  PRIMARY KEY(personne1, personne2),
  CHECK(personne1 <> personne2)
);

CREATE TABLE IF NOT EXISTS Communaute (
  nom VARCHAR PRIMARY KEY,
  createur INTEGER NOT NULL REFERENCES Personne(id),
  localisation JSON ;
);

CREATE TABLE IF NOT EXISTS Membre (
  id SERIAL PRIMARY KEY,
  personne INTEGER NOT NULL REFERENCES Personne(id),
  communaute VARCHAR NOT NULL REFERENCES Communaute(nom),
  vote_contre INTEGER REFERENCES Membre(id)
);

CREATE TABLE IF NOT EXISTS Lien_intercommunautaire (
  communaute1 VARCHAR REFERENCES Communaute(nom),
  communaute2 VARCHAR REFERENCES Communaute(nom),
  description TEXT,
  PRIMARY KEY (communaute1, communaute2),
  CHECK (communaute1 <> communaute2)
);

CREATE TABLE IF NOT EXISTS Maitrise_communautaire (
  communaute VARCHAR REFERENCES Communaute(nom),
  savoir_faire VARCHAR REFERENCES Savoir_faire(intitule),
  rang INT CHECK (rang BETWEEN 1 AND 5),
  PRIMARY KEY (communaute, savoir_faire)
);

CREATE TABLE IF NOT EXISTS Maitrise_personnelle (
  personne INT REFERENCES Personne(id),
  savoir VARCHAR REFERENCES Savoir_faire(intitule),
  rang INT CHECK (rang BETWEEN 1 AND 5),
  PRIMARY KEY(personne, savoir)
);

CREATE TABLE IF NOT EXISTS Compte_G1 (
  id SERIAL PRIMARY KEY,
  proprietaire_personne INTEGER REFERENCES Personne(id),
  proprietaire_commu VARCHAR REFERENCES Communaute(nom),
  cle_publique JSON,
  CHECK (
    (proprietaire_personne IS NOT NULL AND proprietaire_commu IS NULL)
    OR
    (proprietaire_personne IS NULL AND proprietaire_commu IS NOT NULL)
  )
);


CREATE TABLE IF NOT EXISTS Message (
  id SERIAL PRIMARY KEY,
  message VARCHAR NOT NULL,
  expediteur_personne INTEGER REFERENCES Personne(id),
  expediteur_commu VARCHAR REFERENCES Communaute(nom),
  receveur_personne INTEGER REFERENCES Personne(id),
  receveur_commu VARCHAR REFERENCES Communaute(nom),
  message_precedent INTEGER REFERENCES Message(id),
  CHECK (
    (expediteur_personne IS NOT NULL AND expediteur_commu IS NULL)
    OR
    (expediteur_personne IS NULL AND expediteur_commu IS NOT NULL)
  ),
  CHECK (
    (receveur_personne IS NOT NULL AND receveur_commu IS NULL)
    OR
    (receveur_personne IS NULL AND receveur_commu IS NOT NULL)
  )
);

CREATE TABLE IF NOT EXISTS Service (
  service_id SERIAL PRIMARY KEY,
  nom VARCHAR
);

CREATE TABLE IF NOT EXISTS Service_gratuit (
  service INTEGER PRIMARY KEY REFERENCES Service(service_id)
);

CREATE TABLE IF NOT EXISTS Service_commercial (
  service INTEGER PRIMARY KEY REFERENCES Service(service_id),
  somme INT
);

CREATE TABLE IF NOT EXISTS Service_echange (
  service INTEGER PRIMARY KEY REFERENCES Service(service_id),
  contrepartie INTEGER REFERENCES Service(service_id)
);

CREATE TABLE IF NOT EXISTS Necessite_savoir (
  service INT REFERENCES Service(service_id),
  savoir VARCHAR REFERENCES Savoir_faire(intitule),
  PRIMARY KEY(service, savoir)
);

CREATE TABLE IF NOT EXISTS Proposition_service (
  personne INT REFERENCES Personne(id),
  service INT REFERENCES Service(service_id),
  PRIMARY KEY(personne, service)
);
