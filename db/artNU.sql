create database if not exists ArtNU;
use ArtNU;
create table if not exists Clients (
    clientID    INT PRIMARY KEY,
    firstName   TEXT,
    lastName    TEXT,
    email       VARCHAR(50) NOT NULL UNIQUE
);

create table if not exists Orders (
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

    constraint fk_orders_client foreign key (clientID)
        references Clients(clientID)
        on update cascade
        on delete restrict,
    constraint fk_orders_type foreign key (typeID)
        references CommissionTypes(typeID)

);

create table if not exists Artists (
  artistID INT PRIMARY KEY,
  email TEXT NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  bio TEXT,
  link1 TEXT,
  link2 TEXT,
  link3 TEXT,
  link4 TEXT,
  termsOfService TEXT NOT NULL
);

create table if not exists CommissionTypes (
    typeID INT PRIMARY KEY,
    name TEXT,
    description TEXT,
    minPrice DOUBLE,
    maxPrice DOUBLE,
    licenseID INT NOT NULL,
    imageID INT NOT NULL,
    artistID INT NOT NULL,
    constraint fk_comm_license foreign key (licenseID)
        references Licenses(licenseID)
        on update cascade
        on delete restrict,
    constraint fk_comm_artist foreign key (artistID)
        references Artists(artistID)
        on update cascade
        on delete restrict
);

create table if not exists Tags (
    tagID INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

create table if not exists Licenses (
    licenseID INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

create table if not exists DigitalImages (
    imageID INT PRIMARY KEY,
    description TEXT,
    isExplicit BOOLEAN NOT NULL,
    typeID INT NOT NULL,
    constraint fk_image_comm foreign key (typeID)
        references CommissionTypes(typeID)
        on update cascade
        on delete restrict
);

create table if not exists OrderDetails (
    streetAddr VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(20) NOT NULL,
    country VARCHAR(20) NOT NULL,
    zipCode VARCHAR(10) NOT NULL,
    orderID INT NOT NULL,
    primary key (streetAddr, city, state, country, zipCode),
    constraint fk_orderID_details foreign key (orderID)
        references Orders(orderID)
);

create table if not exists Comm_Tag (
    typeID INT NOT NULL,
    tagID INT NOT NULL,
    primary key (typeID, tagID),
    constraint fk_ctag_tag foreign key (tagID)
        references Tags(tagID)
        on update cascade
        on delete cascade,
    constraint fk_ctag_comm foreign key (typeID)
        references CommissionTypes(typeID)
        on update cascade
        on delete cascade
);

create table if not exists Deny_List (
    artistID INT NOT NULL,
    tagID INT NOT NULL,
    primary key (artistID, tagID),
    constraint fk_deny_tag foreign key (tagID)
        references Tags(tagID)
        on update cascade
        on delete cascade,
    constraint fk_deny_artist foreign key (artistID)
        references Artists(artistID)
        on update cascade
        on delete cascade
);