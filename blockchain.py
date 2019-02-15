import block
import struct
import pending_pool as pp
import ipaddress
import json
import config




class Blockchain():
	def __init__(self):
		self.reward = 50
		self.ideal_time = 60
		self.real_time = 15
		self.max_hash = int("f" * 64, 16)
		self.bits = 0
		self.target = int("00000aaaaaaaaaaaaaaa00000000000000000000000000000000000000000000", 16)
		self.diff = self.max_hash / self.target

		self.chain, self.height = self.init_file('chain.pickle', 1)
		self.node = self.init_file('node.pickle', 0)
		print("init target = ", hex(self.target))
		print("init diff = ", hex(int(self.diff)))

	def genesis_block(self):
		new_block = block.Block()
		new_block.mine(self.target)
		self.chain.append(new_block.get_block())
		pp.add_data(self.chain, 'chain.pickle')

	def reCalcDiff(self):
		self.real_time = int(float(self.chain[0]['timestamp']) - float(self.chain[4]['timestamp']))
		if self.real_time in range (self.ideal_time - 3, self.ideal_time + 3):
			return 1
		if self.real_time <= 0:
			self.real_time = 1
		coef = self.calcCoeff()
		self.diff = self.diff * coef
		self.target = self.max_hash / self.diff 
		print("new target = ", hex(int(self.target)))
		print("new diff = ", hex(int(self.diff)))

	def calcCoeff(self):
		coef = self.ideal_time / self.real_time
		if coef > 1.25:
			return (1.25)
		if coef < 0.75:
			return (0.75)
		return (coef)

	def mine(self, prev_hash):
		self.height += 1
		new_block = block.Block(prev_hash, self.height, reward = self.reward)
		new_block.mine(self.target)
		self.chain.insert(0, new_block.get_block())
		pp.add_data(self.chain, 'chain.pickle')
		if len(self.chain) % 5 == 0:
			self.reCalcDiff()
		if (len(self.chain) % 10 == 0):
			self.reward /= 2

	def resolve_conflicts():
		pass

	def is_valid_chain():
		pass

	def add_node(self, node):
		ip = node.split(':')[0]
		try:
			ip = ipaddress.ip_address(ip)
		except ValueError:
			return(0)
		if int(node.split(':')[1]) >= 1 and int(node.split(':')[1]) <= 65535:
			self.node.append(node)
			pp.add_data(self.node, 'node.pickle')
			return(1)
		else:
			return(0)

	def init_file(self, name, t):
		data = pp.get_data(name)
		if data == False:
			data = []
			height = 0
		else:
			data = json.loads(data)
			if t != 0:
				height = data[0]['height']
		if t == 1:		
			return data, height
		else:
			return data

def fromBitsToDiff(bits):
	leng = int(bits[:2], 16)
	res = bits[2:]
	while (len(res) < leng * 2):
		res += "00"
	return (res)

def fromDiffToBits(diff):
	res = hex(len(diff) // 2)[2:]
	res += diff[0:6]
	return (res)

if __name__ == '__main__':
	# bc = Blockchain()
	print()
	# print(int("2815ee000000000000000000000000000000000000000000", 16))
	print(floa)
	print(fromDiffToBits(floa))
	# print(int(fromBitsToDiff("172e6f88"), 16))
	# fromBitsToDiff("1d00ffff")
	# print(15.1 > 15)
	# print(range(bc.ideal_time - 3, bc.ideal_time + 3))
