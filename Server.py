from datetime import timedelta
import os
import flask
from cryptography.fernet import Fernet
from flask import Flask,request,flash, redirect, render_template, session
from flask_cors import CORS
from werkzeug import serving
import ssl
import sys

HTTPS_ENABLED = True
VERIFY_USER = True

API_HOST = "0.0.0.0"
API_PORT = 5000
API_CRT = "./static/Cert/Server.crt" # add your Server.crt into that folder
API_KEY = "./static/Cert/Server.key" # add your Server.key into that folder
API_CA_T = "./static/rootCA/rootCA.crt" # add your rootCA.crt into that folder

app = Flask(__name__)
CORS(app)

def load_key():
    """
    Loads the key from the current directory named `.key.key`
    """
    return open("key.key", "rb").read()


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)





@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect('/')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/v1/api/add-rule/', methods=['POST'])
def add_rule():

    request_data = request.get_json()
    chain = request_data['chain']
    lineNumber = request_data['Line_Number']
    source = request_data['Source_IP']
    destination = request_data['Destination_IP']
    protocol = request_data['Protocol']
    sport = request_data['Source_Port']
    dport = request_data['Destination_Port']
    interfaceInput = request_data['Interface_Input']
    interfaceOutput = request_data['Interface_Output']
    target = request_data['Target']

    STR = "The chain is: " + chain + "\nThe line number is: " + lineNumber + "\nThe source IP is:" + source + "\nThe destination IP is: " + destination + "\nThe protocol is: " + protocol + "\nThe source port is: " + sport + "\nThe destination port is: " + dport + "\nThe interface input is: " + interfaceInput + "\nThe interface output is: " + interfaceOutput + "\nThe target is: " + target
    target = " -j " + target;
    if (source != ""):
        source = " -s " + source;
    if (destination != ""):
        destination = " -d " + destination;
    if (protocol != ""):
        protocol = " -p " + protocol;
    if (sport != ""):
        sport = " --sport " + sport;
    if (dport != ""):
        dport = " --dport " + dport;
    if (interfaceInput != ""):
        interfaceInput = " -i " + interfaceInput;
    if (interfaceOutput != ""):
        interfaceOutput = " -o " + interfaceOutput;

    if (lineNumber == ""):
        os.system("sudo iptables -A " + chain + source + destination + protocol + sport + dport + interfaceInput + interfaceOutput + " " + target)
    else:
        os.system("sudo iptables -I " + chain + " " + lineNumber + source + destination + protocol + sport + dport + interfaceInput + interfaceOutput + " " + target)

    return format(STR)

@app.route("/v1/api/delete-rule/", methods=['POST'])
def delete_rule():
    request_data1 = request.get_json()
    chain = request_data1['chain']
    lineNumber = request_data1['Line_Number']
    returned_value = os.system("sudo iptables -D " + chain + " " + lineNumber)
    if(returned_value == 256 ):
        return '''
            There are no rules to be deleted
            '''.format()
    return '''
        Chain {}
        rule number {}
        has been deleted '''.format(chain, lineNumber)

@app.route("/v1/api/list/", methods=['GET'])
def list():
    os.system("sudo iptables -L -n -v > list.txt")
    os.system("python3 ListIPTables.py")
    return open("list.json", "r").read()

@app.route("/v1/api/save/", methods=['GET'])
def save():
    os.system("iptables-save > iptables_Save.txt")
    key = load_key()
    filename = "iptables_Save.txt"
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open("encrypted_iptables.txt", "wb") as file:
        file.write(encrypted_data)

    return flask.send_file("encrypted_iptables.txt",as_attachment=True)

@app.route("/v1/api/restore/", methods=['POST'])
def restore():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        flash('File extension is not allowed')
    key = load_key()
    f = Fernet(key)
    #file = request.files['file']
    file_data = file.read()
    decrypted_data = f.decrypt(file_data)
    with open("decrypted_iptables.txt", "wb") as file:
        file.write(decrypted_data)

    os.system("iptables-restore decrypted_iptables.txt")
    return redirect('/')
app.secret_key = os.urandom(12)
context = None
if HTTPS_ENABLED:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    if VERIFY_USER:
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(API_CA_T)
    try:
        context.load_cert_chain(API_CRT, API_KEY)
    except Exception as e:
        sys.exit("Error starting flask server. " +
            "Missing cert or key. Details: {}"
            .format(e))
serving.run_simple(API_HOST, API_PORT, app, ssl_context=context)    



