# mega-tool-pvkmassconvert

Tool to convert any number of private keys from Hexadecimal format to other formats as well as get their respective Bitcoin Addresses.

I developed the tool thinking of helping to save a lot of time if you have many private keys, i too developed a tool that takes the list of Bitcoin Addresses obtained and consult the balance of each one automated. This saves the addresses that have balance in a separate list. So if you have a large amount of private keys and addresses, you can easily locate the addresses that have balance and do not spend your precious time.

Link to the balances verification tool: https://github.com/geniusprodigy/bitcoin-balance-checker

# INSTALLATION and USE

* Install Python 2.7 if you not have

Open the Command Line/Terminal and download the dependencies one by one typing:

* pip install base58
* pip install ecdsa
* pip install codecs

* Create a .txt file named "brute-pvks" and replace the directory sample file. Or edit the existing file with your private keys hex, 1 per line

* You can now run the code with: *python mega-tool-pvkmassconvert.py*

# RESULTS

Tool working: https://imgur.com/a/h8iv496

Tool results output: https://imgur.com/a/F1yL1hv

For each Hexadecimal Private Key, the script results in the Private Key in WIF, WIF Compressed, and the 2 Default Bitcoin Addresses, ie Address Compressed and Address Uncompressed.

The code will generate 5 output files:

list-Addresses-Uncompressed.txt -> List with each Bitcoin Address Uncompressed, is the default format used.

list-Addresses-Compressed.txt -> List with each Bitcoin Address Compressedd.

list-WIF-Uncompressed.txt -> List with each Private Key on WIF default format used.

list-WIF-Compressed.txt -> List with each Private Key on WIF Compressed.

list-AllOrdened.txt -> All information in the above files, organized visually better. Disable "Auto Line Break" from the Text Editor to see better.

Separate text files are for mass use in Wallet software for quick import. In order to locate through them and know which key belongs to which file, use a Text Editor that lists each line, so for example, line number 6 of each of the files will be equivalent to the data of the same hexadecimal private key that was converted, and so on successively.

Very important! Do not forget to use the balances verification tool in the "TWO GENERATED TEXT FILES", that is: * list-Addresses-Uncompressed.txt * and * list-Addresses-Compressed.txt *. This will ensure that you have not forgotten any money.

The balances check feature will be very useful especially if you do not remember which of the addresses has balance.

If you need any support, just contact me. Reddit: https://www.reddit.com/user/genius360 Email: geniusprodigy@protonmail.com

If this helped you, please leave a tip. BTC Address: 1FrRd4iZRMU8i2Pbffzkac5u4KwUptmc7S
