import merkle
import pending_pool as pp
import script
import serializer as sr
from copy import deepcopy
import json
import miner_cli
import requests
import binascii
from hashlib import sha256

def check_reward_target(coinbase, port, block_hash):
	req = requests.get("http://" + port + "/chain")
	chain = json.loads(req.text)
	reward = float(chain['reward'])
	reward = reward * pow(10, 8)
	tx = sr.Deserializer.deserializer(coinbase, 1)
	if tx['outputs'][0]['Value'] > reward:
		return False
	target = int(chain['target'])
	if (int(block_hash, 16) > target):
		print("Invalid block_hash")
		return False
	return True


def consensus():
	minercli = miner_cli.Cli()
	minercli.do_consensus("")

def get_last_block(port):
	req = requests.get("http://" + port + "/block/last")
	last_block = json.loads(req.text)
	return last_block

def block(block):
	block = block.to_dict(flat=False)
	ports = pp.read_nodes_from_file()
	port = ports[0]
	if check_reward_target(block['transactions'][0], port, block['hash'][0]) == False:
		return False
	last_block = get_last_block(port)
	if last_block['hash'] != block['previous_hash'][0]:
		consensus()
	if float(last_block['timestamp']) > float(block['timestamp'][0]):
		return False
	merkle_norm = binascii.hexlify(merkle.create_merkle_tree(block['transactions'])).decode('utf-8')
	if (merkle_norm != block['merkle'][0]):
		return False

	# data_for_hash =  bytes(str(block['timestamp'][0]) + str(block['nonce'][0]) + str(block['previous_hash'][0]) + str(block['transactions']) + str(['merkle'][0]), 'utf-8')
	# hash_norm =  sha256(data_for_hash).hexdigest()
	# print(hash_norm)
	# print(block['hash'][0])
	# if (hash_norm != block['hash'][0]):
	# 	return False
	# print("Hash passsed")
	if (len(block['transactions']) > 1):
		txs = deepcopy(block['transactions'])
		i = 0
		for tx in txs:
			if i > 0:
				if script.is_it_valid(tx) == False:
					return False
			i += 1
	return True

def mining(do):
	try:
		fd = open('mine', 'w')
	except IOError:
		print("Something get wrong!")
		exit(0)
	fd.write(str(do))
