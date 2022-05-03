import argparse
import json

from Abi_interpreter import ABI_Interpreter


# ---------------------------------------------------------------- #
#                         INPUTS
# ---------------------------------------------------------------- #
parser = argparse.ArgumentParser()
parser.add_argument("--abi", help="ABI filename", required=True)
parser.add_argument("--hex", help="The hex to decode", required=True)
parser.add_argument("--type_name", help="The type of the struct or enum", required=True)


args = parser.parse_args()

abi_filename = "JSON/" + args.abi
hex_to_decode = args.hex
type_name = args.type_name

# ---------------------------------------------------------------- #
#                      DECODE HEX STRUCT
# ---------------------------------------------------------------- #

abi_interpreter = ABI_Interpreter(abi_filename)
struct = {}
output = abi_interpreter.decode_custom_type(struct, type_name, hex_to_decode, type_name)

print(json.dumps(output[0], indent=4))


# Test avec dao.abi.json
# type name : Proposal
# hex : 0000000b44414f5f7574696c6974790000000200000000000000000000000000
# hex : 0000000b44414f5f7574696c69747900000002000000010000000100000001000000020000000000 

# type name : Voter
# hex : 000000020000000000000001000000000000000200000002000000093635c9adc5dea0000001

# Test 2 avec presale.abi.json
# type name : PackageInfos
# hex : 00000008016345785d8a00000000000901158e460913d000000001

# Test 3 avec nft_trading.abi.json (marche pas, prend pas encore en compte les EsdtTokenPayment)
# type name : TxInfos
# hex : 9a8001df71aabe74c622328d077b90fc62be5972a59f2988a017e4f5c4e3ee4c
# 00000002020000000d434f4c4f52532d61343830316200000000000000010000000101020000000d434f4c4
# f52532d6134383031620000000000000002000000010100000001000000000d474f4c44454e2d64313264386200000000000000000
# 00000088ac7230489e80000


# Test 4 avec doic.json
# Type name : doic
# hex : 616363315f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f0000000c61756374696f6e5f6e616d65000000010900000001020000000445474c4400000000000186a00000000000855ca0000000010200


