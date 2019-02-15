import requests
import pickle
import json
import block
import pending_pool as pp

def broadcast_to_friend(data, where):
	nodes = []
	ports = pp.read_nodes_from_file()
	for x in ports:
		nodes.append(x.replace("\n", ""))
	if (type(data) is block.Block):
		data = pickle.dumps(data)
	for node in nodes:
		print(node)
		req = requests.post("http://" + node + where, data = data)

def getPortFromFile(file = "port.txt"):
	try:
		fd = open(file, 'r')
		return (fd.read())
	except IOError:
		print("can't read file %s" % file)