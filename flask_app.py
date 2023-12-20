import os
import shutil
from flask import Flask, render_template,url_for,redirect,send_file,session
from flask_session import Session
import datetime 
from flask import request, make_response
from flask_sqlalchemy import SQLAlchemy
import smtplib
import ssl
from email.message import EmailMessage

from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import zipfile
from io import BytesIO
import pdfkit
import sqlite3
import random
import json
from werkzeug.utils import secure_filename

from custom_funcs import create_invoice

conn = sqlite3.connect('church.db', check_same_thread=False)

c = conn.cursor()

# c.execute ("DROP TABLE members ")

# c.execute("""CREATE TABLE members (
# 				ID INTEGER PRIMARY KEY AUTOINCREMENT,
# 				first TEXT,
# 				last text,
# 				email text,
# 				password text,
# 				position text
# 				) """)

def insertMember(first, last, email, password, position):
	with conn:
		c.execute("INSERT INTO members VALUES (?,?,?,?,?,?)", 
			(None, first, last, email, password, position))

def getMember(email):
	c.execute("SELECT * FROM members WHERE email=:email", {'email':email})
	return c.fetchone()

def getAllMembers():
	c.execute("SELECT * FROM members ")
	return c.fetchall()


def getNumMembers():
	c.execute("SELECT COUNT(*) FROM members")
	return c.fetchone()[0]

def setMember(id, password):
    with conn:
        c.execute("""UPDATE members SET password =:password
                    WHERE id = :id """,
                  {'id': id, 'password': password})

def setMemberAll(id, first, last, email, password):

	with conn:
	        c.execute("""UPDATE members SET first=:first, last=:last, email=:email,password =:password
	                    WHERE id = :id """,
	                  {'id': id, 'first':first, 'last':last, 'email':email, 'password': password})


def deleteOneMember(id):
    with conn:
        c.execute("DELETE from members WHERE id = :id",
                  {'id': id})


# c.execute ("DROP TABLE entries ")

# c.execute("""CREATE TABLE entries (
# 				ID INTEGER PRIMARY KEY AUTOINCREMENT,
# 				category text,
# 				payment text,
# 				entry_date text,
# 				amount integer,
# 				author text,
# 				area text,
# 				local text,
# 				wd text,
# 				purpose text
# 				) """)

def insert_contribution(category, payment, date, amount, author, area, local, wd,purpose):
	with conn:
		c.execute("INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?)", 
			(None, category, payment, date, amount, author, area, local,wd,purpose))

def getEntries():
	c.execute("SELECT * FROM entries ORDER BY entry_date ASC ")
	return c.fetchall()

def getEntriesDate(start_date,end_date):
	c.execute("SELECT * FROM entries WHERE entry_date>:start_date AND entry_date<:end_date ORDER BY entry_date ASC ",
		{'start_date':start_date,'end_date':end_date})
	return c.fetchall()

def getAllEntries():
	c.execute("SELECT * FROM entries ORDER BY entry_date ASC ")
	return c.fetchall()

def getEntry(id):
	c.execute("SELECT * FROM entries WHERE id=:id", {'id':id})
	return c.fetchone()

def getEntriesArea(area):
	c.execute("SELECT * FROM entries WHERE area=:area ORDER BY entry_date ASC", {'area':area})
	return c.fetchall()

def getEntriesAreaDate(area,start_date,end_date):
	c.execute("SELECT * FROM entries WHERE area=:area AND entry_date>:start_date AND entry_date<:end_date ORDER BY entry_date ASC ",
		{'area':area,'start_date':start_date,'end_date':end_date})
	return c.fetchall()

def getEntriesAreaLocal(area, local):
	c.execute("SELECT * FROM entries WHERE area=:area AND local=:local ORDER BY entry_date ASC", {'area':area,'local':local})
	return c.fetchall()

def getEntriesAreaLocalDate(area, local,start_date,end_date):
	c.execute("SELECT * FROM entries WHERE area=:area AND local=:local AND entry_date>:start_date AND entry_date<:end_date ORDER BY entry_date ASC", 
		{'area':area,'local':local,'start_date':start_date,'end_date':end_date})
	return c.fetchall()


def set_Entry(id, category, payment, entry_date, amount):
    with conn:
        c.execute("""UPDATE entries SET category=:category,payment=:payment,entry_date=:entry_date,amount=:amount
                    WHERE id = :id """,
                  {'id': id, 'category':category,'payment':payment ,'entry_date':entry_date,'amount': amount })
def set_Entry_WithId(id,amount,purpose):
    with conn:
        c.execute("""UPDATE entries SET amount=:amount,purpose=:purpose 
                    WHERE id = :id """,
                  {'id': id, 'amount': amount ,'purpose':purpose})

def deleteEntry(id):
    with conn:
        c.execute("DELETE from entries WHERE id = :id",
                  {'id': id})



# c.execute ("DROP TABLE churches ")

# c.execute("""CREATE TABLE churches (
# 				ID INTEGER PRIMARY KEY AUTOINCREMENT,
# 				area text,
# 				local text,
# 				root text,
# 				account text,
# 				members integer
# 				) """)



def insert_churches(area, local, root, account, members):
	with conn:
		c.execute("INSERT INTO churches VALUES (?,?,?,?,?,?)", 
			(None, area, local,root,account,members))

def getChurchId(id):
	c.execute("SELECT * FROM churches WHERE id=:id", {'id':id})
	return c.fetchone()

def setChurchMembers(id, members):
    with conn:
        c.execute("""UPDATE churches SET members =:members
                    WHERE id = :id """,
                  {'id': id, 'members': members})

def setAccount(id, members):
    with conn:
        c.execute("""UPDATE churches SET members =:members
                    WHERE id = :id """,
                  {'id': id, 'members': members})

def getChurch(local):
	c.execute("SELECT * FROM churches WHERE local=:local", {"local":local})
	return c.fetchall()

def getAreaName(area):
	c.execute("SELECT * FROM churches WHERE area=:area", {"area":area})
	areas = c.fetchall()

	for a in areas:
		if a[3] == "2":
			return a 
	return None


def getAllChurches():
	root = "1"
	c = conn.cursor()
	c.execute("SELECT * FROM churches WHERE root=:root ORDER BY area", {"root":root})
	return c.fetchall()

def getAllChurchesAccount():
	root = "3"
	c = conn.cursor()
	c.execute("SELECT * FROM churches WHERE root=:root ORDER BY area", {"root":root})
	return c.fetchall()

def getAccountsForLocal(area, local):
	root = "3"
	c.execute("SELECT * FROM churches WHERE area=:area AND local=:local AND root=:root", {"area":area,"local":local,"root":root} )
	return c.fetchall()

def getLocals(area):
	root = "1"
	c.execute("SELECT * FROM churches WHERE area=:area AND root=:root ORDER BY local", {"area":area,"root":root} )
	return c.fetchall()

def getLocalChurches(area):
	root = "1"
	c.execute("SELECT * FROM churches WHERE area=:area AND root=:root ORDER BY local", {"area":area, "root":root})
	return c.fetchall()


def getAreaLocal(area, local):
	root = "1"
	c.execute("SELECT * FROM churches WHERE area=:area AND local=:local AND root=:root", {"area":area,"local":local,"root":root} )
	return c.fetchall()

def getAreaLocalCategory(area, local, account):
	
	c.execute("SELECT * FROM churches WHERE area=:area AND local=:local AND account=:account", {"area":area,"local":local,"account":account} )
	return c.fetchone()


def getAreas():
	root = "2"
	c.execute("SELECT * FROM churches WHERE root=:root", {"root":root})
	return c.fetchall()




# c.execute ("DROP TABLE applist ")

# c.execute("""CREATE TABLE applist (
# 				ID INTEGER PRIMARY KEY AUTOINCREMENT,
# 				root text,
# 				filename text,
# 				position integer
# 				) """)



def insertfilepath(root, filename, position):
	with conn:
		c.execute("INSERT INTO applist VALUES (?,?,?,?)", 
			(None, root, filename, position))

def getfilepath(id):
	c.execute("SELECT * FROM applist WHERE id=:id", {'id':id})
	return c.fetchone()

def renamefile(id, filename):
    with conn:
        c.execute("""UPDATE applist SET filename =:filename
                    WHERE id = :id """,
                  {'id': id, 'filename': filename})

def getFilesInPath(root):
	c.execute("SELECT * FROM applist WHERE root=:root ORDER BY position ASC", {"root":root})
	return c.fetchall()

def getMaxFilePosition(root):
	c.execute("SELECT * FROM applist WHERE root=:root ORDER BY position DESC LIMIT 1", {"root":root})
	return c.fetchall()

def getFileRootName(root, filename):
	c.execute("SELECT * FROM applist WHERE root=:root AND filename=:filename", {"root":root, "filename":filename})
	return c.fetchone()

def deleteFileEntry(id):
    with conn:
        c.execute("DELETE from applist WHERE id = :id",
                  {'id': id})


def send_email(email_receiver, password, reset):
	email_sender = 'napohreuben@gmail.com'
	email_password = 'cjcpmanegvncclqo'
	
	# Set the subject and body of the email
	subject = 'Welcome to Napoh Holdings Limited'
	body = """
	Your new account has been created.
	Username : """ + email_receiver + """
	Password : """ + password + """
	Below is the login url
	https://napoh.pythonanywhere.com/
	"""

	if reset == True:
		body = """
		Your new password is """ + password + """
		Below is the login url
		https://napoh.pythonanywhere.com/
		"""

	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)

	# Add SSL (layer of security)
	context = ssl.create_default_context()

	# Log in and send the email
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
	    smtp.login(email_sender, email_password)
	    smtp.sendmail(email_sender, email_receiver, em.as_string())





	

	
#insertMember("Arnel", "Serem", "arnelserem10@gmail.com", "000", "4")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = "static/documents"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://site.db'
db = SQLAlchemy(app)


@app.route("/")
def login():
	return render_template('login.html', error="")

@app.route("/login", methods=['GET', 'POST'])
def signin():
	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")
		val = getMember(email)
		if val == None:
			return redirect("/")
		if val[4] != password:
			return redirect("/")
		session["user"] = val

		return redirect("/dashboard")
 
		
	return render_template('login.html', error="")

@app.route("/logout")
def logout():
	session["user"] = None
	return redirect("/")

@app.route("/forgot", methods =["GET", "POST"])
def forgotPassword():
	
	email = request.args["email"]
	m = getMember(email)
	if m == None:
		return "not found"

	password  = str(random.randint(1111,9999))
		
	send_email(email, password, True)
	setMember(m[0], password)
	return "success"


@app.route("/dashboard")
def dashboard():
	if "user" not in session:
		session["user"] = None

	if session["user"] == None:
		return redirect("/")

	#Get churches
	chs = getAllChurches()
	summary = []
	summary.append(str(len(chs)))
	numMembers = getNumMembers()
	summary.append(str(numMembers-1))
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	areas = getAreas()
	companies = len(areas)
	if user[5] == "1":
		return render_template("dashboard.html", summary=summary, welcome=welcome, areas=areas,companies=companies,clearance=user[5])	
	return render_template("admin.html", summary=summary, welcome=welcome, areas=areas, companies=companies,clearance=user[5])



@app.route("/tempdf")
def tempdf():
	data = ['Napoh Holdings Limited', '+254 733 402 463', 'info@napohholdingsltd.co.ke', 'P.O Box 201', 'Nairobi, Kenya', '00100']
	chec = "Check mate"
	rendered = render_template('invoicepdf.html', data=data, chec=chec)
	
	return rendered


@app.route("/convertpdf")
def convertpdf():
	rendered = render_template('invoicepdf.html')
	css = ['static/bootstrap.min.css', 'static/invoicepdf.css']
	pdf = pdfkit.from_string(rendered, False, css=css)

	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

	return response 


@app.route("/invoice")
def Invoice():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	return render_template("Invoice.html",  welcome=welcome)

@app.route("/add_invoice", methods =["GET", "POST"])
def add_invoice():
	if request.method == "POST":
		company_name = request.form.get("name")
		address = request.form.get("box")
		city = request.form.get("city")
		postal = request.form.get("postal")
		invoice_number = request.form.get("invoice_number")
		issue_date = request.form.get("issue_date")
		due_date = request.form.get("due_date")

		array = request.form.get("array")
		data = []
		arr1 = array.split(',')
		for a in arr1:
			a1 = a.split('-')
			data.append(a1)

		# print(data)
		# filepath = "static/documents/Ian.pdf"
		filepath = create_invoice(company_name,address,city,postal,invoice_number,issue_date,due_date,data)

	return send_file(filepath, as_attachment=True)

@app.route("/invoicefilename", methods =["GET", "POST"])
def checkInvoiceFilename():
	name = request.args['name']
	files = os.listdir("static/documents/Invoices")
	name = name + '.pdf'
	for f in files:
		if f == name:
			return "False"

	return 'True'

@app.route('/zipapp', methods =["GET", "POST"])
def ZipApplication():
	path = request.form.get("root")
	apps = path.split('/')
	appName = apps[len(apps)-1]
	
	fileName = appName + ".zip"
	memory_file = BytesIO()
	file_path = "/" + path
	print(file_path) 
	with zipfile.ZipFile(memory_file,'w',zipfile.ZIP_DEFLATED) as zipf:
		files = os.listdir(path)
		for file in files:
				zipf.write(os.path.join(path, file), arcname=file)

		
	memory_file.seek(0)
	return send_file(memory_file, attachment_filename=fileName, as_attachment=True)



@app.route("/previewapp", methods =["GET", "POST"])
def preview_application():
	root = request.args["root"]
	files = getFilesInPath(root)
	pdf_writer = PdfFileWriter()
	apps = root.split('/')
	appName = apps[len(apps)-1]
	for file in files:
		path = file[1] + "/" + file[2]
		pdf_reader = PdfFileReader(path)
		for page in range(pdf_reader.getNumPages()):
			# Add each page to the writer object
			pdf_writer.addPage(pdf_reader.getPage(page))

	output = "static/Previews/" + appName + ".pdf"
	if os.path.exists(output):
		os.remove(path)

	with open(output, 'wb') as out:
		pdf_writer.write(out)

	
	return send_file(output, as_attachment=True)


@app.route("/storage")
def allDocs():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	root = "static/documents"
	try:
		doc = request.args["doc"]
		dir_list = os.listdir(doc)
		root = doc
	except Exception as e:
		dir_list = os.listdir("static/documents")  
	
	dirs = []
	files = []
	if root == "static/documents":
		dirs.append("Applications")
		dirs.append("Invoices")
		
	for d in dir_list:
		if ".pdf" in d:
			files.append(d)
		else:
			if d != "Applications" and d != "Invoices":
				dirs.append(d)

	nodes = root.split("/")
	paths = []
	pathNames = []
	curr = "static/documents"
	paths.append(curr)
	pathNames.append("Storage")
	for i,n in enumerate(nodes):
		if i > 1:
			curr = curr + "/" + n
			pathNames.append(n)
			paths.append(curr)
	
	temp = "static/documents/Applications"
	if temp != root and temp in root:
		files = getFilesInPath(root)
		befores = []
		afters = []
		prev = 0 
		post = 0 
		size = len(files)
		basePos = 1
		for i,f in enumerate(files):
			if i == 0:
				befores.append(int(f[3] - 100))
				basePos = f[3] + 100
				if i+1 < size:
					afters.append(int((f[3] + files[i+1][3])/2))
				else:
					afters.append(int(f[3] + 100))
			elif i + 1 == size:
				afters.append(int(f[3] + 100))
				basePos = f[3] + 100
				if i == 0:
					befores.append(int(f[3] - 100))
				else:
					befores.append(int((f[3] + files[i-1][3])/2))

			else:
				befores.append(int((f[3] + files[i-1][3])/2))
				afters.append(int((f[3] + files[i+1][3])/2))

		return render_template("docs.html",  welcome=welcome,root=root,packed=zip(paths, pathNames)
			,oz=1,data=zip(files, befores, afters), basePos=basePos)
	
	return render_template("docs.html",  welcome=welcome,  dirs=dirs, files=files, root=root, packed=zip(paths, pathNames),oz=0)

@app.route("/selectfile", methods =["GET", "POST"])
def selectFile():
	
	data = request.get_json()
	path = data['path']
	file = data['file']
	filename = data['filename']
	original = filename
	position = data['position']
	for i in range(21):
		if os.path.exists(path +"/" + filename):
			filename = str(i) + original
		else:
			break

	#os.rename(path +"/" + original, path +"/" + filename)
	shutil.copy(file, path + "/" + filename)

	# if os.path.exists(path +"/" + filename):
	# 	#os.rename(path +"/" + filename, path +"/*" + filename)
	# 	shutil.copy(file, path +"/_" + filename)
	# 	filename = "_" + filename
	# else:
	# 	shutil.copy(file, path)	

	insertfilepath(path, filename, int(position))
	return path

@app.route("/renderinvoice", methods =["GET", "POST"])
def renderinvoice():
	filename = request.args["name"]
	invoice = getInvoiceByName(filename)
	data = json.loads(invoice[2])

	return render_template("invoicepdf.html", data=data)

@app.route("/postinvoice", methods =["GET", "POST"])
def postinvoice():
	
	data = request.get_json()
	filename = data['filename'].strip()
	rendered = render_template('invoicepdf.html', data=data)
	css = ['static/invoicepdf.css', 'static/bootstrap.min.css']
	pdf = pdfkit.from_string(rendered, 'static/documents/Invoices/'+filename+'.pdf', css=css)
	
	return 'success'


@app.route("/uploadfile", methods =["GET", "POST"])
def uploadFile():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	 
	file = request.files['file']
	filename = secure_filename(file.filename)
	mypath = request.form.get("path")
	original = filename

	for i in range(1,21):
		if os.path.exists(mypath +"/" + filename):
			filename = str(i) + original
		else:
			break

	# path = mypath +"/" + filename
	# if os.path.exists(path):
	# 	filename = "1" + filename

	file.save(os.path.join(mypath, filename))
	return redirect("/storage?doc=" + mypath)	

@app.route("/checkfilename", methods =["GET", "POST"])
def checkfilename():
	path = request.args["path"]
	if os.path.exists(path):
		return 'false'
	return 'true'



@app.route("/renamefile", methods =["GET", "POST"])
def renameFile():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	newName = request.form.get("filename")
	root = request.form.get("root")
	prev = request.form.get("path")
	cat = request.form.get("cat")
	prevname = request.form.get("prevname")
	temp_root = root
	if cat == "file":
		root = root + "/" + newName + ".pdf"
	else:
		root = root + "/" + newName

	os.rename(prev, root)

	myfile = getFileRootName(temp_root, prevname)
	if myfile != None:
		renamefile(myfile[0], newName+".pdf")

	return redirect("/storage?doc="+temp_root)	


@app.route("/newfolder", methods =["GET", "POST"])
def newFolder():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	newDir = request.form.get("foldername")
	root = request.form.get("root")

	path = os.path.join(root, newDir)
	os.mkdir(path)
	return redirect("/storage?doc=" + root)	


@app.route("/deletefile", methods =["GET", "POST"])
def deleteFile():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	path = request.args["name"]
	root = request.args["root"]
	if os.path.exists(path):
		os.remove(path)

	if 'file' not in request.args.keys():
		return redirect("/storage?doc="+root)			
	
	file = request.args["file"]
	myfile = getFileRootName(root, file)
	if myfile != None:		
		deleteFileEntry(myfile[0])

	return redirect("/storage?doc="+root)	

@app.route("/deletefolder", methods =["GET", "POST"])
def deleteFolder():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	path = request.args["name"]
	root = request.args["root"]
	os.rmdir(path)
	return redirect("/storage?doc="+root)	


@app.route("//allProjects")
def allchurchesfunc():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	areas = getAreas()
	churchs = getAllChurches()
	accounts = getAllChurchesAccount()
	balances = []
	for acc in accounts:
		balances.append(f"{acc[5]:,}")
	print(balances)
	user = session["user"]
	status = user[5]
	welcome = "Welcome, " + user[1] + " " + user[2]
	return render_template("churches.html", churchs=churchs, status=status, welcome=welcome, areas=areas,balances=balances)


@app.route("/filterchurches", methods =["GET", "POST"])
def filterchurches():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	if area == "":
		churchs = getAllChurches()
	else:
		churchs = getLocalChurches(area)

	return json.dumps(churchs)


@app.route("/filterbillings", methods =["GET", "POST"])
def filterbillings():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	date = request.args["date"]
	start = "2023-" + date + "-00";
	end = "2023-" + date + "-32";
	if area == "":
		if date == "" or date == None:
			ents = getEntries()
		else:	
			ents = getEntriesDate(start,end)
	else:
		if date == "" or date == None:
			ents = getEntriesArea(area)
		else:	
			ents = getEntriesAreaDate(area,start,end)

	return json.dumps(ents)

@app.route("/getFiles")
def getFilesData():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	root = "static/documents"
	try:
		doc = request.args["doc"]
		dir_list = os.listdir(doc)
		root = doc
	except Exception as e:
		dir_list = os.listdir("static/documents")  
	
	dirs = []
	files = []
	if root == "static/documents":
		dirs.append("Applications")
		dirs.append("Invoices")
		
	for d in dir_list:
		if ".pdf" in d:
			files.append(d)
		else:
			if d != "Applications" and d != "Invoices":
				dirs.append(d)

	nodes = root.split("/")
	paths = []
	pathNames = []
	curr = "static/documents"
	paths.append(curr)
	pathNames.append("Storage")
	for i,n in enumerate(nodes):
		if i > 1:
			curr = curr + "/" + n
			pathNames.append(n)
			paths.append(curr)
	
	data = {}
	data['dirs'] = dirs 
	data['files'] = files 
	data['root'] = root
	return json.dumps(data)
	

@app.route("/filterbillingslocal", methods =["GET", "POST"])
def filterbillingslocal():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	local = request.args["local"]
	date = request.args["date"]
	start = "2023-" + date + "-00";
	end = "2023-" + date + "-32";
	
	if area == "":
		ents = getEntries()
	else:
		if date == "" or date == None:
			ents = getEntriesAreaLocal(area, local)
		else:
			ents = getEntriesAreaLocalDate(area, local, start, end)

	return json.dumps(ents)

@app.route("/setMembers", methods =["GET", "POST"])
def setMembers():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	churchId = request.args["id"]
	newVal = request.args["val"]
	church = getChurchId(int(churchId))
	if church == None:
		return "failed"
	setChurchMembers(int(churchId), int(newVal))
	
	return "success"




@app.route("/billing")
def billing():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	contributions = getEntries()
	amounts = []
	total = 0
	for c in contributions:
		curr = c[4]
		if c[8] == "Withdraw":
			curr = curr *-1
		amounts.append(f"{curr:,}")
		total = total + curr
	user = session["user"]
	status = user[5]
	areas = getAreas()
	welcome = "Welcome, " + user[1] + " " + user[2]
	return render_template("entries.html", contributions=contributions, total=f"{total:,}", status=status, welcome=welcome, areas=areas, amounts=amounts)

@app.route("/addDirector")
def addMember():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	directors = getAllMembers()
	return render_template("member.html", error="", welcome=welcome, directors = directors,clearance=user[5])


@app.route("/summary")
def summary():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	summary = getAllSummary()
	return render_template("summary.html", error="", summary=summary, welcome=welcome, user=user)

@app.route("/editSummary", methods =["GET", "POST"])
def editSummary():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		branches = request.form.get("branches")
		events = request.form.get("events")
		members = request.form.get("members")
		val = getSummary("Branches")
		set_Summary(val[0], int(branches))
		val = getSummary("Events")
		set_Summary(val[0], int(events))
		val = getSummary("Members")
		set_Summary(val[0], int(members))


		return redirect("/dashboard")
	return redirect("/dashboard")


@app.route("/findLocals", methods =["GET", "POST"])
def findLocals():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	locs = getLocals(area)
	st = ""
	for l in locs:
		if l[3] == "1":
			st = st + l[2] + ","


	return st

@app.route("/findAccounts", methods =["GET", "POST"])
def findAccounts():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	local = request.args["local"]
	accounts = getAccountsForLocal(area, local)

	st = ""
	for acc in accounts:
		st = st + acc[4] + " - " + str(acc[5]) + ","

	return st


@app.route("/sortarea", methods =["GET", "POST"])
def sortarea():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	locs = getLocals(area)
	category = {1:0,2:0,3:0,4:0}
	for p in locs:
		if p[5] in category:
			category[p[5]] = category[p[5]] + 1
	result = {}
	members = 0 
	branches = 0
	for l in locs:
		members = members + l[5]
		branches = branches + 1
		
	months = {'01':None,'02':None, '03':None,'04':None,'05':None,'06':None,'07':None,'08':None,'09':None,'10':None,'11':None,'12':None}
		
	#months = {'01':0,'02':0, '03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'09':0,'10':0,'11':0,'12':0}
	conts = getEntriesArea(area)
	total = 0
	end = None
	start = None
	if len(conts) > 0:
		start = conts[0][3][5:7]
	for c in conts:
		date = c[3]
		key = date[5:7]
		amount = c[4]
		if c[8] == "Withdraw":
			amount = amount * -1
		total = total + amount
		cat = c[1]
		if months[key] == None:
			months[key] = total
			end = key
		else:
			months[key] = months[key] + amount
		
		

	prev = 0
	for key, value in months.items():
		if start != None:
			if value == None:
				months[key] = prev
			prev = months[key]
		else:
			if value == None:
				months[key] = 0
	if end == None:
		end = ""
	
		
	result['branches'] = branches
	result['members'] = members
	result['total'] = total
	result["months"] = months
	result['categories'] = category
	result["end"] = end
	
	return json.dumps(result)

@app.route("/sortlocal", methods =["GET", "POST"])
def sortlocal():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	area = request.args["area"]
	local = request.args["local"]
	locs = getAreaLocal(area, local)
	category = {1:0,2:0,3:0,4:0}
	for p in locs:
		if p[5] in category:
			category[p[5]] = category[p[5]] + 1
	result = {}
	members = 0 
	branches = 0
	for l in locs:
		members = members + l[5]
		branches = branches + 1
		
	months = {'01':None,'02':None, '03':None,'04':None,'05':None,'06':None,'07':None,'08':None,'09':None,'10':None,'11':None,'12':None}
		
	#months = {'01':0,'02':0, '03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'09':0,'10':0,'11':0,'12':0}
	conts = getEntriesAreaLocal(area, local)
	total = 0
	end = None
	start = None
	if len(conts) > 0:
		start = conts[0][3][5:7]
	for c in conts:
		date = c[3]
		key = date[5:7]
		amount = c[4]
		if c[8] == "Withdraw":
			amount = amount * -1
		total = total + amount
		cat = c[1]
		if months[key] == None:
			months[key] = total
			end = key
		else:
			months[key] = months[key] + amount
		
		

	prev = 0
	for key, value in months.items():
		if start != None:
			if value == None:
				months[key] = prev
			prev = months[key]
		else:
			if value == None:
				months[key] = 0
	if end == None:
		end = ""
		


	result['branches'] = branches
	result['members'] = members
	result['total'] = total
	result["months"] = months
	result['categories'] = category
	result["end"] = end

	return json.dumps(result)

@app.route("/allChurch")
def allChurch():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	return str(getAllChurches())


@app.route("/addAccount")
def addAccount():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	areas = getAreas()
	return render_template("addAccount.html", error="", welcome=welcome, user=user, areas=areas)

@app.route("/createAccount", methods =["GET", "POST"])
def createAccount():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		area = request.form.get("area")
		local = request.form.get("local")
		name = request.form.get("name")
		if area == "" or local == "":
			areas = getAreas()
			return render_template("addAccount.html", error="*Enter all fields", areas=areas)
		insert_churches(area, local, "3",name, 0)
		

		return redirect("/dashboard")
	return redirect("/dashboard")


@app.route("/addProject")
def addChurch():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	areas = getAreas()
	return render_template("addChurch.html", error="", welcome=welcome, user=user, areas=areas)

@app.route("/createProject", methods =["GET", "POST"])
def createChurch():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		area = request.form.get("area")
		newArea = request.form.get("newArea")
		local = request.form.get("local")
		members = int(request.form.get("members"))
		if area == "" or local == "":
			areas = getAreas()
			return render_template("addChurch.html", error="*Enter all fields", areas=areas)

		if area == "Other" and newArea == "":
			areas = getAreas()
			return render_template("addChurch.html", error="*Enter all fields", areas=areas)

		if area == "Other":
			area = newArea
		val = getAreaName(area)
		if val == None:
			insert_churches(area, area,"2","",0)

		val = getChurch(local)
		for v in val:
			if area == v[1] and v[3] == "1":
				areas = getAreas()
				return render_template("addChurch.html", error="*church name already exists", areas=areas)
		
		insert_churches(area, local, "1","",members)
		insert_churches(area, local, "3","primary", 0)
		

		return redirect("/dashboard")
	return redirect("/dashboard")


@app.route("/profile")
def profile():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	return render_template("profile.html", error="", welcome=welcome, user=user)


@app.route("/deleteMember", methods =["GET", "POST"])
def deleteMember():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	email = request.args["email"]
	m = getMember(email)
	deleteOneMember(m[0])

	return redirect("/addDirector")


@app.route("/createMember", methods =["GET", "POST"])
def createMember():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		first = request.form.get("first_name")
		last = request.form.get("second_name")
		email = request.form.get("email")
		clearance = request.form.get("clearance")
		val = getMember(email)
		user = session["user"]
		welcome = "Welcome, " + user[1] + " " + user[2]
		if val != None:
			directors = getAllMembers()
			return render_template("member.html", error="*Use a different email", welcome=welcome, directors = directors)
			
		password  = str(random.randint(1111,9999))

		send_email(email, password, False)
		insertMember(first, last, email, password, clearance)
		directors = getAllMembers()
		return render_template("member.html", error="", welcome=welcome, directors = directors)
			
	return redirect("/dashboard")

@app.route("/editMember", methods =["GET", "POST"])
def editMember():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		first = request.form.get("first_name")
		last = request.form.get("second_name")
		email = request.form.get("email")
		password = request.form.get("password")
		user = session["user"]
		val = getMember(user[3])
		if val == None:
			return render_template("member.html", error="*Use a different email")

		
		setMemberAll(val[0],first, last, email,password)
		val = getMember(email)
		session["user"] = val
		return redirect("/dashboard")
	return redirect("/dashboard")

@app.route("/withdraw")
def withdrawFunds():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	entry = (0,'0','0','0',0,'0')
	areas = getAreas()
	return render_template("withdraw.html", entry=entry, welcome=welcome,areas=areas, user=user)


@app.route("/deposit")
def addContribution():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	entry = (0,'0','0','0',0,'0')
	areas = getAreas()
	return render_template("addContribution.html", entry=entry, welcome=welcome,areas=areas, user=user)

@app.route("/editContribution")
def editContribution():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")
	user = session["user"]
	welcome = "Welcome, " + user[1] + " " + user[2]
	id = request.args["id"]
	entry = getEntry(int(id))
	return render_template("addContribution.html", entry=entry,welcome=welcome, user=user)	


@app.route("/submitContribution", methods =["GET", "POST"])
def submitContribution():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		category = "primary"
		payment = request.form.get("payment")
		date = request.form.get("date")
		amount = request.form.get("amount")
		area = request.form.get("area")
		local = request.form.get("local")
		wd = request.form.get("wd")
		purpose = request.form.get("purpose")
		author = request.form.get("email")
		if author == None or payment == None or author == None or amount == None or date == None or area == None:
			return redirect("/dashboard")	
		insert_contribution(category, payment, date, int(amount), author, area, local,wd,purpose)
		account = getAreaLocalCategory(area, local, category)
		val = int(amount)
		if wd == "Withdraw":
			val = val * -1
		setAccount(account[0],val + account[5])
		# update_monthly(category, date, int(amount))
		# updateSummary(category, int(amount))
		return redirect("/dashboard")
	return redirect("/dashboard")

@app.route("/setAccount", methods =["GET", "POST"])
def setAccountPay():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	accountId = request.args["id"]
	newVal = request.args["val"]
	desc = request.args["desc"]

	entry = getEntry(int(accountId))
	if entry == None:
		return "failed"
	set_Entry_WithId(entry[0], int(newVal), desc)
	account = getAreaLocalCategory(entry[6], entry[7], entry[1])

	val = int(newVal) - entry[4]
	if entry[8] == "Withdraw":
		val = val*-1
	setAccount(account[0], val + account[5])
		
			
	return "success"


@app.route("/changeContribution", methods =["GET", "POST"])
def changeContribution():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	if request.method == "POST":
		category = request.form.get("category")
		payment = request.form.get("payment")
		date = request.form.get("date")
		amount = request.form.get("amount")
		author = request.form.get("email")
		id = request.form.get("entry_id")
		entry = getEntry(int(id))
		pre_category = entry[1]
		pre_date = entry[3]
		pre_amount = entry[4]
		update_monthly(pre_category, pre_date, pre_amount*-1)
		updateSummary(pre_category, pre_amount*-1)
		
		set_Entry(entry[0], category,payment,date, int(amount))
		update_monthly(category, date, int(amount))
		updateSummary(category, int(amount))
		return redirect("/billing")
	return redirect("/billing")

@app.route("/deleteEntry", methods =["GET", "POST"])
def deleteContribution():
	if "user" not in session:
		session["user"] = None
	
	if session["user"] == None:
		return redirect("/")

	id = request.args["id"]
	entry = getEntry(int(id))
	if entry == None:
		return redirect("/billing")

	deleteEntry(entry[0])
	account = getAreaLocalCategory(entry[6], entry[7], entry[1])
	val = entry[4]
	if entry[8] == "Withdraw":
		val = val*-1
	setAccount(account[0], account[5] - val)
	return redirect("/billing")

	

@app.route("/getData", methods =["GET", "POST"])
def getData():
	if request.method == "GET": 
		result = {}
	
		months = {'01':None,'02':None, '03':None,'04':None,'05':None,'06':None,'07':None,'08':None,'09':None,'10':None,'11':None,'12':None}
		#Ongoing Pending Completed Archives
		category = {1:0,2:0,3:0,4:0}
		projects = getAllChurches()
		for p in projects:
			if p[5] in category:
				category[p[5]] = category[p[5]] + 1

		conts = getAllEntries()
		total = 0
		end = None
		start = None
		if len(conts) > 0:
			start = conts[0][3][5:7]
		for c in conts:
			date = c[3]
			key = date[5:7]
			amount = c[4]
			if c[8] == "Withdraw":
				amount = amount * -1
			total = total + amount
			
			if months[key] == None:
				months[key] = total
				end = key
			else:
				months[key] = months[key] + amount
			
			
		prev = 0
		for key, value in months.items():
			if start != None:
				if value == None:
					months[key] = prev
				prev = months[key]
			else:
				if value == None:
					months[key] = 0
		if end == None:
			end = ""
		
		result['categories'] = category
		result["months"] = months
		result["total"] = total
		result["end"] = end
		return json.dumps(result)
	 
		# out = ""
		# year = getMonthlies("98")
		# for y in year:
		# 	out = out + str(y[3]) + ","
		# return out[:-1]
	return "trouble"

@app.route("/getSummary", methods =["GET", "POST"])
def giveSummary():
	if request.method == "GET": 
		out = ""
		val = getSummary("Offerings")
		out = out + str(val[2])
		val = getSummary("Mavuno")
		out = out + "," + str(val[2])
		val = getSummary("Tithes")
		out = out + "," + str(val[2])
		val = getSummary("Fund-Raising")
		out = out + "," + str(val[2]) + ",4000"
		return out
	return "error on request type"


if __name__ == '__main__':
	app.run(debug=True)