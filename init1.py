#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

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
@app.route('/register')
def register():
	return render_template('register.html')

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
	print(request.form)
	if request.method == 'POST':
		print(222)
		startDate = request.form.get('startDate')
		endDate = request.form['endDate']
		arr_airport = request.form['destination']
		print(request.form)
		if startDate != "" and endDate != "":
			if arr_airport != "":
				query = 'SELECT Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.email="%s" AND Flight.departure_date_time BETWEEN "%s" AND "%s" AND Flight.arrival_airport="%s"'
				cursor.execute(query % (username,startDate,endDate,arr_airport))
				data1 = cursor.fetchall()
			else:
				query = 'SELECT Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.email="%s" AND Flight.departure_date_time BETWEEN "%s" AND "%s"'
				cursor.execute(query % (username, startDate, endDate))
				data1 = cursor.fetchall()
		else:
			if arr_airport != "":
				query = 'SELECT Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.email="%s" AND Flight.arrival_airport="%s"'
				cursor.execute(query % (username, arr_airport))
				data1 = cursor.fetchall()
			else:
				query = 'SELECT Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.email="%s"'
				cursor.execute(query % (username))
				data1 = cursor.fetchall()
		cursor.close()
		return render_template('viewmyflights.html', records=data1)

	else:
		query = 'SELECT Flight.airline, Flight.flight_number, Flight.plane_ID, Flight.departure_date_time, Flight.departure_airport, Flight.arrival_date_time, Flight.arrival_airport, Flight.status FROM Ticket,Flight WHERE Ticket.flight_number=Flight.flight_number AND Ticket.email="%s"'
		cursor.execute(query %(username))
		data1 = cursor.fetchall()
		cursor.close()
		return render_template('viewmyflights.html', records=data1)

@app.route('/customer/searchflights', methods=['GET','POST'])
def searchflights():
	cursor = conn.cursor()
	oneway = True
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
			#print(session["Dcity1"])
			return render_template('searchflights.html', flights=data, oneway=oneway)
		elif LstartDate!="" and LendDate!="" and Dcity!="" and Acity!="" and RstartDate!="" and RendDate!="":
			oneway = False
			cursor.execute(query %(LstartDate, LendDate, Dcity, Acity))
			ldata = cursor.fetchall()
			cursor.execute(query % (RstartDate, RendDate, Acity, Dcity))
			rdata = cursor.fetchall()
			return render_template('searchflights.html',Lflights=ldata,Rflights=rdata,oneway=oneway)
	else:
		return render_template('searchflights.html')

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



@app.route('/Agent')
def Agent():
	return render_template('agent.html')

@app.route('/Staff')
def Staff():
	return render_template('staff.html')

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

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor()
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    #app.debug = True
    app.run('127.0.0.1', 5000)
