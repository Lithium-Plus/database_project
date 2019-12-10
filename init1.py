#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from dateutil.relativedelta import relativedelta
from pymysql import NULL


#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='AirTicketReservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/registerselect')
def registerselect():
	return render_template('register.html')

@app.route('/register/customer', methods=['GET', 'POST'])
def registercustomer():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		state = request.form['state']
		city = request.form['city']
		street = request.form['street']
		building = request.form['building']
		phone = request.form['phone']
		ppnumber = request.form['ppnumber']
		ppexp = request.form['ppexpiration']
		ppcountry = request.form['ppcountry']
		dob = request.form['dob']
		cursor = conn.cursor()
		query = 'SELECT * FROM Customer WHERE email = "%s"'
		cursor.execute(query %(email))
		data = cursor.fetchone()
		error = None
		if (data):
			error = "This user already exists"
			return render_template('register.html', error=error)
		else:
			ins = "INSERT INTO customer(building_number,city,date_of_birth,email,name,passport_country,passport_expiration,passport_number,`password`,phone_number,state,street) VALUES('%s','%s','%s','%s','%s','%s','%s','%s',md5('%s'),'%s','%s','%s')"
			print(ins %(building,city,dob,email,name,ppcountry,ppexp,ppnumber,password,phone,state,street))
			cursor.execute(ins %(building,city,dob,email,name,ppcountry,ppexp,ppnumber,password,phone,state,street))
			conn.commit()
			cursor.close()
			return redirect(url_for("hello"))
	else:
		return render_template('r_customer.html')

@app.route('/register/agent', methods=['GET', 'POST'])
def registeragent():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		ID = request.form['agentID']
		query = 'SELECT * FROM Agent WHERE email = "%s"'
		cursor = conn.cursor()
		cursor.execute(query %(email))
		data = cursor.fetchone()
		error = None
		if (data):
			error = "This user already exists"
			return render_template('register.html', error=error)
		else:
			ins = "INSERT INTO agent(booking_agent_id,email,`password`) VALUES('%s','%s',md5('%s'))"
			cursor.execute(ins %(ID,email,password))
			conn.commit()
			cursor.close()
			return redirect(url_for("hello"))
	else:
		return render_template('r_agent.html')

@app.route('/register/staff', methods=['GET', 'POST'])
def registerstaff():
	if request.method == 'POST':
		airline = request.form["airline"]
		email = request.form['email']
		password = request.form['password']
		firstname = request.form['fname']
		lastname = request.form['lname']
		dob = request.form['dob']
		phone = request.form['phone']
		query = 'SELECT * FROM Staff WHERE email = "%s"'
		cursor = conn.cursor()
		cursor.execute(query %(email))
		data = cursor.fetchone()
		error = None
		if (data):
			error = "This user already exists"
			return render_template('register.html', error=error)
		else:
			try:
				ins = "INSERT INTO staff(airline,date_of_birth,firstname,lastname,`password`,email) VALUES('%s','%s','%s','%s',md5('%s'),'%s')"
				cursor.execute(ins %(airline,dob,firstname,lastname,password,email))
				conn.commit()
				ins2 = "INSERT INTO phone(username,phone_number) VALUES('%s','%s')"
				cursor.execute((ins2 %(email,phone)))
				conn.commit()
				cursor.close()
				return redirect(url_for("hello"))
			except:
				error = "Invalid Input!"
				return render_template('register.html', error=error)
	else:
		return render_template('r_staff.html')

@app.route('/visitor')
def visitor():
	return render_template('visitor.html')

#Define route for view flight status
@app.route('/view_flight_status', methods = ['GET', 'POST'])
def view_flight_status():
	cursor = conn.cursor()
	oneway = True
	airline_query = "SELECT DISTINCT name FROM airline;"
	cursor.execute(airline_query)
	airline_list = cursor.fetchall()
	airline_list = [i['name'] for i in airline_list]
	flight_num_query = "SELECT DISTINCT flight_number FROM flight;"
	cursor.execute(flight_num_query)
	flight_num_list = cursor.fetchall()
	flight_num_list = [i['flight_number'] for i in flight_num_list]
	if request.method == 'POST':
		Ddate = request.form["Ddate"]
		Adate = request.form["Adate"]
		airline = request.form["airline"]
		flight_number = request.form["flight_number"]
		if len(Ddate) > 0:
			query = 'SELECT f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city, f.status FROM Flight AS f, Airport AS a1, Airport AS a2 WHERE f.departure_airport=a1.name AND f.arrival_airport=a2.name AND f.flight_number = "%s" AND f.airline = "%s" AND f.departure_date_time BETWEEN "%s" AND "%s" '			
			cursor.execute(query %(flight_number, airline, Ddate,Ddate+" 23:59:59"))
			data = cursor.fetchall()
			return render_template('view_flight_status.html', flights=data, oneway=oneway,flight_num_list=flight_num_list,airline_list=airline_list)
		elif len(Adate) > 0:
			query = 'SELECT f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city, f.status FROM Flight AS f, Airport AS a1, Airport AS a2 WHERE f.departure_airport=a1.name AND f.arrival_airport=a2.name AND f.flight_number = "%s" AND f.airline = "%s" AND f.arrival_date_time BETWEEN "%s" AND "%s" '	
			cursor.execute(query %(flight_number, airline, Adate,Adate+" 23:59:59"))
			data = cursor.fetchall()
			return render_template('view_flight_status.html', flights=data, oneway=oneway,flight_num_list=flight_num_list,airline_list=airline_list)
	else:
		return render_template('view_flight_status.html',flight_num_list=flight_num_list,airline_list=airline_list)

@app.route('/customer')
def customer():
	username = session['username']
	cursor = conn.cursor()
	query = 'SELECT name FROM Customer WHERE email = "%s"'
	cursor.execute(query %(username))
	name = cursor.fetchall()[0]['name']
	return render_template('customer.html', username=name)

@app.route('/customer/viewmyflights', methods=['GET', 'POST'])
def viewmyflights():
	username = session['username']
	cursor = conn.cursor()
	if request.method == 'POST':
		startDate = request.form.get('startDate')
		endDate = request.form['endDate']
		arr_airport = request.form['destination']

		if startDate != "" and endDate != "":
			if arr_airport != "":
				query = 'SELECT Ticket.ID, Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.airline = Flight.airline AND Ticket.departure_date_time=Flight.departure_date_time AND Ticket.email="%s" AND Flight.departure_date_time BETWEEN "%s" AND "%s" AND Flight.arrival_airport="%s"'
				cursor.execute(query % (username,startDate,endDate,arr_airport))
				data1 = cursor.fetchall()
			else:
				query = 'SELECT Ticket.ID, Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.airline = Flight.airline AND Ticket.departure_date_time=Flight.departure_date_time AND Ticket.email="%s" AND Flight.departure_date_time BETWEEN "%s" AND "%s"'
				cursor.execute(query % (username, startDate, endDate))
				data1 = cursor.fetchall()
		else:
			if arr_airport != "":
				query = 'SELECT Ticket.ID, Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.airline = Flight.airline AND Ticket.departure_date_time=Flight.departure_date_time AND Ticket.email="%s" AND Flight.arrival_airport="%s"'
				cursor.execute(query % (username, arr_airport))
				data1 = cursor.fetchall()
			else:
				query = 'SELECT Ticket.ID, Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.airline = Flight.airline AND Ticket.departure_date_time=Flight.departure_date_time AND Ticket.email="%s"'
				cursor.execute(query % (username))
				data1 = cursor.fetchall()
		cursor.close()
		print(data1)
		return render_template('viewmyflights.html', records=data1)

	else:
		query = 'SELECT Ticket.ID, Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.airline = Flight.airline AND Ticket.departure_date_time=Flight.departure_date_time AND Flight.departure_date_time >= NOW() AND Ticket.email="%s"'
		cursor.execute(query % (username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('viewmyflights.html', records=data1)

@app.route('/customer/ratemyflights', methods=['GET', 'POST'])
def ratemyflights():
	email = session['username']
	cursor = conn.cursor()
	message = None
	query = 'SELECT DISTINCT airline FROM Ticket WHERE email="%s" AND departure_date_time <= NOW()'
	cursor.execute(query % (email))
	airline_list = cursor.fetchall()
	airline_list = [i['airline'] for i in airline_list]
	query = 'SELECT DISTINCT flight_number FROM Ticket WHERE email="%s" AND departure_date_time <= NOW()'
	cursor.execute(query % (email))
	flight_num_list = cursor.fetchall()
	flight_num_list = [i['flight_number'] for i in flight_num_list]
	query = 'SELECT DISTINCT departure_date_time FROM Ticket WHERE email="%s" AND departure_date_time <= NOW()'
	cursor.execute(query % (email))
	Ddate_list = cursor.fetchall()
	Ddate_list = [i['departure_date_time'] for i in Ddate_list]
	if request.method == 'POST':
		airline = request.form["airline"]
		flightNumber = request.form["flight_number"]
		departure_date_time = request.form['Ddate']
		rating = request.form["rating"]
		comments = request.form["comments"]
		validation_query = 'SELECT * FROM Flight WHERE Flight.flight_number="%s" AND Flight.departure_date_time="%s" AND Flight.airline="%s"'
		cursor.execute(validation_query %(flightNumber,departure_date_time,airline))
		if len(cursor.fetchall())==0:
			message = "Error! Invalid entry. Please choose right flight information"
		else:
			query = 'SELECT flight_number FROM rate WHERE email="%s" AND flight_number="%s" AND airline="%s" AND departure_date_time="%s"'
			cursor.execute(query %(email,flightNumber,airline,departure_date_time))
			data = cursor.fetchall()
			print(len(data))
			if len(data)==0:
				query = 'INSERT INTO rate(email,flight_number,rating,comment,airline,departure_date_time) VALUES("%s","%s","%s","%s","%s","%s")'
				cursor.execute(query %(email,flightNumber,rating,comments,airline,departure_date_time))
				conn.commit()
				message = "Your response has been successfully recorded!"
			else:
				message = "You cannot submit twice for the same flight or wrong flight information!"
		return render_template("ratemyflights.html",flight_num_list=flight_num_list,airline_list=airline_list,Ddate_list=Ddate_list,message=message)
	else:
		return render_template("ratemyflights.html",flight_num_list=flight_num_list,airline_list=airline_list,Ddate_list=Ddate_list,message=message)

@app.route('/searchflights', methods=['GET','POST'])
def searchflights():
	cursor = conn.cursor()
	oneway = True
	if request.method == 'POST':
		oneway = request.form.getlist('oneway')
		roundtrip = request.form.getlist('roundtrip')
		LstartDate = request.form["LstartDate"]
		LendDate = request.form["LendDate"]
		Dcity = request.form["Dcity"]
		Acity = request.form["Acity"]
		RstartDate = request.form["RstartDate"]
		RendDate = request.form["RendDate"]
		query = 'SELECT f.base_price, Airplane.number_of_seats, f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airplane , Airport AS a1, Airport AS a2 WHERE Airplane.ID=f.plane_ID AND f.departure_airport=a1.name AND f.arrival_airport=a2.name AND f.departure_date_time BETWEEN "%s" AND "%s" AND a1.city="%s" AND a2.city = "%s"'
		if len(oneway) != 0 and oneway[0] == "oneway":
			oneway = True
			cursor.execute(query % (LstartDate, LendDate, Dcity, Acity))

			data = cursor.fetchall()
			for line in data:
				cursor.execute("SELECT COUNT(*) FROM Ticket WHERE Ticket.flight_number='%s' AND Ticket.airline='%s' AND Ticket.departure_date_time='%s'" % (line["flight_number"],line["airline"],line['departure_date_time']))
				soldNum = cursor.fetchone()['COUNT(*)']
				if soldNum >= 0.7*line["number_of_seats"] and soldNum<=line["number_of_seats"]:
					soldprice = (line['base_price']*1.2)
					line["soldPrice"] = soldprice
				elif soldNum <= line["number_of_seats"]:
					soldprice = (line["base_price"])
					line["soldPrice"] = soldprice
				else:
					line["soldPrice"] = "Full"
			print(data)
			cursor.close()
			#return redirect(url_for("search_results", flights=data, oneway=oneway))
			return render_template('searchflights_results.html', flights=data, oneway=oneway)
		elif len(roundtrip) != 0 and roundtrip[0] == "roundtrip":
			oneway = False
			cursor.execute(query % (LstartDate, LendDate, Dcity, Acity))
			ldata = cursor.fetchall()
			for line in ldata:
				cursor.execute(
					"SELECT COUNT(*) FROM Ticket WHERE Ticket.flight_number='%s' AND Ticket.airline='%s' AND Ticket.departure_date_time='%s'" % (
					line["flight_number"], line["airline"], line['departure_date_time']))
				soldNum = cursor.fetchone()['COUNT(*)']
				if soldNum >= 0.7 * line["number_of_seats"] and soldNum <= line["number_of_seats"]:
					soldprice = (line['base_price'] * 1.2)
					line["soldPrice"] = soldprice
				elif soldNum <= line["number_of_seats"]:
					soldprice = (line["base_price"])
					line["soldPrice"] = soldprice
				else:
					line["soldPrice"] = "Full"

			cursor.execute(query % (RstartDate, RendDate, Acity, Dcity))
			rdata = cursor.fetchall()
			for line in rdata:
				cursor.execute(
					"SELECT COUNT(*) FROM Ticket WHERE Ticket.flight_number='%s' AND Ticket.airline='%s' AND Ticket.departure_date_time='%s'" % (
					line["flight_number"], line["airline"], line['departure_date_time']))
				soldNum = cursor.fetchone()['COUNT(*)']
				if soldNum >= 0.7 * line["number_of_seats"] and soldNum <= line["number_of_seats"]:
					soldprice = (line['base_price'] * 1.2)
					line["soldPrice"] = soldprice
				elif soldNum <= line["number_of_seats"]:
					soldprice = (line["base_price"])
					line["soldPrice"] = soldprice
				else:
					line["soldPrice"] = "Full"
			cursor.close()
			return render_template('searchflights_results.html', Lflights=ldata, Rflights=rdata, oneway=oneway)
		#return redirect("searchflights_results.html")
		else:
			return render_template('searchflights.html', userType=session["userType"])
	else:
		return render_template('searchflights.html',userType=session["userType"])

@app.route('/customer/searchflights/results', methods=['GET','POST'])
def search_results():
	if request.method == 'POST':
		selectedflight = request.form.get("selectedflight")
		session['selectedflight'] = selectedflight
		if selectedflight != None:
			if session["userType"] == "Customer":
				return redirect(url_for("c_purchase"))
			else:
				return redirect(url_for("a_purchase"))
		else:
			return render_template("searchflights_results.html")
	else:
		return  render_template("searchflights_results.html")

@app.route('/customer/purchase', methods=['GET','POST'])
def c_purchase():
	cursor = conn.cursor()
	thisflight = session['selectedflight'].split(",")
	flight_ID = thisflight[0]
	Ddate = thisflight[1]
	airline = thisflight[2]
	soldPrice = thisflight[3]
	email = session["username"]
	if request.method == 'POST':
		cursor.execute("SELECT COUNT(*) FROM Ticket")
		soldNum = cursor.fetchone()['COUNT(*)']
		print(soldNum)
		ticketID = soldNum+1
		print(ticketID)
		cardType = request.form["cardType"]
		cardNum = request.form["cardNum"]
		cardName = request.form["cardName"]
		cardExp = request.form["cardExp"]
		time = request.form["time"]
		print(time)
		ins = "INSERT INTO ticket(airline,email,flight_number,ID,sold_price,departure_date_time) VALUES('%s','%s','%s','%s','%s','%s')"
		cursor.execute(ins % (airline,email,flight_ID,ticketID,soldPrice,Ddate))
		conn.commit()
		ins1 = "INSERT INTO purchase(ID,card_type,card_number,name_on_card,expiration_date,purchase_date_time) VALUES('%s','%s','%s','%s','%s','%s')"
		cursor.execute(ins1 % (ticketID,cardType,cardNum,cardName,cardExp,time))
		conn.commit()
		session.pop("selectedflight")
		return redirect(url_for("customer"))
	else:
		return render_template("c_purchase.html",flight_ID=flight_ID,Ddate=Ddate,airline=airline,soldPrice=soldPrice)

@app.route('/customer/trackmyspending', methods=['GET','POST'])
def trackmyspending():
	cursor = conn.cursor()
	email = session["username"]
	labels = []
	label_temp = []
	values = []
	endDate = datetime.date.today() + relativedelta(months=1)
	startDate = endDate - relativedelta(months=6)
	yearago = endDate - relativedelta(months=12)
	query = 'SELECT SUM(t.sold_price) AS year_total FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND t.email="%s" AND p.booking_agent_ID IS NULL AND p.purchase_date_time BETWEEN "%s" AND "%s"'
	cursor.execute(query % (email, yearago, endDate))
	data = cursor.fetchall()
	year_total = data[0]["year_total"]
	if year_total == None:
		year_total = 0
	query = 'SELECT YEAR(p.purchase_date_time) AS year, MONTH(p.purchase_date_time) AS month,SUM(t.sold_price) AS month_total FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND t.email="%s" AND p.booking_agent_ID IS NULL AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY YEAR(p.purchase_date_time),MONTH(p.purchase_date_time)'
	cursor.execute(query %(email,startDate,endDate))
	data = cursor.fetchall()
	d = startDate
	while d.year != endDate.year or d.month != endDate.month:
		thislabel = str(d.year) + "-" + str(d.month)
		labels.append(thislabel)
		label_temp.append([d.year, d.month])
		values.append(0)
		d = d + relativedelta(months=1)
	if len(data)!=0:
		for i in range(6):
			for line in data:
				if line['year'] == label_temp[i][0] and line['month'] == label_temp[i][1]:
					values[i] = float(line["month_total"])
	if request.method == "POST":
		startDate = request.form["sDate"]
		startDate = datetime.datetime.strptime(startDate,'%Y-%m-%d')
		endDate = request.form["eDate"]
		endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
		query = 'SELECT SUM(t.sold_price) AS total FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND t.email="%s" AND p.booking_agent_ID IS NULL AND p.purchase_date_time BETWEEN "%s" AND "%s"'
		cursor.execute(query % (email, startDate, endDate))
		data = cursor.fetchall()
		total = data[0]["total"]
		if total==None:
			total = 0
		print(len(data),total)
		query = 'SELECT YEAR(p.purchase_date_time) AS year, MONTH(p.purchase_date_time) AS month,SUM(t.sold_price) AS month_total FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND t.email="%s" AND p.booking_agent_ID IS NULL AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY YEAR(p.purchase_date_time),MONTH(p.purchase_date_time)'
		cursor.execute(query % (email, startDate, endDate))
		data = cursor.fetchall()
		values = []
		labels = []
		label_temp = []
		d = startDate
		while d.year != endDate.year or d.month != endDate.month:
			thislabel = str(d.year)+"-"+str(d.month)
			labels.append(thislabel)
			label_temp.append([d.year,d.month])
			values.append(0)
			d = d + relativedelta(months=1)
		if len(data) != 0:
			for i in range(len(labels)):
				for line in data:
					if line['year']==label_temp[i][0] and line['month']==label_temp[i][1]:
						values[i] = float(line["month_total"])
			return render_template("trackmyspending.html",money=values,month=labels,total=total)
		else:
			return render_template("trackmyspending.html", money=values, month=labels,total=total)
	else:
		return render_template("trackmyspending.html",money=values,month=labels,year_total=year_total)

@app.route('/visitor_search', methods=['GET','POST'])

def visitor_search():
	cursor = conn.cursor()
	oneway = True
	city_query = "SELECT DISTINCT city FROM airport;"
	cursor.execute(city_query)
	city_list = cursor.fetchall()
	city_list = [i['city'] for i in city_list]

	if request.method == 'POST':
		DstartDate1 = request.form["DstartDate1"]
		DendDate1 = request.form["DendDate1"]
		Dcity1 = request.form["Dcity1"]
		Acity1 = request.form["Acity1"]
		LstartDate = request.form["LstartDate"]
		LendDate = request.form["LendDate"]
		Dcity = request.form["Dcity"]
		Acity = request.form["Acity"]
		RstartDate = request.form["RstartDate"]
		RendDate = request.form["RendDate"]
		query = 'SELECT f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airport AS a1, Airport AS a2 WHERE f.departure_airport=a1.name AND f.arrival_airport=a2.name AND f.departure_date_time BETWEEN "%s" AND "%s" AND a1.city="%s" AND a2.city = "%s"'
		if DstartDate1!="" and DendDate1!="" and Dcity1!="" and Acity1!="":
			oneway = True
			cursor.execute(query %(DstartDate1, DendDate1, Dcity1, Acity1))
			data = cursor.fetchall()
			return render_template('visitor_search.html', flights=data, oneway=oneway,city_list=city_list)
		elif LstartDate!="" and LendDate!="" and Dcity!="" and Acity!="" and RstartDate!="" and RendDate!="":
			oneway = False
			cursor.execute(query %(LstartDate, LendDate, Dcity, Acity))
			ldata = cursor.fetchall()
			cursor.execute(query % (RstartDate, RendDate, Acity, Dcity))
			rdata = cursor.fetchall()
			return render_template('visitor_search.html',Lflights=ldata,Rflights=rdata,oneway=oneway,city_list=city_list)
	else:
		return render_template('visitor_search.html',city_list=city_list)



@app.route('/agent')
def agent():
	email = session["username"]
	return render_template('agent.html',username=email)

@app.route('/agent/viewmyflights', methods=['GET', 'POST'])
def a_viewmyflights():
	cursor = conn.cursor()
	cursor.execute('SELECT booking_agent_id FROM Agent WHERE email="%s"' % (session["username"]))
	agent_id = cursor.fetchall()[0]["booking_agent_id"]
	if request.method == 'POST':
		startDate = request.form.get('startDate')
		endDate = request.form['endDate']
		query = 'SELECT t.ID,t.email,f.airline,f.flight_number,f.plane_ID,f.departure_date_time,f.departure_airport,f.arrival_date_time,f.arrival_airport,f.status FROM Ticket AS t, Flight AS f, Purchase AS p WHERE t.ID=p.ID AND t.airline=f.airline AND t.flight_number=f.flight_number AND t.departure_date_time=f.departure_date_time AND p.booking_agent_ID="%s" AND f.departure_date_time BETWEEN "%s" AND "%s"'
		cursor.execute(query % (agent_id,startDate,endDate))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('a_viewmyflights.html', records=data1)

	else:
		query = 'SELECT t.ID,t.email,f.airline,f.flight_number,f.plane_ID,f.departure_date_time,f.departure_airport,f.arrival_date_time,f.arrival_airport,f.status FROM Ticket AS t, Flight AS f, Purchase AS p WHERE t.ID=p.ID AND t.airline=f.airline AND t.flight_number=f.flight_number AND t.departure_date_time=f.departure_date_time AND p.booking_agent_ID="%s" AND f.departure_date_time >= NOW()'
		cursor.execute(query % (agent_id))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('a_viewmyflights.html', records=data1)

@app.route('/agent/purchase', methods=['GET','POST'])
def a_purchase():
	cursor = conn.cursor()
	thisflight = session['selectedflight'].split(",")
	flight_ID = thisflight[0]
	Ddate = thisflight[1]
	airline = thisflight[2]
	soldPrice = thisflight[3]
	cursor.execute('SELECT booking_agent_id FROM Agent WHERE email="%s"' %(session["username"]))
	agent_id = cursor.fetchall()[0]["booking_agent_id"]
	if request.method == 'POST':
		cursor.execute("SELECT COUNT(*) FROM Ticket")
		soldNum = cursor.fetchone()['COUNT(*)']
		print(soldNum)
		ticketID = soldNum+1
		print(ticketID)
		email = request.form["email"]
		cardType = request.form["cardType"]
		cardNum = request.form["cardNum"]
		cardName = request.form["cardName"]
		cardExp = request.form["cardExp"]
		time = request.form["time"]
		ins = "INSERT INTO ticket(airline,email,flight_number,ID,sold_price,departure_date_time) VALUES('%s','%s','%s','%s','%s','%s')"
		cursor.execute(ins % (airline,email,flight_ID,ticketID,soldPrice,Ddate))
		conn.commit()
		ins1 = "INSERT INTO purchase(booking_agent_ID,ID,card_type,card_number,name_on_card,expiration_date,purchase_date_time) VALUES('%s','%s','%s','%s','%s','%s','%s')"
		cursor.execute(ins1 % (agent_id,ticketID,cardType,cardNum,cardName,cardExp,time))
		conn.commit()
		session.pop("selectedflight")
		return redirect(url_for("agent"))
	else:
		return render_template("a_purchase.html",flight_ID=flight_ID,Ddate=Ddate,airline=airline,soldPrice=soldPrice,agent_id=agent_id)

@app.route('/agent/viewmycommission', methods=['GET','POST'])
def viewmycommission():
	cursor = conn.cursor()
	cursor.execute('SELECT booking_agent_id FROM Agent WHERE email="%s"' % (session["username"]))
	agent_id = cursor.fetchall()[0]["booking_agent_id"]
	query1 = 'SELECT 0.1*SUM(t.sold_price) AS total FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND p.booking_agent_ID="%s" AND p.purchase_date_time BETWEEN "%s" AND "%s"'
	query2 = 'SELECT COUNT(t.ID) AS count FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND p.booking_agent_ID="%s" AND p.purchase_date_time BETWEEN "%s" AND "%s"'
	if request.method == 'POST':
		startDate = request.form["startDate"]
		endDate = request.form["endDate"]
		cursor.execute(query1 % (agent_id, startDate, endDate))
		total = cursor.fetchall()[0]["total"]
		if total == None:
			total = 0
		else:
			total = float(total)
		cursor.execute(query2 % (agent_id, startDate, endDate))
		count = cursor.fetchall()[0]["count"]
		cursor.close()
		if count == None:
			count = 0
		if count == 0:
			avg = 0
		else:
			avg = total / count
		return render_template("viewmycommission.html", total=total, count=count, avg=avg)
	else:
		endDate = datetime.date.today() + relativedelta(days=1)
		startDate = endDate - relativedelta(days=30)
		cursor.execute(query1 %(agent_id,startDate,endDate))
		total = cursor.fetchall()[0]["total"]
		if total == None:
			total = 0
		else:
			total = float(total)
		cursor.execute(query2 % (agent_id, startDate, endDate))
		count = cursor.fetchall()[0]["count"]
		cursor.close()
		if count == None:
			count = 0
		if count == 0:
			avg = 0
		else:
			avg = total/count
		return render_template("viewmycommission.html",total=total,count=count,avg=avg)

@app.route('/agent/viewtopcustomers', methods=['GET','POST'])
def viewtopcustomers():
	cursor = conn.cursor()
	cursor.execute('SELECT booking_agent_id FROM Agent WHERE email="%s"' % (session["username"]))
	agent_id = cursor.fetchall()[0]["booking_agent_id"]
	c_labels = []
	c_values = []
	cm_labels = []
	cm_values = []
	endDate = datetime.date.today() + relativedelta(months=1)
	startDate = endDate - relativedelta(months=6)
	yearago = endDate - relativedelta(months=12)
	query1 = 'SELECT t.email, COUNT(t.ID) AS count FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND p.booking_agent_ID="%s" AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY t.email ORDER BY COUNT(t.ID)'
	query2 = 'SELECT t.email, 0.1*SUM(t.sold_price) AS commission FROM Purchase AS p, Ticket AS t WHERE p.ID=t.ID AND p.booking_agent_ID="%s" AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY t.email ORDER BY SUM(t.sold_price)'
	cursor.execute(query1 % (agent_id,startDate,endDate))
	count = cursor.fetchall()
	cursor.execute(query2 %(agent_id,yearago,endDate))
	commission = cursor.fetchall()
	if len(count) <= 5:
		for line in count:
			c_labels.append(line["email"])
			c_values.append(int(line["count"]))
	else:
		for i in range(5):
			c_labels.append(count[i]["email"])
			c_values.append(int(count[i]["count"]))
	if len(commission) <= 5:
		for line in commission:
			cm_labels.append(line["email"])
			cm_values.append(float(line["commission"]))
	else:
		for i in range(5):
			cm_labels.append(commission[i]["email"])
			cm_values.append(float(commission[i]["commission"]))
	return render_template("viewtopcustomers.html",c_labels=c_labels,c_values=c_values,cm_labels=cm_labels,cm_values=cm_values)

@app.route('/staff')
def staff():
	username = session['username']
	cursor = conn.cursor()
	query = 'SELECT firstname,lastname FROM staff WHERE email = "%s"'
	cursor.execute(query %(username))
	name = cursor.fetchall()[0]['firstname'] 
	return render_template('staff.html',username = name)
@app.route('/staff/myflights', methods=['GET','POST'])
def viewflights():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline FROM staff WHERE email = "%s"'
	cursor.execute(query1 %(username))
	airline_name = cursor.fetchall()[0]['airline'] 
	curr_date = str(datetime.date.today())
	day30 = str(datetime.date.today()+datetime.timedelta(days=30))
	oneway = True
	default_query = 'SELECT f.base_price, f.status, Airplane.number_of_seats, f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airplane , Airport AS a1, Airport AS a2 WHERE Airplane.ID=f.plane_ID AND f.departure_airport=a1.name AND f.arrival_airport=a2.name AND  f.airline = "%s" and f.departure_date_time between "%s" and "%s"' 
	cursor.execute(default_query %(airline_name,curr_date,day30))
	data_default = cursor.fetchall()
	city_query = "SELECT DISTINCT city FROM airport;"
	cursor.execute(city_query)
	city_list = cursor.fetchall()
	city_list = [i['city'] for i in city_list]
	if request.method == 'POST':
		selectedflight = request.form.get("selectedflight")
		if selectedflight != None:
			session['selectedflight'] = selectedflight
			return redirect(url_for("modifyflights"))
		LstartDate = request.form["DstartDate"]
		LendDate = request.form["DendDate"]
		Dcity = request.form["Dcity"]
		Acity = request.form["Acity"]
		query = 'SELECT f.base_price, f.status, Airplane.number_of_seats, f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airplane , Airport AS a1, Airport AS a2 WHERE a1.city = "%s" AND a2.city = "%s" AND Airplane.ID=f.plane_ID AND f.departure_airport=a1.name AND f.arrival_airport=a2.name AND  f.airline = "%s" and f.departure_date_time between "%s" and "%s"' 
		cursor.execute(query % (Dcity, Acity,airline_name,LstartDate, LendDate ))
		data = cursor.fetchall()
		cursor.close()
		return render_template('myflights.html', userType=session["userType"],flights=data,city_list= city_list,search=True)
	else:
		return render_template('myflights.html',userType=session["userType"],flights=data_default,city_list=city_list,search=False)
@app.route('/staff/modifyflights', methods=['GET','POST'])
def modifyflights():
	cursor = conn.cursor()
	thisflight = session['selectedflight'].split(",")
	flight_ID = thisflight[0]
	Ddate = thisflight[1]
	airline = thisflight[2]
	status = thisflight[3].strip()
	query = 'SELECT c.name,c.email,c.passport_country  FROM ticket AS t,customer as c WHERE t.flight_number = "%s" AND  t.departure_date_time = "%s" AND t.airline = "%s" AND t.email = c.email' 
	cursor.execute(query % (flight_ID,Ddate,airline))
	data = cursor.fetchall()
	query_rating = 'SELECT r.comment,r.rating,c.name,r.email FROM rate as r,customer as c WHERE r.flight_number = "%s" AND  r.departure_date_time = "%s" AND r.airline = "%s"  AND r.email = c.email'
	cursor.execute(query_rating % (flight_ID,Ddate,airline))
	ratings = cursor.fetchall()
	# app.logger.warning(len(ratings))
	if len(ratings) > 0 :
		score = []
		for rating in ratings:
			score.append(rating['rating'])
		avg_rating = sum(score)/len(score)
	else:
		avg_rating = False
	if request.method == 'POST':
		new_status = request.form.get("new_status")
		update_query = 'UPDATE flight SET status = "%s" WHERE flight_number = "%s" AND  departure_date_time = "%s" AND airline = "%s";'
		cursor.execute(update_query % (new_status,flight_ID,Ddate,airline))
		conn.commit()
		app.logger.warning('status updated')
		cursor.close()
		return render_template('modify_flight.html',flight_ID=flight_ID,Ddate=Ddate,airline=airline,status=new_status,avg_rating=avg_rating,data=data,ratings=ratings)
	else:
		return render_template('modify_flight.html',flight_ID=flight_ID,Ddate=Ddate,airline=airline,avg_rating=avg_rating,status=status,data=data,ratings=ratings)

@app.route('/staff/add_airplane', methods=['GET','POST'])
def add_airplane():
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline FROM staff WHERE email = "%s"'
	cursor.execute(query1 %(username))
	airline_name = cursor.fetchall()[0]['airline'] 
	if request.method == 'POST':
		ID = request.form.get("ID")
		number_of_seats = request.form.get('number_of_seats')
		add_query = 'INSERT INTO airplane(airline,ID,number_of_seats) VALUES ("%s","%s",%s)'
		cursor.execute(add_query %(airline_name,ID,int(number_of_seats)))
		conn.commit()
		cursor.close()
		return render_template('add_airplane.html',added=True)
	else:
		return render_template('add_airplane.html',added=False)



@app.route('/staff/add_flight', methods=['GET','POST'])
def add_flight():
	cursor = conn.cursor()
	username = session['username']
	cursor = conn.cursor()
	query1 = 'SELECT airline FROM staff WHERE email = "%s"'
	cursor.execute(query1 %(username))
	airline_name = cursor.fetchall()[0]['airline'] 
	query_airport = 'SELECT name FROM airport'
	cursor.execute(query_airport)
	airport_list = cursor.fetchall()
	airport_list = [i['name'] for i in airport_list]
	query_plane_id = 'SELECT ID FROM airplane WHERE airline = "%s"'
	cursor.execute(query_plane_id % (airline_name))
	id_list = cursor.fetchall()
	id_list = [i['ID'] for i in id_list]
	curr_date = str(datetime.date.today())
	day30 = str(datetime.date.today()+datetime.timedelta(days=30))
	default_query = 'SELECT f.base_price, f.status, Airplane.number_of_seats, f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airplane , Airport AS a1, Airport AS a2 WHERE Airplane.ID=f.plane_ID AND f.departure_airport=a1.name AND f.arrival_airport=a2.name AND  f.airline = "%s" and f.departure_date_time between "%s" and "%s"' 
	cursor.execute(default_query %(airline_name,curr_date,day30))
	data_default = cursor.fetchall()


	if request.method == 'POST':
		flight_number = request.form.get("flight_number")
		base_price = request.form.get('base_price')
		DDate = request.form.get('DDate')
		ADate = request.form.get('ADate')
		DAirport = request.form.get('DAirport')
		AAirport = request.form.get('AAirport')
		plane_ID = request.form.get('plane_ID')
		status =  request.form.get('status')
		add_query = 'INSERT INTO flight(flight_number,base_price,departure_date_time,arrival_date_time,airline,departure_airport,arrival_airport,plane_ID,`status`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'
		cursor.execute(add_query % (flight_number,base_price,DDate,ADate,airline_name,DAirport,AAirport,plane_ID,status))
		conn.commit()
		default_query = 'SELECT f.base_price, f.status, Airplane.number_of_seats, f.airline, f.flight_number,f.plane_ID, f.departure_date_time, f.departure_airport, a1.city, f.arrival_date_time, f.arrival_airport, a2.city FROM Flight AS f, Airplane , Airport AS a1, Airport AS a2 WHERE Airplane.ID=f.plane_ID AND f.departure_airport=a1.name AND f.arrival_airport=a2.name AND  f.airline = "%s" and f.departure_date_time between "%s" and "%s"' 
		cursor.execute(default_query %(airline_name,curr_date,day30))
		data_default = cursor.fetchall()
		cursor.close()
		return render_template('add_flight.html',added=True,flights=data_default)
	else:
		return render_template('add_flight.html',added=False,airport_list=airport_list,id_list=id_list,flights=data_default)


@app.route('/staff/add_airport', methods=['GET','POST'])
def add_airport():
	cursor = conn.cursor()
	if request.method == 'POST':
		name = request.form.get("name")
		city = request.form.get('city')
		add_query = 'INSERT INTO airport(name,city) VALUES ("%s","%s")'
		cursor.execute(add_query % (name,city))
		conn.commit()
		cursor.close()
		return render_template('add_airport.html',added=True)
	else:
		return render_template('add_airport.html',added=False)


@app.route('/staff/view_agents', methods=['GET','POST'])
def view_agents():
	today =  datetime.date.today()
	lastmonth = datetime.date.today() - relativedelta(months=1)
	lastyear = datetime.date.today() - relativedelta(months=12)
	cursor = conn.cursor()	
	# query = 'SELECT email,booking_agent_id FROM agent'
	# cursor.execute(query)
	# data = cursor.fetchall()
	query_month =  'SELECT a.email,a.booking_agent_id,count(*) AS sale FROM agent AS a, purchase AS p WHERE p.booking_agent_ID = a.booking_agent_ID AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY a.booking_agent_ID,a.email ORDER BY sale DESC'
	cursor.execute(query_month % (lastmonth,today))
	last_month = cursor.fetchall()[:5]
	query_year =  'SELECT a.email,a.booking_agent_id,count(*) AS sale FROM agent AS a, purchase AS p WHERE p.booking_agent_ID = a.booking_agent_ID AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY a.booking_agent_ID,a.email ORDER BY sale DESC'
	cursor.execute(query_year % (lastyear,today))
	last_year = cursor.fetchall()[:5]
	query_commission =  'SELECT a.email,a.booking_agent_id,0.1*SUM(t.sold_price) AS commission FROM agent AS a, purchase AS p,ticket as t WHERE t.ID = p.ID AND p.booking_agent_ID = a.booking_agent_ID AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY a.booking_agent_ID,a.email ORDER BY commission DESC'
	cursor.execute(query_commission % (lastyear,today))
	commission = cursor.fetchall()[:5]
	return render_template('view_agents.html',last_month = last_month,last_year = last_year,commission= commission)

@app.route('/staff/view_customers', methods=['GET','POST'])
def view_customers():
	username = session['username']
	cursor = conn.cursor()
	today =  datetime.date.today()
	lastyear = datetime.date.today() - relativedelta(months=12)
	query_most = 'SELECT c.email,c.name,count(*) AS number_of_tickets FROM customer AS c, ticket AS t,airline AS a,staff AS s,purchase as p WHERE t.airline = a.name AND s.email = "%s" ANd s.airline = a.name AND t.email = c.email AND t.ID = p.ID AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY c.email ORDER BY number_of_tickets DESC'
	cursor.execute(query_most % (username,lastyear,today))
	most = cursor.fetchall()[:1]
	query_cust = 'SELECT DISTINCT c.name FROM customer AS c, ticket AS t,airline AS a,staff AS s,purchase as p WHERE t.airline = a.name AND s.email = "%s" ANd s.airline = a.name AND t.email = c.email'
	# app.logger.warning(most)
	cursor.execute(query_cust% (username))
	customer_list = cursor.fetchall()
	customer_list = [i['name'] for i in customer_list]
	if request.method == 'POST':
		customer = request.form.get("customer")
		query = 'SELECT t.flight_number,t.departure_date_time FROM customer AS c, ticket AS t,airline AS a,staff AS s,purchase as p WHERE c.name = "%s" AND t.airline = a.name AND s.email = "%s" ANd s.airline = a.name AND t.email = c.email AND t.ID = p.ID AND t.departure_date_time <= CURDATE()' 
		
		cursor.execute(query %(customer,username))
		data = cursor.fetchall()
		return render_template('view_customer.html',most = most,data=data,customer_list=customer_list,cust=customer)
	else:
		return render_template('view_customer.html',most = most,customer_list=customer_list)

@app.route('/staff/view_reports', methods=['GET','POST'])
def view_reports():
	cursor = conn.cursor()
	email = session["username"]
	labels = []
	label_temp = []
	values = []
	today = datetime.date.today() 
	last_year = today - relativedelta(months=12)
	last_month = today - relativedelta(months=1)
	query = 'SELECT YEAR(p.purchase_date_time) AS year, MONTH(p.purchase_date_time) AS month,COUNT(*) AS month_total FROM Purchase AS p, Ticket AS t,staff as s WHERE p.ID=t.ID AND s.email="%s" AND s.airline = t.airline AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY YEAR(p.purchase_date_time),MONTH(p.purchase_date_time)'
	cursor.execute(query % (email, last_year,today))
	data = cursor.fetchall()
	d = last_year
	while d.year != today.year or d.month != today.month:
			thislabel = str(d.year)+"-"+str(d.month)
			# app.logger.warning(thislabel)
			labels.append(thislabel)
			label_temp.append([d.year,d.month])
			values.append(0)
			d = d + relativedelta(months=1)
	if len(data) != 0:
		for i in range(len(labels)):
			for line in data:
				if line['year']==label_temp[i][0] and line['month']==label_temp[i][1]:
					values[i] = float(line["month_total"])
	if len(values) != 0:
		year_total = sum(values)
	else:
		year_total = 0
	last_month_total = values[-1]

	if request.method == "POST":
		startDate = request.form["sDate"]
		startDate = datetime.datetime.strptime(startDate,'%Y-%m-%d')
		endDate = request.form["eDate"]
		endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
		cursor.execute(query % (email, startDate, endDate))
		data = cursor.fetchall()
		values = []
		labels = []
		label_temp = []
		total = 0
		d = startDate
		while d.year != endDate.year or d.month != endDate.month:
			thislabel = str(d.year)+"-"+str(d.month)
			labels.append(thislabel)
			label_temp.append([d.year,d.month])
			values.append(0)
			d = d + relativedelta(months=1)
		if len(data) != 0:
			for i in range(len(labels)):
				for line in data:
					if line['year']==label_temp[i][0] and line['month']==label_temp[i][1]:
						values[i] = float(line["month_total"])
						total += values[i]
			return render_template("view_reports.html",money=values,month=labels,total=total,year_total=year_total,last_month_total=last_month_total)
		else:
			return render_template("view_reports.html", money=values, month=labels,total=total,year_total=year_total,last_month_total=last_month_total)
	else:
		return render_template("view_reports.html",money=values,month=labels,year_total=year_total,last_month_total=last_month_total)
@app.route('/staff/view_revenue', methods=['GET','POST'])
def view_revenue():
	cursor = conn.cursor()
	email = session["username"]
	last_year_values = [0,0]
	last_month_values = [0,0]
	today = datetime.date.today()
	last_year = today - relativedelta(months=12)
	last_month = today - relativedelta(months=1)
	query = 'SELECT p.booking_agent_id,SUM(t.sold_price) AS total FROM Purchase AS p, Ticket AS t,staff as s WHERE p.ID=t.ID AND s.email="%s" AND s.airline = t.airline AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY booking_agent_id'
	cursor.execute(query % (email, last_year,today))
	last_year_data = cursor.fetchall()
	if len(last_year_data) != 0:
		for line in last_year_data:
			if line['booking_agent_id'] is None:
				last_year_values[0] += float(line['total'])
			else:
				last_year_values[1] += float(line['total'])
	cursor.execute(query % (email, last_month,today))
	last_month_data = cursor.fetchall()
	if len(last_month_data) != 0:
		for line in last_month_data:
			if line['booking_agent_id'] is None:
				last_month_values[0] += float(line['total'])
			else:
				last_month_values[1] += float(line['total'])
	if request.method == "POST":
		selection = request.form["selection"]
		if selection == 'last month':
			return render_template('view_revenue.html',data=last_month_values,last_year_data=False)
		else:
			return render_template('view_revenue.html',data=last_year_values,last_year_data=True)
	else:
		return render_template('view_revenue.html',data=last_year_values,last_year_data=True)

@app.route('/staff/view_destinations', methods=['GET','POST'])
def view_destinations():
	cursor = conn.cursor()
	email = session["username"]
	today = datetime.date.today() + relativedelta(months=1)
	last_year = today - relativedelta(months=12)
	last_3month = today - relativedelta(months=3)
	query = 'SELECT a.city,COUNT(*) AS number_of_tickets FROM Purchase AS p, Ticket AS t,staff as s,airport as a,flight as f WHERE t.flight_number = f.flight_number AND f.departure_date_time = t.departure_date_time AND f.arrival_airport = a.name AND p.ID=t.ID AND s.email="%s" AND s.airline = t.airline AND p.purchase_date_time BETWEEN "%s" AND "%s" GROUP BY a.city ORDER BY number_of_tickets DESC'
	cursor.execute(query % (email, last_year,today))
	last_year_data = cursor.fetchall()[:3]
	cursor.execute(query % (email, last_3month,today))
	last_3month_data = cursor.fetchall()[:3]
	return render_template('view_top_destinations.html',last_year_data=last_year_data,last_3month_data=last_3month_data)

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	userType = request.form['userType']
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM %s WHERE email = "%s" and password = md5("%s")'
	#print(query %(userType, username, password))
	cursor.execute(query %(userType, username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['userType'] = userType
		return redirect(url_for(userType.lower()))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')


@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('userType')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    #app.debug = True
    app.run('127.0.0.1', 5000)
