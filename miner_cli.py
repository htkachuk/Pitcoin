import cmd
import blockchain
import server_commands
import pending_pool as pp
import json
import requests
import config as cnf

PORT = None

class Cli(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "฿ "
		self.intro  = "\t\tWelcome to the miner cli\nHow to use? 'help'!!"
		self.doc_header ="For detail information use 'help _command_')"
		self.blockchain = pp.get_data("blockchain.pickle")
		if (self.blockchain == False):
			self.blockchain = blockchain.Blockchain()
			self.blockchain.genesis_block()

		# self.mine = True
		# self.utxo = utxo_set.Utxo_pool()

	def mine(self):
		chain = self.blockchain.chain
		self.blockchain.mine(chain[0].hash)
		print("New block hash", self.blockchain.chain[0].hash)

	def do_mine(self, args):
		"""mine - start mining process. Mine block with getting transactions 
		from pending pool, adding coinbase transaction with miner address from a file,
		calculation parameters like merkle root, hash and saving block in chain"""

		# self.do_consensus(args)
		while True:
			try:
				fd = open('mine', 'r')
			except:
				print("Mining has been stoped(((")
				break
			m = fd.readline()
			if m == '3':
				print("In file mine is '3', so it's time to do something else!\nFor starting mine process, please write in file mine '1' and start command mine")
				return
			while m == '1':
				self.mine()
				m = '0'
				fd.close()
	
	def do_exit(self, args):
		"""exit"""
		print("Bye, have a nice day!")
		exit(0)

	def do_add_node(self, args):
		"""add_node - adding node to nodes list of Blockchain (based on received
		parameter in URL format without scheme)"""
		if len(args.split(' ')) == 1:
			if self.blockchain.add_node(args) == 1:
				print("Node sucsessfuly added!")
			else:
				print("Unvalid node, please check it and use this command again")
		else:
			print("usage\tadd_node ip:port")

	def do_consensus(self, args):
		nodes = pp.read_nodes_from_file()
		len_list = []
		dicti = {}
		for x in nodes:
			dicti = {}
			dicti["ip"] = x
			try:
				dicti["length"] = int(requests.get("http://" + x + "/chain/length").text)
			except:
				dicti["length"] = 0
			len_list.append(dicti)
		newlist = sorted(len_list, key=lambda k: k['length']) 
		if (newlist[-1]['ip'] != nodes[0]):
			req = requests.get("http://" + newlist[-1]['ip'] + "/chain")
			chain = req.text
			req = requests.get("http://" + newlist[-1]['ip'] + "/utxo")
			utxo = req.text
			pp.add_data(chain, 'blockchain.pickle')
			pp.add_data(utxo, 'utxo.pickle')

if __name__ == '__main__':
	PORT = cnf.getPortFromFile()
	print("Port = ", PORT)
	cli = Cli()
	try:
		cli.cmdloop()
	except KeyboardInterrupt:
		print("\nBye, have a nice day!")
