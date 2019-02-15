import transaction
import pending_pool as pp
import json
import requests
import wallet
import codecs
#deserialazed transaction output, vout, hash of it
def add_output(tx_output, n, tx_hash): 

#utxo_set = {'address':some_addr
#								{'unspent_outputs':[
#													{'tx_hash_big_endian':
#													 'tx_output_n':
#													  'script':
#													  'value':
#													 }
#													]
#								}
#			}

	new_data = {
		'tx_hash_big_endian':tx_hash,
		'tx_output_n':n,
		'script':tx_output['SPK'],
		'value':tx_output['Value']
	}
	ready_data = {
		'address' : tx_output['address'],	
		'unspent_outputs' : [
		{
			'tx_hash_big_endian':tx_hash,
			'tx_output_n':n,
			'script':tx_output['SPK'],
			'value':tx_output['Value']
		}]
	}
	i = 0
	utxo_set = pp.get_data('utxo.pickle')
	if utxo_set == False:
		utxo_set = []
	else:
		lens = len(utxo_set)
		for elem in utxo_set:
			if (elem['address'] == tx_output['address']):
				i = 1
				elem['unspent_outputs'].append(new_data)
	if i == 0:
		utxo_set.append(ready_data)
	pp.add_data(utxo_set, 'utxo.pickle')


def add_to_pool(tx, tx_hash):
	n = 0
	for output in tx['outputs']:
		add_output(output, n, tx_hash)

def get_address(script):
	sig_len = script[:2]
	i = (int(sig_len, 16) * 2) + 2
	sig = script[2:i]
	pub_key = script[i+2:]
	return wallet.get_address_from_compressed_key(pub_key)

def del_from_pool(tx): #deserialiazed transaction
	utxo_set = pp.get_data('utxo.pickle')
	if utxo_set == False:
		print("Empty utxo pool!!")
		return
	utxo_set = json.loads(utxo_set)
	new_pool = []
	for elem in tx['inputs']:
		address = get_address(elem['ScriptSig'])
		for utxo in utxo_set:
			if utxo['address'] != address:
				new_pool.append(utxo)
			else:
				new_data = []
				for unspent in utxo['unspent_outputs']:
					if unspent['tx_hash_big_endian'] != elem['TXID'] and unspent['tx_output_n'] != elem['VOUT']:
						new_data.append(unspent)
				utxo['unspent_outputs'] = new_data
				new_pool.append(utxo)
	pp.add_data(new_pool, 'utxo.pickle')


def get_script(txid, vout):
	utxo_set = pp.get_data('utxo.pickle')
	utxo_set = json.loads(utxo_set)
	print(utxo_set)
	for utxo in utxo_set:
		for unspent in utxo['unspent_outputs']:
			# print(unspent['tx_hash_big_endian'])
			# print(txid)
			if unspent['tx_hash_big_endian'] == txid and hex(unspent['tx_output_n'])[2:] == vout:
				return unspent['script']



def get_utxo_set(which, address):
	if which == 'Testnet':
		resp = requests.get('https://testnet.blockchain.info/unspent?active=%s' % address)
		utxo_set = json.loads(resp.text)["unspent_outputs"]
	else:
		i = 0
		utxo_set = pp.get_data('utxo.pickle')
		if utxo_set != False:
			utxo_set = json.loads(utxo_set)
			for elem in utxo_set:
				if (elem['address'] == address):
					utxo_set = elem['unspent_outputs']
					i = 1
					break
		if i != 1:
			utxo_set = 0
	return utxo_set


def check_balance(utxo_set):
	# utxo_set = pp.get_data('utxo.pickle')
	if utxo_set != False:
		# utxo_set = json.loads(utxo_set)
		balance = 0
		for utxo in utxo_set:
			balance += int(utxo['value'])
		return balance
	return 0

def get_inputs_info(utxo_set, amount):
	balance = 0
	inputs_info = []
	for elem in utxo_set:
		if balance < amount:
			balance += int(elem['value'])
			inputs_info.append(elem)
		else:
			break
	return inputs_info, balance

