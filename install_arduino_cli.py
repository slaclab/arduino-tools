from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import tarfile
import os
import platform
import subprocess
import shutil


target=platform.system()+"-"+platform.architecture()[0]

arduino_url= "https://downloads.arduino.cc/arduino-cli"
images={
    "Windows-64bit": "arduino-cli_latest_Windows_64bit.zip",
    "Windows-32bit": "arduino-cli_latest_Windows_32bit.zip",
    "Linux-64bit" : "arduino-cli_latest_Linux_64bit.tar.gz"
}
exe={
    "Windows-64bit": ".exe",
    "Windows-32bit": ".exe",
    "Linux-64bit" : ""
}


def arduino_cli(command):
    os.chdir(os.environ['PREFIX'])
    cmd=[ 'bin/arduino-cli'+exe[target] ,'--config-file','etc/arduino-cli.yaml' ]
    cmd=cmd+command.split(" ")
    print(cmd)
    process = subprocess.Popen(cmd,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()


destdir=os.environ["PREFIX"]+"/bin"
libdir=os.environ["PREFIX"]+"/lib"

try:
    os.mkdir(destdir)
    os.mkdir(libdir)
except:
    pass


filename=images[target]

r = urlopen(arduino_url+"/"+images[target])
data=BytesIO(r.read())
if(filename.endswith(".tar.gz") or filename.endswith(".tgz")):
    tar = tarfile.open(fileobj=data,mode="r")
    content=tar.extractall(path=destdir)
elif (filename.endswith(".zip")):
    zipfile = ZipFile(data)
    zipfile.extractall(path=destdir)
shutil.copytree("etc",os.environ['PREFIX']+'/etc')
arduino_cli("cache clean")
arduino_cli("core update-index")
arduino_cli("core install arduino:avr")
