import merkle
import pending_pool as pp

def block(block):
	minercli = miner_cli.Cli()
	ports = pp.read_nodes_from_file()
	port = ports[0]
	req = requests.get("http://" + port + "/block/last")
	last_block = json.loads(req.text)
	if last_block['hash'] != block['previous_hash']:
		minercli.do_consensus("")
	if float(last_block['timestamp']) > float(block['timestamp']):
		return False
	merkle_norm = binascii.hexlify(merkle.create_merkle_tree(block['transactions'])).decode('utf-8')
	if (merkle_norm != block['merkle']):
		return False
	hash_norm =  bytes(str(block['timestamp']) + str(block['nonce']) + str(block['previous_hash']) + str(block['transactions']) + str(['merkle']), 'utf-8')
	if (hash_norm != block['hash']):
		return False
