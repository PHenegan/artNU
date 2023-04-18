-- Restart the database from scratch
DROP DATABASE IF EXISTS ArtNU;

-- Make the new ArtNU database
CREATE DATABASE IF NOT EXISTS ArtNU;
USE ArtNU;
CREATE TABLE IF NOT EXISTS Clients (
    clientID    INT PRIMARY KEY,
    firstName   TEXT,
    lastName    TEXT,
    email       VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Artists (
  artistID          INT PRIMARY KEY,
  email             TEXT NOT NULL,
  firstName         TEXT NOT NULL,
  lastName          TEXT NOT NULL,
  bio               TEXT,
  link1             TEXT,
  link2             TEXT,
  link3             TEXT,
  link4             TEXT,
  termsOfService    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Tags (
    tagID   INT PRIMARY KEY,
    name    VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Licenses (
    licenseID   INT PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE if NOT EXISTS CommissionTypes (
    typeID      INT PRIMARY KEY,
    name        TEXT,
    description TEXT,
    minPrice    DOUBLE,
    maxPrice    DOUBLE,
    licenseID   INT NOT NULL,
    artistID    INT NOT NULL,
    CONSTRAINT fk_comm_license FOREIGN KEY (licenseID)
        REFERENCES Licenses(licenseID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_comm_artist FOREIGN KEY (artistID)
        REFERENCES Artists(artistID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Orders (
    orderID             INT PRIMARY KEY,
    workStatus          VARCHAR(15),
    startDate           DATE,
    finishDate          DATE,
    description         TEXT,
    quote               DOUBLE,
    paymentStatus       VARCHAR(15),
    orderFileLocation   TEXT,
    typeID              INT NOT NULL,
    clientID            INT NOT NULL,

    CONSTRAINT fk_orders_client FOREIGN KEY (clientID)
        REFERENCES Clients(clientID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_orders_type FOREIGN KEY (typeID)
        REFERENCES CommissionTypes(typeID)

);

CREATE TABLE IF NOT EXISTS DigitalImages (
    imageID     INT PRIMARY KEY,
    description TEXT,
    isExplicit  BOOLEAN NOT NULL,
    typeID      INT NOT NULL,
    CONSTRAINT fk_image_comm FOREIGN KEY (typeID)
        REFERENCES CommissionTypes(typeID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ImageFiles (
    imageID                 INT NOT NULL,
    location VARCHAR(50)    NOT NULL,
    title                   TEXT,
    PRIMARY KEY (imageID, location),
    CONSTRAINT fk_image_file FOREIGN KEY (imageID)
        REFERENCES DigitalImages(imageID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS OrderDetails (
    streetAddr  VARCHAR(50) NOT NULL,
    city        VARCHAR(50) NOT NULL,
    state       VARCHAR(20) NOT NULL,
    country     VARCHAR(20) NOT NULL,
    zipCode     VARCHAR(10) NOT NULL,
    orderID     INT NOT NULL,
    PRIMARY KEY (streetAddr, city, state, country, zipCode),
    CONSTRAINT fk_orderID_details FOREIGN KEY (orderID)
        REFERENCES Orders(orderID)
);

CREATE TABLE IF NOT EXISTS Comm_Tag (
    typeID  INT NOT NULL,
    tagID   INT NOT NULL,
    PRIMARY KEY (typeID, tagID),
    CONSTRAINT fk_ctag_tag FOREIGN KEY (tagID)
        REFERENCES Tags(tagID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_ctag_comm FOREIGN KEY (typeID)
        REFERENCES CommissionTypes(typeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Deny_List (
    artistID    INT NOT NULL,
    tagID       INT NOT NULL,
    PRIMARY KEY (artistID, tagID),
    CONSTRAINT fk_deny_tag FOREIGN KEY (tagID)
        REFERENCES Tags(tagID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_deny_artist FOREIGN KEY (artistID)
        REFERENCES Artists(artistID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);