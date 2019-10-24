# pysensorproxy-ui
A software component to control Sensorboxes running pysensorproxy 

# Prerequisites
You must install two web framework. One is used for the front-end and another for the websocket and REST API server. 
Both of them are on different Python version. It is recommended to set-up an environment before using the software. 

```
$VENV/bin/pip3 install tornado
$VENV/bin/pip install "pyramid==1.10.4" waitress
```
