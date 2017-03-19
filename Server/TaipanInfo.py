def PrintTaipanFooter():
    print("""

  _______    _                     _____         _______ 
 |__   __|  (_)                   |  __ \     /\|__   __|
    | | __ _ _ _ __   __ _ _ __   | |__) |   /  \  | |   
    | |/ _` | | '_ \ / _` | '_ \  |  _  /   / /\ \ | |   
    | | (_| | | |_) | (_| | | | | | | \ \  / ____ \| |   
    |_|\__,_|_| .__/ \__,_|_| |_| |_|  \_\/_/    \_\_|   
              | |                                        
              |_|                                        

""")

def PrintMeterpreterHelp():
    print("\nCommand: 'terminate' Action: Terminates the connection between client server\n")
    print("\nCommand: 'screenshot' Action: Takes a screenshot from the client and sends it back to server.\n")
    print("\nCommand: 'webshot' Action: Take a webcam photo from the client and sens it back to server.\n")
    print("\nCommand: 'sysinfo' Action: Returns information of the computer, like OS name and computer name\n")
    print("\nCommand: 'messagebox' Action: Shows a fully customizable messagebox to client\n")
    print("\nCommand: 'persistence' Action: Add program to registry. Attention it will not work ! See more info\n")
    print("\nCommand: 'credgather' Action: Returnto client... all credentials found to firefox and chrome\n")
    print("\nCommand: 'uploadexecute' Action: Upload executable file only to server and then executes it\n")
    print("\nCommand: 'keylogger_start' Action: Start the remote keylogger on the client\n")
    print("\nCommand: 'keylogger_stop' Action: Stop the remote keylogger on the client\n")
    print("\nCommand: 'keylog_dump' Action: Send back to server all keystroke logs\n")
    print("\nCommand: 'exitconn' Action: Go the current connection background, and goes back to main handle\n")
    print("\nCommand: 'help' Action: Prints this message to the console\n")
    print("\nCommand: 'clear' Action: Clear the console\n")

def PrintHandleHelp():
    print("\nCommand: 'printconns' Action: Prints all active connection in the console.")
    print("Command: 'conn' Action: You can connect to a client given it's ID.")
    print("Command: 'help' Action: Prints this message.")
    print("Command: 'exit' Action: Exit the program completely.")
    print("Command: 'clear' Action: Clear the console\n")