import mechanize
import getpass
#Mechanize does not support JavaScript, therefore neither JQuery AJAX for data sending
#Attribute 'action' with server address in the <form> tag is required

br = mechanize.Browser()

###########
##### LOGIN
###########

br.open("http://10.0.1.61:4000")

br.geturl()

for form in br.forms():
	print(form)
	
br.select_form(name="login")

username = input("Username: ")

password = getpass.getpass()

br.form.set_value(username, name="username")

br.form.set_value(password, name="password")

print(form)

br.visit_response(br.submit())

###########
##### MAIN
###########

br.geturl()

for form in br.forms():
	print(form)

br.select_form(name="print")

filename = input("File name: ")

file_location = "/home/pi/Desktop/" + filename

nozzle_temp = input("Nozzle temp: ")

bed_temp = input("Bed temp:")

br.form.set_value(nozzle_temp, name = "nozzle_temp")

br.form.set_value(bed_temp, name = "bed_temp")

br.form.add_file(open(file_location), filename = filename)

print(form)

br.submit()
