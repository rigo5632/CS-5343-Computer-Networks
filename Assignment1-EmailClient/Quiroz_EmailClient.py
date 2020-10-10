from socket import *

# prints response of server
def getServerResponse(socket):
    print(socket.recv(1024).decode()) # Prints server response, 1MB

# sends requests to server, prints response of server only if request is not the content of email.
def generateRequests(socket, request, type):
    print(request.decode())
    socket.send(request)
    getServerResponse(socket) if type == 0 else None # Does not print when sending email content (subject, content) 

# Opens TCP connection to server. Contains a small dictionary of all email requests that will be made.
def serverCommunication(serverName, serverPortNumber, emailRequests):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM) #IPV4 and TCP stream
        clientSocket.connect((serverName, serverPortNumber))

        getServerResponse(clientSocket)

        # Iterates through dictionary making requests
        for key in emailRequests.keys():
            if key == 'msgBody':
                for subKey in emailRequests[key]:
                    generateRequests(clientSocket, emailRequests[key][subKey], 1)
            else:
                generateRequests(clientSocket, emailRequests[key], 0)
    
        clientSocket.close()
    except:
        print('Connection to server was lost.')
        print('Possible Errors: ')
        print('1. Make sure you are using UTEP\'s network. (VPN)')
        print('2. Server time out')
        print('3. Server did not recognize request encoding')
        exit()

# Dictionary containing all requests that will be made, and content of email message
emailRequests = {
    'helo'      : b'helo utep.edu\r\n',
    'from'      : b'mail from:rmquiroz@miners.utep.edu\r\n',
    'to'        : b'rcpt to:rmquiroz@miners.utep.edu\r\n',
    'data'      : b'data\r\n',
    'msgBody'   : 
    {
        'Subject'   : b'Subject: Email from my email client\r\n\r\n', 
        'body'      : b'This is a test email from my own email client. Hope this finds you well. Quiroz, Rigoberto.\r\n'
    },
    'endOfMsg'  : b'.\r\n',
}

serverCommunication('smtp.utep.edu', 25, emailRequests)
 