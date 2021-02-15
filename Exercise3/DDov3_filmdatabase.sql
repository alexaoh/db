create table regissør(
RegissørID INT primary key,
Navn VARCHAR(30));

create table sjanger(
SjangerID INT primary key,
Navn VARCHAR(50), 
Beskrivelse VARCHAR(100)
);

create table skuespiller(
SkuespillerID INT primary key,
Navn VARCHAR(30), 
Fødselsår INT
);

create table film(
FilmID INT primary key,
Tittel VARCHAR(30), 
Produksjonsår INT, 
RegissørID INT,
CONSTRAINT FK
FOREIGN KEY (RegissørID) references regissør(RegissørID)
);

create table skuespillerifilm(
FilmID INT, 
SkuespillerID INT, 
Rolle VARCHAR(30), 
PRIMARY KEY (FilmID, SkuespillerID),
FOREIGN KEY (FilmId) REFERENCES film(FilmId)
        ON DELETE CASCADE  ON UPDATE CASCADE
);

create table sjangerforfilm(
SjangerID INT, 
FilmID INT,
CONSTRAINT PK PRIMARY KEY (FilmID, SjangerID),
CONSTRAINT FKFIlm FOREIGN KEY (FilmID) references film(FilmID)
		ON DELETE CASCADE  ON UPDATE CASCADE, 
CONSTRAINT FKSjanger FOREIGN KEY (SjangerID) references sjanger(SjangerID)
);
