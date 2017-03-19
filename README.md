# Taipan RAT
## What Taipan RAT is ?
Taipan is a lightweight Remote Administration Tool for windows... with safety and stability that other Remote Administration Tools doesn't provide.

## What features does it have ?
Taipan doesn't have unnecessary features. The complete feature list is this:

1. Screenshot Description: Take a screenshot from the client and send it back to server
2. Webshot Description: If the client has a webcam it takes a photo from it, and send it back to server
3. MessageBox Description: Shows a fully customizable messagebox to the client
4. Persistence Description: Add the script to the Windows registry
5. credgather Description: Gather credentials from Firefox and Google Chromeand(if available) send it back to server.
6. upload and execute Description: Upload an executable(only) to client and execute it.
7. System Information Description: Send back to server information about the client, such as OS information, version e.t.c
8. Keylogger Description: Captures keystrokes in the client, and send it back to server(when client want it)

## Is Taipan RAT secure ?
Yes it is. Taipan RAT has a default SSL support which makes it very safe. SSL Certificate is embedded inside the client. However if you are planning to use the RAT, the best is to change the SSL files(Certificate and Key) in the server ... and the SSL Certificate in the client(The certificate is inside the SSLCertificate.py file)

## Can Taipan RAT be executable through pyinstaller ?
Yes and No. Taipan RAT ofcourse can be "compilied" using pyinstaller... but there are some side effects. The keylogger feature will not work properly... because Taipan RAT uses multiprocessing to start/stop Taipan RAT... and pyinstaller has some issues with it.

## How to install Taipan RAT requirements ?
You can install all Taipan RAT required modules through the requirements.txt in the repository with this command: `pip install -r requirements.txt`

## Support
I really appreciate any kind of help in this project... even by writing code or just by reporting bugs in the program.



