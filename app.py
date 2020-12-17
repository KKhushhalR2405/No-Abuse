from flask import *
from flask_socketio import SocketIO
import requests
import pickle
import json as j

model = pickle.load(open("lr_model.pkl", 'rb'))
vect = pickle.load(open("vectorizer.pickle", 'rb'))
bwset = pickle.load(open("bwset.pkl","rb"))

url = "https://jatayuhost1.herokuapp.com/"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

def ifbadword(string):#return true if string contains any bad word
    for i in string.split():
        if i in bwset:
            return True
    return False

@app.route('/')
def sessions():
    return render_template('main.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):

    def isvalid(string):
        test = [string]
        test_trans = vect.transform(test)
        p = model.predict(test_trans)[0]
        return True if (p==0 and not ifbadword(string)) else False
    
    try:
        """data = str(json['message'])
        j_data = j.dumps(data)
        headers = {"content-type":"application/json",
        "ACcept-Charset" : "UTF-8"
        }
        r = requests.post(url,data=j_data,headers=headers)
        print(r.text)
        
        if r.text[1]=="N":
            print('received my event: ' + str(json))
            socketio.emit('my response', json, callback=messageReceived)
        else:
            print("FD")"""
        if isvalid(str(json['message'])): 
    	    print('received my event: ' + str(json))
    	    socketio.emit('my response', json, callback=messageReceived)
    
    
    except Exception as e:
    	print(e)
if __name__ == '__main__':
    socketio.run(app, debug=True)