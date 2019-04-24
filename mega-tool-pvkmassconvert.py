
import binascii, hashlib, base58, sys, ecdsa, codecs
arq1 = open('list-WIF-Uncompressed.txt', 'w')
arq2 = open('list-WIF-Compressed.txt', 'w')
arq3 = open('list-Addresses-Uncompressed.txt', 'w')
arq4 = open('list-Addresses-Compressed.txt', 'w')
arq5 = open('list-AllOrdened.txt', 'w')

#Header order info
arq5.write("      Address Uncompressed          |        Address Compressed           |                    Private Key WIF                   |              Private Key WIF Compressed \n")

def convert_pvk_Hex_to_WIF_Uncompressed(z):
    # Step 1: get the privatekey in extended format, this is hexadecimal upper or lower case.
    private_key_static = z
    # Step 2: adding 80 in the front for select de MAINNET channel bitcoin address
    extended_key = "80"+private_key_static
    # Step 3: first process SHA-256
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    # Step 4: second process SHA-256
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # Step 5-6: add checksum info to end of extended key
    final_key = extended_key+second_sha256[:8]
    # Step 7: finally the Wallet Import Format (WIF) is generated in the format base 58 encode of final_key
    WIF = base58.b58encode(binascii.unhexlify(final_key))
    # Step 8: show the private key on usual format WIF for wallet import. Enjoy!
    print "Private Key WIF Uncompress: " + WIF
    arq1.write("%s \n" % WIF)
    arq5.write("%s    " % WIF)

def convert_pvk_Hex_to_WIF_Compressed(z):
    # Step 1: get the privatekey in extended format, this is hexadecimal upper or lower case.
    private_key_static = z
    # Step 2: adding 80 in the front for select de MAINNET channel bitcoin address
    extended_key = "80"+private_key_static+'01'
    # Step 3: first process SHA-256
    first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
    # Step 4: second process SHA-256
    second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
    # Step 5-6: add checksum info to end of extended key
    final_key = extended_key+second_sha256[:8]
    # Step 7: finally the Wallet Import Format (WIF) is generated in the format base 58 encode of final_key
    WIFc = base58.b58encode(binascii.unhexlify(final_key))
    # Step 8: show the private key on usual format WIF for wallet import. Enjoy!
    print "Private Key WIF Compressed: " + WIFc
    arq2.write("%s \n" % WIFc)
    arq5.write("%s    \n" % WIFc)


#Step 1 - get the public_key of private_key, the result is string hex, 512 bits pubkey
def conv_pvkhex_to_bitcoinaddress_uncompressed(z):

    zk = ecdsa.SigningKey.from_string(z.decode('hex'), curve=ecdsa.SECP256k1)
    zk_verify = zk.verifying_key

    #result
    z_public_key = ('\04' + zk.verifying_key.to_string()).encode('hex')
   
    #first_sha256 = hashlib.sha256(binascii.unhexlify(z_public_key)).hexdigest()

    #Step 2 - Making SHA-256 of pub_key and using this first_sha256 for make RIPEMD-160
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(z_public_key.decode('hex')).digest())
    ripemd160_result = ripemd160.hexdigest()

    #Step 3 - Adding network bytes on start of result of Step 2
    step3 =  '00' + ripemd160_result
    
    #Step 4 - Making SHA-256 of RIPEMD-160 with network bytes included
    second_sha256 = hashlib.sha256(binascii.unhexlify(step3)).hexdigest()

    #Step 5 - Making SHA-256 of second_sha256
    third_sha256 = hashlib.sha256(binascii.unhexlify(second_sha256)).hexdigest()

    #Step 6 - Get the first 4 bytes of third_sha256
    step6 = third_sha256[:8]

    #Step 7 - Adding the 4 bytes of Step 6 at the end of Step3 to get the final Hex data needed
    step7 = step3+step6

    #Step8 - Making the Base58 encoding of Step 6 to get Bitcoin Public Address
    bitcoin_uncompressed_address_std = base58.b58encode(binascii.unhexlify(step7))
    print "Bitcoin Address Uncompress: " + bitcoin_uncompressed_address_std
    arq3.write("%s \n" % bitcoin_uncompressed_address_std)
    arq5.write("%s    " % bitcoin_uncompressed_address_std)

def conv_pvkhex_to_bitcoinaddress_compressed(z):

    pvk_to_bytes = codecs.decode (z, 'hex')
    
    #Get the ECDSA public key

    key = ecdsa.SigningKey.from_string (pvk_to_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')

    if(ord(bytearray.fromhex(key_hex[-2:])) % 2 == 0):
        #The last byte of value for Y is Pair, this require add '02' at first

        public_key_compressed = '02' + key_hex[0:64]

        #Making SHA-256 of pubkey compressed and making RIPEMD-160 of this
        public_key_in_bytes = codecs.decode(public_key_compressed, 'hex')
        sha256_public_key_compressed = hashlib.sha256(public_key_in_bytes)
        sha256_public_key_compressed_digest = sha256_public_key_compressed.digest()

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_public_key_compressed_digest)
        ripemd160_digest = ripemd160.digest()
        ripemd160_hex = codecs.encode(ripemd160_digest, 'hex')

        #Adding network bytes 0x00
        public_key_compressed_bitcoin_network = b'00' + ripemd160_hex
        public_key_compressed_bitcoin_network_bytes = codecs.decode(public_key_compressed_bitcoin_network, 'hex')

        #Making Checksum for MainNet, this is SHA-256 2x turns and get the firsts 4 bytes
        sha256_one = hashlib.sha256(public_key_compressed_bitcoin_network_bytes)
        sha256_one_digest = sha256_one.digest()
        sha256_two = hashlib.sha256(sha256_one_digest)
        sha256_two_digest = sha256_two.digest()
        sha256_2_hex = codecs.encode(sha256_two_digest, 'hex')
        checksum = sha256_2_hex[:8]

        bitcoin_compressed_address_hex = (public_key_compressed_bitcoin_network + checksum).decode('utf-8')
        bitcoin_compressed_address = base58.b58encode(binascii.unhexlify(bitcoin_compressed_address_hex))
        arq4.write("%s \n" % bitcoin_compressed_address)
        arq5.write("%s    " % bitcoin_compressed_address)
        print "Bitcoin Address Compressed: " + bitcoin_compressed_address

    else:
        #The last byte of value for Y is Odd, this require add '03' at first

        public_key_compressed = '03' + key_hex[0:64]

        #Making SHA-256 of pubkey compressed and making RIPEMD-160 of this
        public_key_in_bytes = codecs.decode(public_key_compressed, 'hex')
        sha256_public_key_compressed = hashlib.sha256(public_key_in_bytes)
        sha256_public_key_compressed_digest = sha256_public_key_compressed.digest()

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_public_key_compressed_digest)
        ripemd160_digest = ripemd160.digest()
        ripemd160_hex = codecs.encode(ripemd160_digest, 'hex')

        #Adding network bytes 0x00
        public_key_compressed_bitcoin_network = b'00' + ripemd160_hex
        public_key_compressed_bitcoin_network_bytes = codecs.decode(public_key_compressed_bitcoin_network, 'hex')

        #Making Checksum for MainNet, this is SHA-256 2x turns and get the firsts 4 bytes
        sha256_one = hashlib.sha256(public_key_compressed_bitcoin_network_bytes)
        sha256_one_digest = sha256_one.digest()
        sha256_two = hashlib.sha256(sha256_one_digest)
        sha256_two_digest = sha256_two.digest()
        sha256_2_hex = codecs.encode(sha256_two_digest, 'hex')
        checksum = sha256_2_hex[:8]

        bitcoin_compressed_address_hex = (public_key_compressed_bitcoin_network + checksum).decode('utf-8')
        bitcoin_compressed_address = base58.b58encode(binascii.unhexlify(bitcoin_compressed_address_hex))
        arq4.write("%s \n" % bitcoin_compressed_address)
        arq5.write("%s    " % bitcoin_compressed_address)
        print "Bitcoin Address Compressed: " + bitcoin_compressed_address
 

with open("brute-pvks.txt") as file:
    for line in file:

        pvk_hexadecimal = str.strip(line)
        print "__________________________________________________\n"
        print "Converting pvk: " + pvk_hexadecimal
        
        conv_pvkhex_to_bitcoinaddress_uncompressed(pvk_hexadecimal)
        conv_pvkhex_to_bitcoinaddress_compressed(pvk_hexadecimal)
        convert_pvk_Hex_to_WIF_Uncompressed(pvk_hexadecimal)
        convert_pvk_Hex_to_WIF_Compressed(pvk_hexadecimal)        



print "__________________________________________________\n"
print "Developed by: ~geniusprodigy"
print "My contact on reddit: reddit.com/u/genius360\n"
print "If this saved you time or helped, donations please for BTC Address:"
print "1FrRd4iZRMU8i2Pbffzkac5u4KwUptmc7S"



#Run with python 2.7

#Usage
#python mega-tool-pvkmassconvert.py

