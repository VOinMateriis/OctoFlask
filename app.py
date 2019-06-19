from flask import Flask, render_template, redirect, request, url_for, session
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = '/home/pi/.octoprint/uploads'
#ALLOWED_EXTENSIONS = set(['txt']) #TRY LATER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(12) #Secret key needed to maintain sessions in Flask (to create a cookie and encode its content)

error = None
invalid_format = None

#Rennder a template depending on whether the user is logged in or not
#This solved the problem of going back to the index.html after logout, 
#because both templates are rendered in the same view '/' and cannot 
#go back to another direction
@app.route('/')
def index():
    global error
    global invalid_format
    
    if 'username' and 'password' not in session:
        return render_template('login.html', error = error)
    else:
        return render_template('index.html', error = invalid_format)
    
    return ''


@app.route('/auth', methods = ['POST'])
def auth():
    global error
    
    credentials = open("/home/pi/oprint/bin/Tests/OctoFlask/credentials.txt","r") 
    #Si no pongo la ruta completa, cuando no reinicio el servidor pero vuelvo a ejecutar el script de mechanize,
    #me da el error FileNotFoundError: [Errno 2] No such file or directory: 'credentials.txt'

    if request.form['username'] == credentials.readline()[:-1] and request.form['password'] == credentials.readline():
                                        #remove line break (:-1)
        
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        error = False
    else:
        error = True
    
    credentials.close()
    return redirect(url_for('index'))
        

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

	
@app.route('/getData', methods = ['POST'])
def get_data():
    global invalid_format
    
    #FORM DATA REQUEST
    data = request.form #Get text-box inputs from front-end
    print(data)

    nozzle = data["nozzle_temp"]
    bed = data["bed_temp"]
    
    
    #FILE UPLOADING
    f = request.files['file']
    filename = secure_filename(f.filename)
    print(filename)
    
    #FILE FORMAT VALIDATION
    if filename.endswith(".gcode"):
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        start_printing(filename, nozzle, bed)
        print("olakase")
        
        invalid_format = False
        
    else:
        print("INVALID FILE FORMAT")
        invalid_format = True
        
    return redirect(url_for('index'))
	
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