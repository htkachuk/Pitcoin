
def getPortFromFile(file = "port.txt"):
	try:
		fd = open(file, 'r')
		return (fd.read())
	except IOError:
		print("can't read file %s" % file)