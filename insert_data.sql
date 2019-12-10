INSERT INTO airline(name)
VALUES ('Air China');

INSERT INTO airport(city,name)
VALUES ('NYC','JFK'),
       ('Boston','BOS'),
       ('Beijing','BEI'),
       ('Shenzhen','SHEN'),
       ('Hong Kong','HKA'),
       ('Los Angles','LAX'),
       ('San Francisco','SFO'),
	 ('Shanghai','PVG');

INSERT INTO customer(building_number,city,date_of_birth,email,name,passport_country,passport_expiration,passport_number,`password`,phone_number,state,street)
VALUES('1555','Pudong','1999-12-19','testcustomer@nyu.edu','Test Customer 1','China','2025-12-24','54321',md5('1234'),'123-4321-4321','Shanghai','Century Avenue'),
      ('1555','Pudong','1999-11-19','user1@nyu.edu','User 1','China','2025-12-25','54322',md5('1234'),'123-4322-4322','Shanghai','Century Avenue'),
      ('1702','Pudong','1999-10-19','user2@nyu.edu','User 2','China','2025-10-24','54323',md5('1234'),'123-4323-4323','Shanghai','Century Avenue'),
      ('1890','Pudong','1999-09-19','user3@nyu.edu','User 3','China','2025-09-24','54324',md5('1234'),'123-4324-4324','Shanghai','Century Avenue');

INSERT INTO airplane(airline,ID,number_of_seats) 
VALUES ('Air China','1',4),
       ('Air China','2',4),
	   ('Air China','3',50);

-- the user name of staff is email in our database
INSERT INTO staff(airline,date_of_birth,firstname,lastname,`password`,email)
VALUES('Air China','1978-05-25','Roe','Zhang',md5('abcd'),'admin');

INSERT INTO flight(airline,arrival_airport,arrival_date_time,base_price,departure_airport,departure_date_time,flight_number,plane_ID,`status`)
VALUES('Air China','LAX','2019-11-12 16:50:25',300,'SFO','2019-11-12 13:25:25','102','3','on-time'),
	('Air China','BEI','2019-12-06 16:50:25',300,'PVG','2019-12-12 13:25:25','104','3','on-time'),
      ('Air China','LAX','2019-10-12 16:50:25',350,'SFO','2019-10-12 13:25:25','106','3','delayed'),
      ('Air China','LAX','2020-01-12 16:50:25',400,'SFO','2020-01-12 13:25:25','206','2','on-time'),
      ('Air China','SFO','2020-02-12 16:50:25',300,'LAX','2020-02-12 13:25:25','207','2','on-time'),
      ('Air China','BOS','2019-08-12 16:50:25',300,'JFK','2019-08-12 13:25:25','134','3','delayed'),
      ('Air China','SFO','2020-01-01 16:50:25',3000,'PVG','2020-01-01 13:25:25','296','1','on-time'),
      ('Air China','BEI','2019-11-28 13:50:25',500,'PVG','2019-11-28 10:25:25','715','1','delayed'),
      ('Air China','BEI','2019-02-12 16:50:25',300,'SHEN','2019-02-12 13:25:25','839','3','on-time');

INSERT INTO agent(booking_agent_id,email,`password`)
VALUES('1','ctrip@agent.com',md5('abcd1234')),
('2','expedia@agent.com',md5('abcd1234'));

INSERT INTO ticket(airline,email,flight_number,ID,sold_price,departure_date_time)
VALUES('Air China','testcustomer@nyu.edu','102','1',300,'2019-11-12 13:25:25'),
('Air China','user1@nyu.edu','102','2',300,'2019-11-12 13:25:25'),
('Air China','user2@nyu.edu','102','3',300,'2019-11-12 13:25:25'),
('Air China','user1@nyu.edu','104','4',300,'2019-12-12 13:25:25'),
('Air China','testcustomer@nyu.edu','104','5',300,'2019-12-12 13:25:25'),
('Air China','testcustomer@nyu.edu','106','6',350,'2019-10-12 13:25:25'),
('Air China','user3@nyu.edu','106','7',350,'2019-10-12 13:25:25'),
('Air China','user3@nyu.edu','839','8',300,'2019-02-12 13:25:25'),
('Air China','user3@nyu.edu','102','9',360,'2019-11-12 13:25:25'),
('Air China','user3@nyu.edu','134','11',300,'2019-08-12 13:25:25'),
('Air China','testcustomer@nyu.edu','715','12',500,'2019-11-28 10:25:25'),
('Air China','user3@nyu.edu','206','14',400,'2020-01-12 13:25:25'),
('Air China','user1@nyu.edu','206','15',400,'2020-01-12 13:25:25'),
('Air China','user2@nyu.edu','206','16',400,'2020-01-12 13:25:25'),,
('Air China','user1@nyu.edu','207','17',300,'2020-02-12 13:25:25'),
('Air China','testcustomer@nyu.edu','207','18',300,'2020-02-12 13:25:25'),
('Air China','user1@nyu.edu','296','19',3000,'2020-01-01 13:25:25'),
('Air China','testcustomer@nyu.edu','296','20',3000,'2020-01-01 13:25:25');

INSERT INTO purchase(ID,booking_agent_id,card_type,card_number,name_on_card,expiration_date,purchase_date_time)
VALUES('1','1','credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-10-12 11:55:55'),
('2',NULL,'credit','1111-2222-3333-5555','User 1','2023-03-01','2019-10-11 11:55:55'),
('3',NULL,'credit','1111-2222-3333-4444','User 2','2023-03-01','2019-11-11 11:55:55'),
('4',NULL,'credit','1111-2222-3333-5555','User 1','2023-03-01','2019-10-21 11:55:55'),
('5','1','credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-11-28 11:55:55'),
('6','1','credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-10-05 11:55:55'),
('7',NULL,'credit','1111-2222-3333-5555','User 3','2023-03-01','2019-09-03 11:55:55'),
('8',NULL,'credit','1111-2222-3333-5555','User 3','2023-03-01','2019-02-03 11:55:55'),
('9',NULL,'credit','1111-2222-3333-5555','User 3','2023-03-01','2019-09-03 11:55:55'),
('11','2','credit','1111-2222-3333-5555','User 3','2023-03-01','2019-02-23 11:55:55'),
('12','1','credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-10-05 11:55:55'),
('14','1','credit','1111-2222-3333-5555','User 3','2023-03-01','2019-12-05 11:55:55'),
('15',NULL,'credit','1111-2222-3333-5555','User 1','2023-03-01','2019-12-06 11:55:55'),
('16',NULL,'credit','1111-2222-3333-5555','User 2','2023-03-01','2019-11-19 11:55:55'),
('17','1','credit','1111-2222-3333-5555','User 1','2023-03-01','2019-10-11 11:55:55'),
('18','1','credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-11-25 11:55:55'),
('19','2','credit','1111-2222-3333-5555','User 1','2023-03-01','2019-12-04 11:55:55'),
('20',NULL,'credit','1111-2222-3333-4444','Test Customer 1','2023-03-01','2019-09-12 11:55:55');

INSERT INTO rate(email,flight_number,airline,departure_date_time,rating,comment)
VALUES("testcustomer@nyu.edu",'102','Air China','2019-11-12 13:25:25',4,'Very Comfortable'),
("user1@nyu.edu",'102','Air China','2019-11-12 13:25:25',5,'Relaxing, check-in and onboarding very professional'),
("user2@nyu.edu",'102','Air China','2019-11-12 13:25:25',3,'Satisfied and will use the same flight again'),
("testcustomer@nyu.edu",'104','Air China','2019-12-12 13:25:25',1,'Customer Care services are not good'),
("user1@nyu.edu",'104','Air China','2019-12-12 13:25:25',5,'Comfortable journey and Professional');
