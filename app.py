import os
import datetime
import shutil
from flask import*
from flask import render_template

app = Flask(__name__, static_folder="static", template_folder="temp")
app.config["SERVER_NAME"] = "localhost:5000"

def rndm():
	return str(datetime.datetime.now()).replace("-","").replace(".","").replace(" ","").replace(":","")

@app.route("/", methods=["GET","POST"])
def index():
	return render_template("index.html")

@app.route("/", subdomain="<sdm>", methods=["GET","POST"])
def subdomain_index(sdm):
	if (request.method == "GET"):
		if (sdm not in os.listdir("accounts")):
			return redirect("/404")
		else:
			w = [open("accounts/"+sdm+"/name.txt","r").read(),open("accounts/"+sdm+"/template/template_no.txt","r").read(),open("accounts/"+sdm+"/template/description.txt","r").read()]
			mk = int(open("accounts/"+sdm+"/views.txt","r").read())+1
			open("accounts/"+sdm+"/views.txt","w").write(str(mk))
			return render_template("select/"+w[1]+".html", name=w[0], description=w[2])
	else:
		if (sdm not in os.listdir("accounts")):
			return redirect("/404")
		else:
			w = [open("accounts/"+sdm+"/name.txt","r").read(),open("accounts/"+sdm+"/template/template_no.txt","r").read(),open("accounts/"+sdm+"/template/description.txt","r").read()]
			mk = int(open("accounts/"+sdm+"/views.txt","r").read())+1
			open("accounts/"+sdm+"/views.txt","w").write(str(mk))
			t = [request.form["name"], request.form["email"], request.form["message"]]
			k = rndm()
			open("accounts/"+sdm+"/contacts/"+k+".txt","w").write(f"Name: {w[0]}\nEmail: {w[1]}\nMessage: {w[2]}")
			return render_template("select/"+w[1]+".html", name=w[0], description=w[2])

@app.route("/signup", methods=["GET","POST"])
def signup():
	if (request.method == "POST"):
		e = [request.form["username"], request.form["password"], request.form["name"]]
		if (e[0] in os.listdir("accounts")):
			return render_template("signup.html", error="Account already exists!")
		else:
			os.mkdir("accounts/"+e[0])
			os.mkdir("accounts/"+e[0]+"/template")
			os.mkdir("accounts/"+e[0]+"/contacts")
			open("accounts/"+e[0]+"/name.txt","a").write(e[2])
			open("accounts/"+e[0]+"/password.txt","a").write(e[1])
			open("accounts/"+e[0]+"/views.txt","a").write("0")
			open("accounts/"+e[0]+"/template/template_no.txt","a").write("Classic")
			open("accounts/"+e[0]+"/template/description.txt","a").write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex. Etiam volutpat laoreet urna. Morbi ut tortor nec nulla commodo malesuada sit amet vel lacus. Fusce eget efficitur libero. Morbi dapibus porta quam laoreet placerat. Donec eu vehicula neque. Donec viverra lorem nunc, tempus euismod eros sollicitudin ut. Quisque et tincidunt libero. Donec id pharetra justo. Proin euismod lacinia dolor, eu scelerisque justo tempus pharetra. Vivamus nunc justo, finibus ut nisl sed, euismod rhoncus nulla. Proin sed magna egestas, egestas ante et, congue eros. In consequat, mauris dapibus tincidunt suscipit, ex libero aliquet diam, at maximus risus enim non leo.")
			ctn=[]
			for imk in os.listdir("accounts/"+e[0]+"/contacts"):
				op= open("accounts/"+e[0]+"/contacts/"+imk,"r").read().split("\n")
				ctn.append({"name":op[0],"email":op[1], "message":op[2],"id":imk})
			p=[open("accounts/"+e[0]+"/name.txt","r").read(),open("accounts/"+e[0]+"/template/template_no.txt","r").read(),open("accounts/"+e[0]+"/views.txt","r").read(),open("accounts/"+e[0]+"/password.txt","r").read()]
			return render_template("dashboard.html", username=e[0], name=p[0], contact=ctn, template=p[1], views=p[2], domain="localhost:5000", password=p[3])
	else:
		return render_template("signup.html", error="none")
@app.route("/login", methods=["GET","POST"])
def login():
	if (request.method == "GET"):
		return render_template("login.html", error="none")
	else:
		w = [request.form["username"], request.form["password"]]
		if (w[0] not in os.listdir("accounts")):
			return render_template("login.html", error="No such account found!")
		else:
			if (open("accounts/"+w[0]+"/password.txt","r").read() == w[1]):
				ctn=[]
				for imk in os.listdir("accounts/"+w[0]+"/contacts"):
					op= open("accounts/"+w[0]+"/contacts/"+imk,"r").read().split("\n")
					ctn.append({"name":op[0],"email":op[1], "message":op[2],"id":imk})
				p=[open("accounts/"+w[0]+"/name.txt","r").read(),open("accounts/"+w[0]+"/template/template_no.txt","r").read(),open("accounts/"+w[0]+"/views.txt","r").read(),open("accounts/"+w[0]+"/password.txt","r").read()]
				return render_template("dashboard.html", username=w[0], name=p[0], contact=ctn, template=p[1], views=p[2], domain="localhost:5000", password=p[3])
			else:
				return render_template("login.html", error="Wrong password!")

@app.route("/back/dashboard/<username>/<password>", methods=["POST"])
def back_to_dashboard(username, password):
	w = [username,password]
	if (w[0] not in os.listdir("accounts")):
		return "Session expired"
	else:
		if (open("accounts/"+w[0]+"/password.txt","r").read() == w[1]):
			ctn=[]
			for imk in os.listdir("accounts/"+w[0]+"/contacts"):
				op= open("accounts/"+w[0]+"/contacts/"+imk,"r").read().split("\n")
				ctn.append({"name":op[0],"email":op[1], "message":op[2],"id":imk})
			p=[open("accounts/"+w[0]+"/name.txt","r").read(), open("accounts/"+w[0]+"/template/template_no.txt","r").read(),open("accounts/"+w[0]+"/views.txt","r").read(),open("accounts/"+w[0]+"/password.txt","r").read()]
			return render_template("dashboard.html", username=w[0], name=p[0], contact=ctn, template=p[1], views=p[2], domain="localhost:5000", password=p[3])
		else:
			return "Session expired"

@app.route("/edit/template/<username>/<password>", methods=["POST"])
def editTemplate(username, password):
	w = [username,password]
	if (w[0] not in os.listdir("accounts")):
		return "Session expired"
	else:
		if (open("accounts/"+w[0]+"/password.txt","r").read() == w[1]):
			ee = [open("accounts/"+w[0]+"/template/template_no.txt","r").read(), open("accounts/"+w[0]+"/template/description.txt","r").read(), open("accounts/"+w[0]+"/name.txt","r").read()]
			return render_template("edittemplate.html", template_no=ee[0] ,description=ee[1], name=ee[2], username=username, password=password)
		else:
			return "Session expired"

@app.route("/edit/changes/<username>/<password>", methods=["POST"])
def editChanges(username, password):
	w = [username,password]
	if (w[0] not in os.listdir("accounts")):
		return "Session expired"
	else:
		if (open("accounts/"+w[0]+"/password.txt","r").read() == w[1]):
			wer=[ request.form["name"], request.form["description"], request.form["template_no"] ]
			open("accounts/"+w[0]+"/template/template_no.txt","w").write(wer[2])
			open("accounts/"+w[0]+"/template/description.txt","w").write(wer[1])
			open("accounts/"+w[0]+"/name.txt","w").write(wer[0])
			ee = [open("accounts/"+w[0]+"/template/template_no.txt","r").read(), open("accounts/"+w[0]+"/template/description.txt","r").read(), open("accounts/"+w[0]+"/name.txt","r").read()]
			return render_template("edittemplate.html", template_no=ee[0] ,description=ee[1], name=ee[2], username=username, password=password)
		else:
			return "Session expired"

@app.route("/delete/contact/<username>/<id>", methods=["POST"])
def delete_contact(username,id):
	try:
		os.remove("accounts/"+username+"/contacts/"+id)
		return "y"
	except:
		return "x"
@app.route("/delete", methods=["GET","POST"])
def delete():
	if (request.method == "GET"):
		return render_template("delete.html", error="none")
	else:
		w = [request.form["username"], request.form["password"]]
		if (w[0] not in os.listdir("accounts")):
			return render_template("delete.html", error="No such account found!")
		else:
			if (open("accounts/"+w[0]+"/password.txt","r").read() == w[1]):
				shutil.rmtree("accounts/"+w[0])
				return render_template("index.html", msg="Account deleted")
			else:
				return render_template("delete.html", error="Wrong password!")

@app.errorhandler(404)
def er404(a):
	return render_template("404.html")

if __name__ == '__main__':
	app.run()