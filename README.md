# Camorah

Camorah is a python tool aimed to start Orah 4i 360 camera.
It's not the napolitan mafia...


### SETUP

You will need a POE module, a dhcp server and a rtmp server to make the setup work.
The camera is powered through POE (take care which plug is powered on it).
The camera need an ip adress through dhcp.
The camera sends its stream in RTMP.
RTMP protocol need an intermediate server for publishing video/audio stream (you can't stream from camera to viewer directly with rtmp).


For dhcp server you can set your own or use your ISP box. There is no limitation.

For rtmp server we advise to use nginx with rtmp module:
download nginx source : http://nginx.org/en/download.html
download nginx rtmp module sources : git clone https://github.com/arut/nginx-rtmp-module.git
Go in nginx directory and compile it with rtmp support:
./configure --add-module=/path/to/nginx-rtmp-module
make
make install
We provide a default nginx.conf file for easy setup but there is no security implemented (anyone can publish and listen on your server).
We provide a stat.xsl file for displaying nginx streaming stat through its http server. Put it in the html root dir of the http server.


### Running camorah tool

You will need the following python libraries as dependencies : 
autobahn, protobuf, zeroconf
you can install them with pip.


To start the camorah tool:
python3 camorah.py
or
python3 camorah.py -s 192.168.0.2 -p 2048 -a mystream -d ./rec/

When using no option, we will consider that the rtmp server is on the same computer as camorah and at port 1935 with rtmp app named "inputs".
Here is the help page if you want to define another rtmp server or dump the stream:

Camorah

Tool for starting 4i 360 camera from orah

-h | --help	Prints this help screen.
-s | --server	Set ip address of rtmp server. (default : ip of this device)
-p | --port	Set port of rtmp server. (default : 1935)
-a | --app	Set rtmp application name. (default : inputs)
-d | --dump	Dump streams in specified dir.


Example:
python3 camorah.py
python3 camorah.py -s 192.168.0.2 -p 2048 -a mystream -d ./rec/


The tool keep running until you kill it as it's continusouly running waiting to detect camera through zeroconf and then start them.
Camorah also retrieve a ptv file named "factoryPresetsProject.ptv" followed by the date that you can use as calibration in stitchem.


### Practical SETUP

Different setup are possible and have been used (don't forget the POE):

Debug or Livestitch at home : Plug your cam in your ISP box, setup a rtmp server and stitchEm Vahana on your PC.
Livestitch mobile : Plug your cam in your PC, setup a dhcp server, a rmtp server and stitchEm Vahana on your PC.
Record mobile : Plug your cam in a raspberry, setup a dhcp server. a rtmp server on raspberry and dump the 
                stream on an usb key plug in the raspberry. Stitch the dumps in stichEm Studio.
