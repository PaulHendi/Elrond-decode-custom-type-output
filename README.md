# Elrond-decode-custom-type-output
Python script to decode custom types (Struct and enum) using the corresponding ABI


## Librairies

[Erdpy](https://docs.elrond.com/sdk-and-tools/erdpy/installing-erdpy/) 


## How to 

You can follow examples with the provided ABI examples, and the hex output in the main.py file. 

For example : 

`python3 main.py --abi dao.abi.json --hex 0000000b44414f5f7574696c69747900000002000000010000000100000001000000020000000000 --type_name Proposal`

gives the output : 

`{'name': 'DAO_utility', 'propositions': 2, 'votes': [1], 'weights': [2], 'has_ended': 0, 'result': 0}`

All ABI files (json files) need to be placed in the JSON folder, and there's no need to specify the path with the --abi argument.


## Note

This work is still in progress. There are many things that the decoder doesn't handle yet, i.e. nested list or special types like EsdtTokenPayment.

Note also that if you use Python 3.10, you could replace all the "if" with a matching pattern, and this would be more elegant.
