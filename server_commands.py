import sys
import utxo_set
import config
import pending_pool
import json
from flask import (
	Flask,
	request
	)

app = Flask(__name__)

@app.route('/transaction/new', methods=['POST'])
def submit_tx():
	if request.method == 'POST':
		next_transaction = request.get_json()
		pending_pool.database(next_transaction)
		return(next_transaction)

@app.route('/transaction/pending', methods=['GET'])
def pending_transaction():
	if request.method == 'GET':
		data = pending_pool.get_data('pool.pickle')
		if data != False:
			return data
		else:
			return("Something get wrong!\nYou have no transaction in pool")

@app.route('/chain', methods=['GET'])
def get_chain():
	if request.method == 'GET':
		data = pending_pool.get_data('chain.pickle')
		if data != False:
			return data
		else:
			return("Something get wrong!\nYou have no chain")
		

@app.route('/nodes', methods=['GET'])
def list_of_nodes():
	if request.method == 'GET':
		data = pending_pool.get_data('node.pickle')
		if data != False:
			return data
		else:
			return("Something get wrong!\nYou have no nodes")

@app.route('/chain/length', methods=['GET'])
def chain_length():
	if request.method == 'GET':
		data = pending_pool.get_data('chain.pickle')
	if data != False:
		data = json.loads(data)
		lens = str(data[0]['height'])
		return lens
	else:
		return("0")

@app.route('/block/last', methods=['GET'])
def last_block():
	if request.method == 'GET':
		data = pending_pool.get_data('chain.pickle')
		if data != False:
			data = json.loads(data)
			block = data[0]
			return json.dumps(block)
		else:
			return("Something get wrong!\nYou have no chain")

@app.route('/block', methods=['GET'])
def block_height():
	if request.method == 'GET':
		height = str(request.args.get('height'))
		data = pending_pool.get_data('chain.pickle')
		if data != False:
			data = json.loads(data)
			i = len(data) -1
			while(i >= 0):
				if (int(data[i]['height']) == int(height)):
					return data[i]



@app.route('/balance', methods=['GET'])
def get_balance():
	if request.method == 'GET':
		addr = str(request.args.get('addr'))
		setik = utxo_set.get_utxo_set("Pitcoin", addr)
		balance = utxo_set.check_balance(setik)
		return('<h1>Your balance is <font color="red">' + str(balance) + '</font> satoshi</h1>')


@app.route('/utxo', methods=['GET'])
def utxo():
	if request.method == 'GET':
		data = pending_pool.get_data('utxo.pickle')
		print(data)
		if data != False:
			return data
		else:
			return("Something get wrong!\nYou have no utxo in pool")


def main():
	PORT = input("Choose port\n")
	try:
		val = int(PORT)
		try:
			fd = open("port.txt", 'w')
			fd.write(PORT)
			fd.close()
			print("!!!Server port was saved in a file port.txt!!!")
		except IOError:
			print()
		app.run(host='localhost', port=PORT, debug=False)
	except (ValueError, PermissionError, OverflowError) as e:
		print("Invalid port, stupid")

if __name__ == '__main__':
	main()	

