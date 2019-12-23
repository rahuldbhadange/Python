import hashlib
m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
print(m.digest())
print(m.hexdigest())
#b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
print(m.digest_size)
print(m.block_size)


print(hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest())
