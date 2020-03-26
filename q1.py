from flask import Flask
app = Flask(__name__)


@app.route('/<username>')
def generateResponse(username):
    result = ''
    if(any(i.isdigit() for i in username)):
        result = ''.join([i for i in username if i.isalpha()])
    elif(username.islower()):
        result = username.upper()
    elif(username.isupper()):
        result = username.lower()
    else:
        result = username
    return '''<html><head>
    	</head>
    	<body>
    	<b>Welcome, {0}, to my CSCB20 website</b>
    	</body>
    	</html>'''.format(result)
