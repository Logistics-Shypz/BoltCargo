from flask import Flask,redirect,url_for,Request,request,Response
from flask import make_response
from flask.templating import render_template
from flask.globals import session
import requests
from sympy.utilities.decorator import threaded
import urllib
import json
from flask import jsonify
import pika
from datetime import datetime
from nltk.metrics import distance
from flask import session
import sys


app = Flask(__name__)
app.secret_key = 'boltcargo_secret'

flask_server_ip = ''
backend_server_ip = ''


@app.route('/')
def index():
	if 'user' in session:
		uid = session['user']
		r = requests.get('http://' + backend_server_ip + ':3000/v1/users/user/' + uid)
		r = r.json()[0]
		uname = r['userName']
		if r['userType'] == 'transporter':
			return render_template('transporter.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'forwarder':
			#get user if from session and call webservice to get type of user and then redirect to approporate dashboard
			return render_template('forwarder.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'shipper':
			return render_template('shipper.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
	else:
		return render_template('index.html',username='guest')
	#return render_template('login.html',username="guest")
	#return my_resp


@app.route('/register')
def usersignup():
	return render_template('signup.html',backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)


@app.route('/profile')
def userProfile():
	return render_template('profile.html',backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)


@app.route('/transporter',methods=['POST'])
def transporter():
	user_id = request.form['userid']
	if user_id == '':
		return redirect(url_for('userlogin'))
	else:
		session['user'] = user_id
		uid = session['user']
		r = requests.get('http://' + backend_server_ip + ':3000/v1/users/user/' + uid)
		r = r.json()[0]
		uname = r['userName']
		return render_template('transporter.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
	# if not in session['user']:
	# 	redirect(url_for('userlogin'))
	# else:
	# 	return "Hello Boss!  <a href="/logout">Logout</a>"
	# #redirect(url_for('transporter',uid=request.args['userid']))

@app.route('/forwarder',methods=['POST'])
def forwarder():
	user_id = request.form['userid']
	if user_id == '':
		return redirect(url_for('userlogin'))
	else:
		session['user'] = user_id
		uid = session['user']
		r = requests.get('http://' + backend_server_ip + ':3000/v1/users/user/' + uid)
		r = r.json()[0]
		uname = r['userName']
		return render_template('forwarder.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)


@app.route('/dashboard',methods=['POST'])
def dasboard():
	username = request.form['bcusername']
	password = request.form['bcpassword']
	r = requests.get('http://' + backend_server_ip + ':3000/v1/users/user/' + username + "/" + password)
	r = r.json()
	if len(r) > 0:
		r = r[0]
		session['user'] = r['_id']
		uname = r['userName']
		if r['userType'] == 'transporter':
			return render_template('transporter.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'forwarder':
			#get user if from session and call webservice to get type of user and then redirect to approporate dashboard
			return render_template('forwarder.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'shipper':
			return render_template('shipper.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
	else:
		return render_template('login.html',username='guest')
	# if 'user' in session:
	# 	uid = session['user']
	# 	r = requests.get('http://localhost:3000/v1/users/user/' + uid)
	# 	r = r.json()[0]
	# 	if r['userType'] == 'transporter':
	# 		return render_template('transporter.html',username=session['user'])
	# 	elif r['userType'] == 'forwarder':
	# 		#get user if from session and call webservice to get type of user and then redirect to approporate dashboard
	# 		return render_template('dashboard.html',username=session['user'])
	# 	elif r['userType'] == 'shipper':
	# 		return render_template('shipper.html',username=session['user'])
	# else:
	# 	return render_template('dashboard.html',username="guest")
	# #return my_resp

@app.route('/product')
def showProduct():
	return render_template('product.html',backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)


@app.route('/signup')
def showRegistration():
	return render_template('registration.html',backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)


@app.route('/login')
def userlogin():
	if 'user' in session:
		uid = session['user']
		r = requests.get('http://' + backend_server_ip + ':3000/v1/users/user/' + uid)
		r = r.json()[0]
		uname = r['userName']
		if r['userType'] == 'transporter':
			return render_template('transporter.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'forwarder':
			#get user if from session and call webservice to get type of user and then redirect to approporate dashboard
			return render_template('forwarder.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
		elif r['userType'] == 'shipper':
			return render_template('shipper.html',username=uname,backend_server_ip=backend_server_ip,flask_server_ip=flask_server_ip)
	else:
		return render_template('login.html')


@app.route("/logout")
def logout():
	session.pop('user',None)
	return redirect(url_for('index'))


if __name__ == '__main__':
	if sys.argv[1] == 'qa':
		flask_server_ip = '3.17.235.28'
		backend_server_ip = '3.17.235.28'
	elif sys.argv[1] == 'dev':
		flask_server_ip = 'localhost'
		backend_server_ip = 'localhost'
	print("Flask server ip : {0}".format(flask_server_ip))
	print("Backedn Server Ip : {0}".format(backend_server_ip))
	app.run('0.0.0.0',port=5000,debug=True,threaded=True)