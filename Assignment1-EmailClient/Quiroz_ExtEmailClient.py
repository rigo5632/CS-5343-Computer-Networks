from socket import *
import ssl
import base64

# prints response of server
def getServerResponse(socket):
    return socket.recv(1024).decode() # Prints out 1 MByte of data

# Returns a SSL connection to Google's smtp server
def establishSecureConnection(socket):
    return ssl.wrap_socket(socket, ssl_version=ssl.PROTOCOL_SSLv23) # Wraps socket with SSL (Different versions might yield different responses)

# sends requests to server, prints response of server only if request is not the content of email.
def generateRequests(socket, request, type):
    print(request.decode())
    socket.send(request)
    print(getServerResponse(socket)) if type == 0 else None # does not print when entering email content (Subject, email content)

# Opens TCP connection to server. Contains a small dictionary of all email requests that will be made.
def serverCommunication(serverName, serverPortNumber, emailRequests):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM) # IPV4 with a TCP connection
        clientSocket.connect((serverName, serverPortNumber))

        print(getServerResponse(clientSocket))

        # unsecure requests
        generateRequests(clientSocket, emailRequests['helo'], 0)
        emailRequests.pop('helo')

        generateRequests(clientSocket, emailRequests['starttls'], 0)
        emailRequests.pop('starttls') # From this point your requests must be secure (SSL wrapper)
        
        # makes secure requests
        secureConnection = establishSecureConnection(clientSocket)
        # Iterates through dictionary making requests
        for key in emailRequests.keys():
            if key == 'login':
                for subKey in emailRequests[key]:
                    generateRequests(secureConnection, emailRequests[key][subKey], 0)
            elif key == 'msgBody':
                for subKey in emailRequests[key]:
                    generateRequests(secureConnection, emailRequests[key][subKey], 1)
            else:
                generateRequests(secureConnection, emailRequests[key], 0)
    except:
        print('Connection to server was lost.')
        print('Possible Errors: ')
        print('1. Invalid Gmail Account')
        print('2. Gmail account has restricted access')
        exit()
    finally:
        secureConnection.close() # Closes socket when done

# Ask user for their Gmails Credentials and Recipient of email
userMail        = str(input('Gmail Email: '))
password        = str(input('Password: '))
recipientEmail  = str(input('Send To: '))

# Contains the request that will be made to Gmail's smtp server
emailRequests = {
    'helo'      : b'helo gmail.com\r\n',
    'starttls'  : b'starttls\r\n',
    'login'     : 
    {
        'authentication'    : b'auth login\r\n',
        'username'          : base64.b64encode(userMail.encode()) + b'\r\n', #Encrypted with base64 (Google's standard)
        'password'          : base64.b64encode(password.encode()) + b'\r\n' 
    },
    'from'      : ('mail from:<' + userMail + '>\r\n').encode(),
    'to'        : ('rcpt to:<' + recipientEmail + '>\r\n').encode(),
    'data'      : b'data\r\n',
    'msgBody'   : 
    {
        'Subject'   : b'Subject: Email from my email client\r\n\r\n', 
        'body'      : b'This is a test email from my own email client. Hope this finds you well. Quiroz, Rigoberto.\r\n'
    },
    'endOfMsg'  : b'.\r\n',
}

serverCommunication('smtp.gmail.com', 587, emailRequests)
 