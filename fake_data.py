from faker import Faker
import datetime
from random import randint,sample,choice
fake = Faker('en_US')
# # generate fake departure and arrival time
# fake_datetime_d = fake.date_time_between_dates(datetime_start=datetime.date(2019,1,1), datetime_end=datetime.date(2021,1,1))
# print('fake departure datetime: ', fake_datetime_d)
# fake_datetime_a = fake.date_time_between_dates(datetime_start=fake_datetime_d,datetime_end=fake_datetime_d+datetime.timedelta(days=2))
# print('fake arrival datetime: ' ,fake_datetime_a)
# # generate fake names
# print(fake.name())
# generate insert commands
airport_list = ['HKG','PEK','ALT','LAX','HND','DXB','ORD','LHR','CDG','DFW','CAN']
airline_list = ['ANA','Spring','Emirates','Delta','China Eastern']
plane_id_list = [str(i) for i in range(1,7)]
status_list = ['on-time','delay']
for i in range(50):
    flight_number = randint(10000,99999)
    price = randint(100,999)
    rand_city = sample(airport_list,2)
    airport_d = rand_city[0]
    airport_a = rand_city[1]
    fake_datetime_d = fake.date_time_between_dates(datetime_start=datetime.date(2019,1,1), datetime_end=datetime.date(2021,1,1))
    fake_datetime_a = fake.date_time_between_dates(datetime_start=fake_datetime_d,datetime_end=fake_datetime_d+datetime.timedelta(days=2))
    airline = choice(airline_list)
    plane_ID = choice(plane_id_list)
    status = choice(status_list)
    command ='INSERT INTO flight(airline,arrival_airport,arrival_date_time,base_price,departure_airport,departure_date_time,flight_number,plane_ID,`status`)' + 'VALUES(' +'"'+ airline + '",'+'"'+airport_a +  '",'+ '"'+ str(fake_datetime_a) +'",'+ '"'+ str(price) + '",'+ '"'+ airport_d + '",' + '"'+ str(fake_datetime_d) + '",'+ '"'+ str(flight_number)+ '",'+ '"'+str(plane_ID) +'",'+ '"'+status+'");'

    print(command)

