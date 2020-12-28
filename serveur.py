#curl -X GET http://localhost:8888/chart pour afficher le chart de Facture
#curl -X GET http://localhost:8888/meteo  
import http.server, urllib.parse, sqlite3, threading, socketserver, requests, json, random

def meteo():
	cs_url  = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=554632cfaef8c83ef4f1f5aec5fbe697'
	r = requests.get(cs_url)
	# d_text = json.loads(text)
	return r.json()

# TODO
def hellopage():

	hellopage = hellopage = '''
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <title>Login</title>  
	<style>
		html{   
    width: 100%;   
    height: 100%;   
    overflow: hidden;   
    font-style: sans-serif;   
}   
body{   
    width: 100%;   
    height: 100%;   
    font-family: 'Open Sans',sans-serif;   
    margin: 0;   
    background-color: #4A374A;   
}   
#login{   
    position: absolute;   
    top: 50%;   
    left:50%;   
    margin: -150px 0 0 -150px;   
    width: 300px;   
    height: 300px;   
}   
#login h1{   
    color: #fff;   
    text-shadow:0 0 10px;   
    letter-spacing: 1px;   
    text-align: center;   
}   
h1{   
    font-size: 2em;   
    margin: 0.67em 0;   
}   
h2
{
	color:white;
	text-align:center;
}
input{   
    width: 278px;   
    height: 18px;   
    margin-bottom: 10px;   
    outline: none;   
    padding: 10px;   
    font-size: 13px;   
    color: #fff;   
    text-shadow:1px 1px 1px;   
    border-top: 1px solid #312E3D;   
    border-left: 1px solid #312E3D;   
    border-right: 1px solid #312E3D;   
    border-bottom: 1px solid #56536A;   
    border-radius: 4px;   
    background-color: #2D2D3F;   
}   
.but{   
    width: 300px;   
    min-height: 20px;   
    display: block;   
    background-color: #4a77d4;   
    border: 1px solid #3762bc;   
    color: #fff;   
    padding: 9px 14px;   
    font-size: 15px;   
    line-height: normal;   
    border-radius: 5px;   
    margin: 0;   
}  
	</style>
</head>  
<body>  
    <div id="login">  
        <h1>Login</h1>  
		<h2>For SQL Injection Test</h2>
        <form action="http://localhost:8888/login" method="post">  
            <input type="text" required="required" placeholder="Username" name="user_name"></input>  
            <input type="password" required="required" placeholder="Password" name="pwd"></input>  
            <button class="but" type="submit">Go!</button>  
        </form>  
    </div>  
</body>  
</html> 
	'''
	return hellopage

def hellopage_alarm():

	hellopage = '\
	<html>\n\
	<body>\n\
	<p>Please enter valid user name or password</p> \n\
		<p><a href="http://localhost:8888/"></a></p>\n\
		<button onclick="myFunction()">Go back</button>\n\
	<script>\n\
		function myFunction() {\
		  window.location.href="http://localhost:8888/";\
		}\n\
	</script>\n\
	</body>\n\
	</html>\n\
	'

	return hellopage


def menu():

	menu = "<html> \n\
					<body>\n\
					<h1>Welcome!</h1> \n\
					<h3>Choose the fonction: </h3>\n\
					<p><a href=\"http://localhost:8888/chart\">See the consumption</a></p>\n\
					<p><a href=\"http://localhost:8888/mesure\">Check the status of the sensors / actuators</a></p>\n\
					<p><a href=\"http://localhost:8888/save\">See the savings achieved</a></p>\n\
					<p><a href=\"http://localhost:8888/config\">Configuration</a></p>\n\
				</body>\n\
				</html>\n"
	return menu

def make_chart(facture):
	elec=[]
	eau=[]
	chauffage=[]
	dechet=[]
	autre=[]
	fac=" "
	for row in facture:
		if row[2]=="electricite":
			elec.append(row[4])
		elif row[2]=="eau":
			eau.append(row[4])
		elif row[2]=="chauffage":
			chauffage.append(row[4])
		elif row[2]=="dechet":
			dechet.append(row[4])
		else:
			autre.append(row[4])

	#lenmax = max(len(elec), len(eau), len(chauffage), len(dechet), len(autre))
	lenmax = 5;
	for i in range(lenmax):
		col = "[%s,%s,%s,%s,%s,%s]" %(i+1,elec[i],eau[i],chauffage[i],dechet[i],autre[i])
		fac += col;
		if(i<lenmax-1):
			fac+=","

	chart = "\
	  <html>\n\
  		<head>\n\
    		<script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>\n\
    		<script type=\"text/javascript\">\n\
      		google.charts.load('current', {'packages':['corechart']});\n\
	      google.charts.setOnLoadCallback(drawChart);\n\
	      function drawChart() {\n\
	        var data = google.visualization.arrayToDataTable([\
	          ['number', 'Electricity', 'Water', 'Warm gas', 'Garbage','Else'],%s]);\n\
	        var options = {\
	          title: 'Consumption of residence in euro (EUR)',\
	          curveType: 'function',\
	          legend: { position: 'bottom' }\
	        };\n\
	        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));\n\
	        chart.draw(data, options);\n\
	      }\n\
	    </script>\n\
	  </head>\n\
	  <body>\n\
	    <div id=\"curve_chart\" style=\"width: 900px; height: 500px\"></div>\n\
	  </body>\n\
	</html>" %(fac)
	
	return chart

def config():

	config = "\
	<html>\n\
	<body>\n\
	<h1>Add a new sensor</h1> \n\
	<form action=\"index.html\" method=\"post\">\n\
	Sensor type id: <input type=\"text\" name=\"idTyCap\"><br>\n\
	Commercial reference: <input type=\"text\" name=\"RfComm\"><br>\n\
	Port: <input type=\"text\" name=\"Port\"><br>\n\
	<input type=\"submit\" value=\"submit\">\n\
	</form>\n\
	</body>\n\
	</html>\n\
	"
	return config

def mesure(self,mes):
	
	m = ""
	length = len(mes)
	i=1
	for row in mes:
		
		req = "select idTyCap from Capteur where id=%s" %(row[1])
		idTyCap = self.c.execute(req).fetchall()
		req = "select Type from TypeCap where id=%s" %(idTyCap[0][0])
		typet = self.c.execute(req).fetchall()
		Type = typet[0][0]

		m += "[%s,\'%s\',%s,\'%s\']" %(row[1],Type,row[2],row[3])
		if(i<length):
			m += ","
		i=i+1

	print (m)
	mesure = "<html>\n\
  <head>\n\
    <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>\n\
    <script type=\"text/javascript\">\n\
      google.charts.load('current', {'packages':['table']});\n\
      google.charts.setOnLoadCallback(drawTable);\n\
      function drawTable() {\
        var data = new google.visualization.DataTable();\n\
        data.addColumn('number', 'Capture');\n\
        data.addColumn('string', 'Type');\n\
        data.addColumn('number', 'Value');\n\
        data.addColumn('string', 'Time');\n\
        data.addRows([%s]);\n\
        var table = new google.visualization.Table(document.getElementById('table_div'));\n\
        table.draw(data,{showRowNumber: true, width: '900px', height: '500px'});\n\
      }\n\
    </script>\n\
  </head>\n\
  <body>\n\
    <div id=\"table_div\"></div>\"\"\n\
  </body>\n\
</html>\n" %(m)
	print(mesure)
	return mesure

def save(facture):
	elec=[]
	eau=[]
	chauffage=[]
	dechet=[]
	autre=[]
	fac=""
	for row in facture:
		if row[2]=="electricite":
			elec.append(row[4])
		elif row[2]=="eau":
			eau.append(row[4])
		elif row[2]=="chauffage":
			chauffage.append(row[4])
		elif row[2]=="dechet":
			dechet.append(row[4])
		else:
			autre.append(row[4])

	#lenmax = max(len(elec), len(eau), len(chauffage), len(dechet), len(autre))
	lenmax = 5;
	for i in range(lenmax):
		som = elec[i]+eau[i]+chauffage[i]+dechet[i]+autre[i]
		col = "[%s,%s,%s]" %(i+1,som-random.randint(15,50),som) #random pour simuler la valeur original(unconnu)
		fac += col;
		if(i<lenmax-1):
			fac+=","

	chart ='''<html>\n\

  <head>\n\
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n\
    <script type="text/javascript">\n\
      google.charts.load('current', {'packages':['corechart']});\n\
      google.charts.setOnLoadCallback(drawChart);\n\
      function drawChart() {\
        var data = google.visualization.arrayToDataTable([\
          ['time', 'original', 'eco-responsable'],\
          %s]);\n\
        var options = {\
          title: 'Comparaison of orginal consumption and eco-responsable',\
          hAxis: {title: 'time',  titleTextStyle: {color: '#333'}},\
          vAxis: {minValue: 0}\
        };\n\
        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));\n\
        chart.draw(data, options);\n\
      }\n\
    </script>\n\
  </head>\n\
  <body>\n\
    <div id="chart_div" style="width: 900px; height: 500px;"></div>\n\
  </body>\n\
</html>\n''' %(fac)
	print(chart)
	return chart


class MyHandler(http.server.BaseHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		self.mysql = MySQL('logement.db')
		super(MyHandler, self).__init__(*args, **kwargs)

	def do_GET(self):
		"""Respond to a GET request."""
		if self.path == '/favicon.ico':
			return 
		if self.path == '/':    #localhost:8888/
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			html  = hellopage()
			self.wfile.write(bytes(str(html)+'\n', 'UTF-8'))
		else:
			res = urllib.parse.urlparse(self.path)
			rep = self.mysql.select(res.path)
			if len(rep) > 0:
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))
			else:
				self.send_response(404)
				self.send_header("Content-type", "text/html")
				self.end_headers()
		
	def do_POST(self):
		"""Respond to a POST request."""
		print("POST" + self.path)
		if self.path == "/index.html":
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			path = "/Capteur"
			val = ', '.join('%s' % it for it in query.values())
			val = val.split(",")
			id = val[0].split('\'')[1]
			selStr = "/Capteur/%s" % (id)
			res = self.mysql.select(selStr)
			if res:
				rep = self.mysql.insert(path, query)
			else:
				print("Insert error")
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
		elif self.path == "/login":
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			
			rep = self.mysql.check_login(self.path,query)

			if len(rep) > 0:
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))

		else:
			res = urllib.parse.urlparse(self.path)
			path = res.path
			query = urllib.parse.parse_qs(res.query)
			rep = self.mysql.insert(path,query)
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()

class MySQL():
	def __init__(self, name):
		self.c = None
		self.req = None
		self.conn = sqlite3.connect(name,check_same_thread=False)
		self.c = self.conn.cursor()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

	def select(self,path):
		elem = path.split('/')
		req = None
		if(elem[1]=="chart"):
			print("chart part")
			req = "select * from Facture"
			facture = self.c.execute(req).fetchall()
			return make_chart(facture)
		if(elem[1]=="meteo"):
			print("meteo request")
			return meteo()
		# if(elem[1]=="config"):
		# 	print("config request")
		# 	return config()
		if(elem[1]=="mesure"):
			print("mesure request")
			req = "select * from Mesure"
			mes = self.c.execute(req).fetchall()
			return mesure(self,mes)
		if(elem[1]=="save"):
			print("save request")
			req = "select * from Facture"
			fac = self.c.execute(req).fetchall()
			return save(fac)
		if(elem[1] == "Capteur"):
			req = "SELECT * FROM TypeCap WHERE id=%s" % (elem[2])
			print(req)
			return self.c.execute(req).fetchall()
		# elif len(elem) == 2:
		# 	req = "select * from %s" %(elem[1])
		# elif len(elem) == 3:
		# 	req = "select * from %s where id=%s" %(elem[1],elem[2])
		# elif len(elem) == 4:
		# 	req = "select %s from %s where id=%s" %(elem[3],elem[1],elem[2])
		# elif len(elem) == 5:
		# 	req = "select %s from %s where %s=%s" %(elem[4],elem[1],elem[2],elem[3])
		else:
			print("GET :URI format error")
		return self.c.execute(req).fetchall()
	
	def insert(self,path,query):
		attr = ', '.join(query.keys())
		val = ', '.join('"%s"' %v[0] for v in query.values())
		print(attr,val)
		req = "insert into %s (%s) values (%s)" %(path.split('/')[1], attr, val)
		print(req)
		self.c.executescript(req)
		self.conn.commit()
		return 1

	def check_login(self,path,query):
		name = "".join(query['user_name'])
		print(name)
		pwd = "".join(query["pwd"])
		print(pwd)
		# req = 'SELECT * FROM Users WHERE user_name="%s" AND pwd="%s";' % (name, pwd)		# Can be skipped
		req = 'SELECT pwd FROM Users WHERE user_name="%s";' % name		# Correction
		print(req)
		res = self.c.execute(req).fetchall()
		res = res[0][0]
		print(res)
		# if res:	# Can be skipped
		if (len(res) > 0) and (pwd == res):		# Correction
			return config()

		return hellopage_alarm()


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass

def serve_on_port(port):
	server = ThreadingHTTPServer(("localhost", port), MyHandler)
	server.serve_forever()

if __name__ == '__main__':
	# mono thread
	# server_class = http.server.HTTPServer
	# httpd = server_class(("localhost", 8888), MyHandler)
	#try:
		#httpd.serve_forever()
	#except KeyboardInterrupt:
		#pass
	#httpd.server_close()

	# multi-thread
	threading.Thread(target=serve_on_port, args=[7777]).start()
	threading.Thread(target=serve_on_port, args=[8888]).start()
	threading.Thread(target=serve_on_port, args=[9999]).start()
	
	
