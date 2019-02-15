import requests
import json

def broadcast_to_friend(data, where):
	try:
		fd = open("port.txt", 'r')
	except IOError:
		print("Can't choose any port")
		return (0)
	port = fd.read()
	
	req = requests.get("http://localhost:" + port + "/nodes")
	nodes = json.loads(req.text)
	for node in nodes:
		print(node)
		req = requests.post("http://" + node + where, json = data)

def getPortFromFile(file = "port.txt"):
	try:
		fd = open(file, 'r')
		return (fd.read())
	except IOError:
		print("can't read file %s" % file)