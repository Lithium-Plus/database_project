INSERT INTO airport(city,name)
VALUES ('Hong Kong','HKG'),('Beijing','PEK'),('Georgia',"ALT"),('California',"LAX"),('Tokyo',"HND"),('Dubai',"DXB"),('Illinois',"ORD"),('London',"LHR"),('Paris',"CDG"),('Dallas',"DFW"),("Guangzhou","CAN");

INSERT INTO airline(name)
VALUES ('ANA');
INSERT INTO airline(name)
VALUES ('Spring');
INSERT INTO airline(name)
VALUES ('Emirates');
INSERT INTO airline(name)
VALUES ('Delta');

INSERT INTO airplane(airline,ID,number_of_seats) 
VALUES ('ANA','1',5),
    ('ANA','2',10),
    ('ANA','3',50),
    ('ANA','4',80),
    ('ANA','5',280),
    ('ANA','6',380),
    ('Emirates','1',5),
    ('Emirates','2',10),
    ('Emirates','3',50),
    ('Emirates','4',80),
    ('Emirates','5',280),
    ('Emirates','6',380),
    ('Spring','1',5),
    ('Spring','2',10),
    ('Spring','3',50),
    ('Spring','4',80),
    ('Spring','5',280),
    ('Spring','6',380),
    ('Delta','1',5),
    ('Delta','2',10),
    ('Delta','3',50),
    ('Delta','4',80),
    ('Delta','5',280),
    ('Delta','6',380),
    ('China Eastern','1',5),
    ('China Eastern','2',10),
    ('China Eastern','3',50),
    ('China Eastern','4',80),
    ('China Eastern','5',280)
    ('China Eastern','6',380);

INSERT INTO staff(airline,date_of_birth,firstname,lastname,`password`,email)
VALUES('ANA','1989-02-05','Xi','Gong',md5('staff2'),'staff2@ana.com’);