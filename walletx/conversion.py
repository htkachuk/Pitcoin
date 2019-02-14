import ecdsa

#returns the coordinate pair resulting from EC point multiplication 
#(repeated application of the EC group operation) of the secp256k1 base point with the integer p.
def point(p: int):
	sk = ecdsa.SigningKey.from_string(ser_256(p), curve=ecdsa.SECP256k1)
	vk = sk.get_verifying_key()
	return 

# serialize a 32-bit unsigned integer i as a 4-byte sequence, most significant byte first.
def ser_32(i):
	return i.to_bytes(length = 4, byte_order = 'big')

# serializes the integer p as a 32-byte sequence, most significant byte first
def ser_256(p):
	return p.to_bytes(length = 32, byte_order = 'big')

# serializes the coordinate pair P = (x,y) as a byte sequence using SEC1's compressed
#  form: (0x02 or 0x03) || 
def ser_p(P):
	key = P[2:66]
	if (int(key[len(key) - 1], 16) % 2 != 0):
		compressed_key = '03' + key
	else:
		compressed_key = '02' + key
	return compressed_key

# interprets a 32-byte sequence as a 256-bit number, most significant byte first.
def parse_256(p):
	return int.from_bytes(p, 'big')




