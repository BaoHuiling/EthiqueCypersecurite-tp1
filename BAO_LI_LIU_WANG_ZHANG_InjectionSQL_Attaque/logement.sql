-- sqlite3 bibli.db
-- .read logement.sql

-------
-- commandes de destruction des tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Adresse;
DROP TABLE IF EXISTS Ville;
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS Coordonnees;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS TypeCap;
DROP TABLE IF EXISTS LogeCham;
DROP TABLE IF EXISTS ChamCap;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;

-------
-- commandes de creation des tables

CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL, pwd TEXT NOT NULL);

-- Table identifiant un logement par son id, l'adresse, son numero de telephone, une adresse IP et la date d'insertion
CREATE TABLE Logement (id INTEGER PRIMARY KEY AUTOINCREMENT, idAd INTEGER NOT NULL, Nbphone TEXT NOT NULL, Aip TEXT NOT NULL, TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (idAd) REFERENCES Adresse(id));
-- Table identifiant l'adresse d'un logement: id unique, numero, voie et le nom du voie, code postal
CREATE TABLE Adresse (id  INTEGER PRIMARY KEY AUTOINCREMENT, Numero INTEGER NOT NULL, Voie TEXT NOT NULL, Nom_voie TEXT NOT NULL, Code INTEGER NOT NULL, FOREIGN KEY (Code) REFERENCES Ville(Code));
-- Table identifiant une ville: code postal, nom de la ville
CREATE TABLE Ville (Code INTEGER PRIMARY KEY, Nom TEXT NOT NULL);

-- Table identifiant une chambre: id unique, nom de la chambre, sa coordonnee dans le logement correspondant
CREATE TABLE Chambre (id INTEGER PRIMARY KEY AUTOINCREMENT, Nom_Cham TEXT NOT NULL, idCor INTEGER NOT NULL, FOREIGN KEY (idCor) REFERENCES Coordonnees(id));
-- Table des coordonnees des chambres: matrice 3D donc 3 champs D1,D2,D3
CREATE TABLE Coordonnees (id INTEGER PRIMARY KEY AUTOINCREMENT,	 D1 INTEGER NOT NULL, D2 INTEGER NOT NULL, D3 INTEGER NOT NULL);

-- Table identifiant un capteur: id unique, le type du capteur, reference commercial, id du chambre ou il se situe, port de communication, date d'insertion
CREATE TABLE Capteur (id INTEGER PRIMARY KEY AUTOINCREMENT, idTyCap INTEGER NOT NULL, RfComm TEXT NOT NULL, Port INTEGER NOT NULL, TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(idTyCap) REFERENCES TypeCap(id));
-- Table identifiant le type du capteur: id unique, le type(température,électricité etc), unite de mesure, plage de precision
CREATE TABLE TypeCap (id INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT NOT NULL, Unite TEXT NOT NULL, Precision TEXT NOT NULL);

-------
-- insertion de données
INSERT INTO Users (user_name, pwd) VALUES ("Huiling", "password");
INSERT INTO Users (user_name, pwd) VALUES ("Tom", "password");
INSERT INTO Users (user_name, pwd) VALUES ("Lily", "password");

-- Ajouter un logement avec 4 pieces
INSERT INTO Ville (Code, Nom) VALUES (94200, "Ivry Sur Seine");
INSERT INTO Adresse (Numero, Voie, Nom_voie, Code) VALUES (89, "Avenue", "Maurice Thorez", 94200);
INSERT INTO Logement (idAd, Nbphone, Aip) VALUES(1, "0638395725", "127.0.0.1");
INSERT INTO Coordonnees (D1, D2, D3) VALUES (1,1,1),(1,2,1),(2,1,1),(2,2,1);
INSERT INTO Chambre (Nom_Cham, idCor) VALUES
	("living room", 1), 
	("dinning room", 2), 
	("bathroom", 3),
	("bedroom", 4);

-- Ajouter 4 type de capteur
INSERT INTO TypeCap (Type, Unite, Precision) VALUES
	("temperature", "°C", "0.1"),
	("humidity", "%RH", "0.1"),
	("light", "Lux", "1"),
	("ultrasonic", "cm", "1");

-- Ajouter 2 capteur 
INSERT INTO Capteur (idTyCap, RfComm, Port) VALUES
	(1, "6010344", 80),
	(2, "6010344", 81);

-------
-- Associations
-- Table represente quel logement possede quelle(s) chambre(s): id du logement, id du Chambre
CREATE TABLE LogeCham (idLoge INTEGER NOT NULL, idCham INTEGER NOT NULL, FOREIGN KEY (idLoge) REFERENCES Logement(id), FOREIGN KEY (idCham) REFERENCES Chambre(id), PRIMARY KEY (idLoge,idCham));
-- Table represente quelle Chambre possede quel(s) capteur(s): id de la chambre, id du capteur
CREATE TABLE ChamCap (idCham INTEGER NOT NULL, idCap INTEGER NOT NULL, FOREIGN KEY (idCham) REFERENCES Chambre(id), FOREIGN KEY (idCap) REFERENCES Capteur(id), PRIMARY KEY (idCham,idCap));

-------
-- Actions
-- Table decrit une mesure: id du capteur utilise, valeur de la mesure, moment de la mesure
CREATE TABLE Mesure (id INTEGER PRIMARY KEY AUTOINCREMENT, idCap INTEGER NOT NULL, Valeur REAL NOT NULL, TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (idCap) REFERENCES Capteur(id));
-- Table identifiant la facture d'un logement: id unique, logement associe, type de la facture, valeur consomme, montant de la facture et la date d'insertion
CREATE TABLE Facture (id INTEGER PRIMARY KEY AUTOINCREMENT, idLoge INTEGER NOT NULL, Type TEXT NOT NULL, Valcsm REAL NOT NULL, Montant REAL NOT NULL, TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (idLoge) REFERENCES Logement(id));

-------
-- insertion de données

-- Associer les 4 pieces a ce logement:
INSERT INTO LogeCham (idLoge, idCham) VALUES 
	(1, 1), 
	(1, 2), 
	(1, 3),
	(1, 4);
-- Associer les 2 capteurs aux differentes chambre: temperature dans le living room et humidity dans le bedroom
INSERT INTO ChamCap (idCham, idCap) VALUES 
	(1, 1), 
	(4, 2);

-- 2 mesure par capteur:
INSERT INTO Mesure (idCap, Valeur) VALUES
	(1, 28.9),
	(1, 29.1),
	(2, 35.6),
	(2, 34.4);

-- 4 facture:
INSERT INTO Facture (idLoge, Type, Valcsm, Montant) VALUES
	(1, "electricite", 		10.2, 32),
	(1, "electricite", 		6.9, 21),
	(1, "electricite", 		8.3, 25),
	(1, "electricite", 		4.9, 15),
	(1, "electricite", 		7.2, 21.9),
	(1, "eau", 		   		18.9, 12.9),
	(1, "eau", 		   		24.5, 15.7),
	(1, "eau", 		   		21.0, 13.4),
	(1, "eau", 		   		28.7, 20.9),
	(1, "eau", 		   		11.4, 9.9),
	(1, "chauffage",   		1,   20.5),
	(1, "chauffage",   		1,   18.0),
	(1, "chauffage",   		1,   24.9),
	(1, "chauffage",   		1,   29.2),
	(1, "chauffage",   		1,   28.9),
	(1, "dechet",   		1,   3.5),
	(1, "dechet",   		1,   5.7),
	(1, "dechet",   		1,   2.4),
	(1, "dechet",   		1,   9.3),
	(1, "dechet",   		1,   2.3),
	(1, "service internet", 1,   13),
	(1, "service internet", 1,   10),
	(1, "service internet", 1,   9),
	(1, "service internet", 1,   8),
	(1, "repair wall", 1,   25);





