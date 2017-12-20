#Proxymo

 Flask app to help gladiator spies communicate with each other using Twilio Proxy to remain anonymous!

https://www.twilio.com/docs/api/proxy/proxy-sms-voice-phone-call-quickstart

You'll need to create a .env file with the following:
* ```TWILIO_ACCOUNT_SID```
* ```TWILIO_AUTH_TOKEN```
* ```TWILIO_PROXY_SERVICE```

Purchase some numbers in your Twilio console and use ```http://localhost:5000/setup?serviceName=<Name>``` to create a new Proxy service and have all your numbers assigned to it. You might want to use a subaccount so you don't use existing numbers in your main account!


