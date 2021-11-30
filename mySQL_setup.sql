


SET GLOBAL local_infile=1;

mysql --local-infile=1 -u root -p;

CREATE DATABASE TrainsDB; 
USE TrainsDB;

DROP TABLE IF EXISTS TrainsDB;

CREATE TABLE IF NOT EXISTS TrainsDB
       (
           train_id TINYINT AUTO_INCREMENT, 
           from_dest VARCHAR(255) NOT NULL,
           to_dest VARCHAR(255) NOT NULL, 
           date_of_dep VARCHAR(10) NOT NULL,
           time_of_dep VARCHAR(8) NOT NULL,
           ticket_id VARCHAR(8) NOT NULL,
           addon_data VARCHAR(20) NOT NULL,
           CONSTRAINT train_PK PRIMARY KEY (train_id)
        );


LOAD DATA LOCAL INFILE 'TrainsDB.csv' 
INTO TABLE TrainsDB
FIELDS TERMINATED BY ',';


DROP TABLE IF EXISTS UserDB;

CREATE TABLE IF NOT EXISTS UserDB
       (
           train_id TINYINT AUTO_INCREMENT, 
           from_dest VARCHAR(255) NOT NULL,
           to_dest VARCHAR(255) NOT NULL, 
           date_of_dep VARCHAR(10) NOT NULL,
           time_of_dep VARCHAR(8) NOT NULL,
           ticket_id VARCHAR(8) NOT NULL,
           addon_data VARCHAR(20) NOT NULL,
           CONSTRAINT train_PK PRIMARY KEY (train_id)
        );



