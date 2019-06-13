from flask import Flask, render_template, redirect, request, url_for
from werkzeug import secure_filename
#import paramiko
import os

UPLOAD_FOLDER = '/home/pi/.octoprint/uploads'
#ALLOWED_EXTENSIONS = set(['txt']) #TRY LATER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	#return render_template('index.html')
    return render_template('login.html')
    

@app.route('/authUser', methods = ['POST'])
def auth_user():
    credentials = open("credentials.txt","r")

    if request.form['username'] == credentials.readline()[:-1] and request.form['password'] == credentials.readline():
                                        #remove line break (:-1)
        credentials.close()
        return render_template('index.html')
        
    else:
        return redirect(url_for('index'))
        

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

	
@app.route('/getData', methods = ['POST'])
def get_data():
	
	#FORM DATA REQUEST
	data = request.form #Get text-box inputs from front-end
	print(data)
	
	nozzle = data["nozzle_temp"]
	bed = data["bed_temp"]

	#FILE UPLOADING
	f = request.files['file']
	filename = secure_filename(f.filename)
	print(filename)
	f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	
	start_printing(filename, nozzle, bed)
	print("olakase")
	
	return ''
	
def start_printing(filename, nozzle_temp, bed_temp):

	os.chdir("/home/pi/oprint/local/bin/OctoControl")	#cd /home/pi/oprint/local/bin/OctoControl
														#here are located OctoControl commands
	
	##########
	##### Funciones
	##########
	
	def connect():
		os.system('bash 8connect')						#execute command
	
	def set_nozzle_temp():
		set_nozzle_command = "bash 8settemp " + nozzle_temp
		os.system(set_nozzle_command)
		
	def set_bed_temp():
		set_bed_command = "bash 8setbed " + bed_temp
		os.system(set_bed_command)
	
	def select_file():
		select_file_command = "bash 8fselect " + filename
		os.system(select_file_command)
	
	def print_file():
		os.system('bash 8print')
		
	
	
	#Connect printer (execute only once after turning printer on)
	#connect()
	
	#Set nozzle temperature
	set_nozzle_temp()
	
	#Set bed temperature
	set_bed_temp()
	
	#Select print file
	select_file()
	
	#Print selected file
	print_file()

	
if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port=4000)