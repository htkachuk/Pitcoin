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
		while True:
			self.mine()
	
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
		req = requests.get("http://localhost:" + PORT + "/nodes")
		nodes = req.text
		req = requests.get("http://localhost:" + PORT + "/chain/length")
		my_length = int(req.text)
		for node in nodes:
			print(node)
			url = 'http://' + PORT + '/chain/length'
			req = requests.get(url)
			length = int(req.text)
			if my_length < length:
				my_length = length
				req = requests.get("http://" + PORT + "/chain")
				chain = json.loads(req.text)
				pp.add_data(chain, 'blockchain.pickle')

if __name__ == '__main__':
	PORT = cnf.getPortFromFile()
	print("Port = ", PORT)
	cli = Cli()
	try:
		cli.cmdloop()
	except KeyboardInterrupt:
		print("\nBye, have a nice day!")
