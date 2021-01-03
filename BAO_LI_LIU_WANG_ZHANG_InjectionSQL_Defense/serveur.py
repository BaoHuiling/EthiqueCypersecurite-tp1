 
import http.server, urllib.parse, sqlite3, threading, socketserver, requests, json, random

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

def config():

	config = "\
	<html>\n\
	<body>\n\
	<h1>Add a new sensor</h1> \n\
	<form action=\"http://localhost:8888/addsensor\" method=\"post\">\n\
	Sensor type id: <input type=\"text\" name=\"idTyCap\"><br>\n\
	Commercial reference: <input type=\"text\" name=\"RfComm\"><br>\n\
	Port: <input type=\"text\" name=\"Port\"><br>\n\
	<input type=\"submit\" value=\"submit\">\n\
	</form>\n\
	</body>\n\
	</html>\n\
	"
	return config


def fausse_donnee_alarm():

	fausse_donnee = '\
	<html>\n\
	<head>\n\
	<script language= "javascript" >\n\
		alert( "Please enter valid sensor type." );\n\
	</script>\n\
	</head>\n\
	</html>\n\
	'

	return fausse_donnee

def  addsucces():

	addsucces = '\
	<html>\n\
	<head>\n\
	<script language= "javascript" >\n\
		alert( "Add sensor successful!" );\n\
	</script>\n\
	</head>\n\
	</html>\n\
	'

	return addsucces


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
		if self.path == "/addsensor":
			q = self.rfile.read(int(self.headers['content-length'])).decode(encoding="utf-8")
			query = urllib.parse.parse_qs(q,keep_blank_values=1,encoding='utf-8')
			path = "/Capteur"

			# Défense contre fausse données
			val = ', '.join('%s' % it for it in query.values())
			val = val.split(",")
			id = val[0].split('\'')[1]
			selStr = "/Capteur/%s" % (id)
			res = self.mysql.select(selStr)

			if res:
				rep = self.mysql.insert(path, query)
		
			else:
				print("Insert error")
				rep = fausse_donnee_alarm()
				
			if len(rep) > 0:
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				self.wfile.write(bytes(str(rep)+'\n', 'UTF-8'))

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
		
		if(elem[1] == "Capteur"):
			req = "SELECT * FROM TypeCap WHERE id=%s" % (elem[2])
			print(req)
			return self.c.execute(req).fetchall()
		
		else:
			print("GET :URI format error")
		return self.c.execute(req).fetchall()
	
	def insert(self,path,query):
		attr = ', '.join(query.keys())
		val = ', '.join('"%s"' %v[0] for v in query.values())
		print(attr,val)
		req = "insert into %s (%s) values (%s)" %(path.split('/')[1], attr, val)
		print(req)
		self.c.execute(req)
		self.conn.commit()

		return addsucces()

	def check_login(self,path,query):
		name = "".join(query['user_name'])
		print(name)
		pwd = "".join(query["pwd"])
		print(pwd)

		# Défense en limitant le nombre de l'instruction

		req = 'SELECT pwd FROM Users WHERE user_name="%s";' % name		# Correction
		print(req)
		res = self.c.execute(req).fetchall()
		res = res[0][0]
		print(res)
		if (len(res) > 0) and (pwd == res):		# Correction
			return config()

		return hellopage_alarm()


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass

def serve_on_port(port):
	server = ThreadingHTTPServer(("localhost", port), MyHandler)
	server.serve_forever()

if __name__ == '__main__':


	# multi-thread
	threading.Thread(target=serve_on_port, args=[7777]).start()
	threading.Thread(target=serve_on_port, args=[8888]).start()
	threading.Thread(target=serve_on_port, args=[9999]).start()
	
	
