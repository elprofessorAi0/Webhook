from flask import Flask, request
from dotenv import load_dotenv
import requests
import json
import os 

""" # .env file contain secret key / account token / more. """

load_dotenv(".env")
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('SECRET_KEY')
Authorization = os.getenv('Authorization')


""" Scritps Start """

# Response Message
def handle_Message(senderPsid, receivedMessage):
    if "Text" in receivedMessage:
        response = {"text":f"You just send me: {receivedMessage['text']}"}

        send_message(senderPsid, response)
    else:
        response = {"text":f"This chatbot only accepts text messages"}
        
        send_message(senderPsid, response)

# Send Message
def send_message(self, senderPsid, response):
        id = "Your Id"
        # url = f"https://graph.facebook.com/v10.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
        url = f"https://graph.facebook.com/v10.0/{id}/subscribed_apps"
        PAGE_ACCESS_TOKEN = VERIFY_TOKEN

        payload = {
            'access_token': PAGE_ACCESS_TOKEN
    
            }
        
        headers = {'content-type': 'application/json'}
    
        r = requests.post(url, json = payload, headers = headers)
        print(r.text)

# Scritps End

""" Flask Start """
app = Flask(__name__)
app.config["SECRET_KEY"] = VERIFY_TOKEN

@app.route('/', methods = ["GET", "POST"])
def home():
    with open("Html_Code/Html.html") as Html_Code:
        html = Html_Code.read()
    return html, 404
    
@app.route('/webhook', methods = ["GET", "POST"])
def index():

    """ Get request """

    if request.method == "GET":
        
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("webhook VERIFIED")
                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                return "ERROR", 403

    """ Post request """
    if request.method == "POST":
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            # print(mode)

        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            # print(token)

        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            # print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("Webhook VERIFIED")

                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                return "ERROR", 403

        return request.data, 200
    
    # Respose From Server.
    """ If You Send Messange or Reseve Message """
    data = request.data
    if data == "" or data == None:
        return "No Data Found"
    data = data.decode('utf-8')
    print(data)
    body = json.loads(data)

    if 'object' in body and body['object'] == 'page':
        entries = body['entry']
        for entry in entries:
            webhookEvent = entry['messaging'][0]
            print(webhookEvent)

            senderPsid = webhookEvent['sender']['id']
            print(f"Sender PSID: {senderPsid}")

            if 'message' in webhookEvent:
                handle_Message(senderPsid, webhookEvent['message'])

            return "EVENT_RECEIVED", 20
        else:
            return "ERROR", 404

# Flask End  
if __name__ == '__main__':
    try:
        #app.run(debug = True) 
        app.run(host = 'localhost', port = '5000', debug = True)    
    except Exception as e:
        print(f"Error is {e}")
