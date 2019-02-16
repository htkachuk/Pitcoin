import wallet
import binascii
import miner_cli
import wallet_cli

privkey_1 = wallet.get_private_key()
privkey_2 = wallet.get_private_key()
privkey_3 = wallet.get_private_key()
print("Privkey 1:",privkey_1)
print("Privkey 2:",privkey_2)
print("Privkey 3:",privkey_3)

wif1 = wallet.convert_to_WIF(privkey_1).decode()
wif2 = wallet.convert_to_WIF(privkey_2).decode()
wif3 = wallet.convert_to_WIF(privkey_3).decode()
print("WIF key 1:",wif1)
print("WIF key 2:",wif2)
print("WIF key 3:",wif3)

with open('minerkey', 'w') as f:
	f.write(wif1)
with open('wif1', 'w') as f:
	f.write(wif1)
with open('wif2', 'w') as f:
	f.write(wif2)
with open('wif3', 'w') as f:
	f.write(wif3)

publkey_1 = wallet.get_public_key(privkey_1)
publkey_2 = wallet.get_public_key(privkey_2)
publkey_3 = wallet.get_public_key(privkey_3)

with open('publkey_1', 'w') as f:
	f.write(publkey_1)
with open('publkey_2', 'w') as f:
	f.write(publkey_2)
with open('publkey_3', 'w') as f:
	f.write(publkey_3)

walletcli = wallet_cli.Cli()
minercli = miner_cli.Cli()

for i in range(10):
	minercli.do_mine("")

# walletcli.do_import('wif1')
# walletcli.do_send('-p ' + wallet.get_bitcoin_address_from_public_key(publkey_1) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_2) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_3) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_1) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_2) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_3) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_1) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_2) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_3) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_1) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_2) + ' ' + str(10))
# walletcli.do_send('send -p ' + wallet.get_bitcoin_address_from_public_key(publkey_3) + ' ' + str(10))