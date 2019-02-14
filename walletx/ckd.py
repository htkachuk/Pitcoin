import hmac
from hashlib import sha512
import conversion as cn

def ckpd_priv(k, c, i):
	if i >= pow(2, 31):
		I = hmac.new(c, '00' + cn.ser_256(k) + cn.ser_32(i), sha512)
	else:
		I = hmac.new(c, cn.ser_p(cn.point(k)) + cn.ser_32(i), sha512)

