import os
import json
from pprint import pprint
from flask import Flask, request, jsonify
from twilio.rest import Client, TwilioException

app = Flask(__name__)

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
proxy_service = os.environ.get('TWILIO_PROXY_SERVICE')
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return app.send_static_file('index.html')

def create_service(name):
    service = client.proxy.services.create(
        unique_name=name,
        callback_url="https://requestb.in/1e8yt5h1"
    )

    return service.sid

def numbers(service_sid):
    number_array= []
    for number in client.incoming_phone_numbers.list():
        pprint(number.sid)
        client.proxy \
            .services(service_sid) \
            .phone_numbers \
            .create(sid=number.sid)
        number_array.append(number.sid)

    return number_array

@app.route('/sessions/delete')
def delete_sessions():
    all_sessions = client.proxy.services(proxy_service).sessions.list()
    for session in all_sessions:
        print(session)
        client.proxy.services(proxy_service).sessions(session.sid).delete()
    
    return "Sessions deleted!", 200

@app.route('/setup')
def setup():
    try:
        service_name = request.args['serviceName']
        service_sid = create_service(service_name)
        service_numbers = numbers(service_sid)

        message = "New Proxy Service ({}) Created!\nThe following numbers have been added to the service: {}".format(
        service_sid, service_numbers)
    except TwilioException as e:
        print(type(e))
        print(e)
        print(e.args)
        message = str(e.args)

    return message, 200
    
@app.route('/session/create', methods=['POST'])
def create_session():
    form_data=request.get_json()
    session_name = form_data['sessionName']
    restaurant = form_data['restaurant']
    customer = form_data['customer']
    session_ttl = form_data['sessionLength']
    try:
        session = client.proxy \
            .services(proxy_service) \
            .sessions \
            .create(unique_name=session_name, ttl=session_ttl)
        
        print(session.sid)

        participant1 = client.proxy \
            .services(proxy_service) \
            .sessions(session.sid) \
            .participants.create(identifier=restaurant, friendly_name="Restaurant")

        print("PARTICIPANT 1 >>> " + participant1.proxy_identifier)
        
        participant2 = client.proxy \
            .services(proxy_service) \
            .sessions(session.sid) \
            .participants.create(identifier=customer, friendly_name="Customer")
        
        print("PARTICIPANT 2>>> " + participant2.proxy_identifier)
        pprint(participant2)
        proxy_details = {
            'sessionSid': session.sid,
            'proxy1': participant1.proxy_identifier,
            'proxy2': participant2.proxy_identifier

        }

        client.proxy.services(proxy_service) \
            .sessions(session.sid).participants(participant1.sid) \
            .message_interactions.create(body="Proxymo established! Reply to start chat!")

        client.proxy.services(proxy_service) \
            .sessions(session.sid).participants(participant2.sid) \
            .message_interactions.create(body="Proxymo established! Reply to start chat!")

        return jsonify(proxy_details), 200
    except Exception as e:
        error = jsonify(e.args)
        return error, 500
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

