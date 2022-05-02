import json
from erdpy.accounts import Address
from formatter import Formatter
from const import *


class ABI_Interpreter (Formatter):

    def __init__(self, abi_filename) :

        abi = json.loads(open(abi_filename).read())
        self.custom_types = abi["types"]
        self.endpoints = abi["endpoints"]


    def decode_vector(self, vector_raw, element_size) :

        pointer_shift = SIMPLE_DATA_SIZE["size"]


        size_vector = self.hex_to_num(vector_raw[:pointer_shift])

        if size_vector==0 : 
            return 0, pointer_shift 
        
        vec_output = []
        vector_raw = vector_raw[pointer_shift:]
        for element_index in range(size_vector) : 
            element_raw = vector_raw[element_size*element_index:
                                     element_size*(element_index+1)]

            
            vec_output.append(self.hex_to_num(element_raw))
            pointer_shift+=element_size

        return vec_output, pointer_shift


    def decode_struct(self, struct_raw, struct_abi) : 
        

        data_index = 0
        pointer = 0
        struct = {}
        while True : 

            data_type = struct_abi[data_index]["type"]
            data_name= struct_abi[data_index]["name"]

            if (data_type == "bytes"):  

                size_bytes = 2*self.hex_to_num(struct_raw[pointer:pointer+SIMPLE_DATA_SIZE["size"]])
                pointer += SIMPLE_DATA_SIZE["size"]
                struct[data_name] = self.hex_to_text(struct_raw[pointer: pointer+size_bytes])
                pointer += size_bytes

            elif (data_type == "BigUint"):

                size_bigUint = 2*self.hex_to_num(struct_raw[pointer:pointer+SIMPLE_DATA_SIZE["size"]])
                pointer += SIMPLE_DATA_SIZE["size"]
                struct[data_name] = self.BigInt_to_int(self.hex_to_num(struct_raw[pointer: pointer+size_bigUint]), DECIMALS["EGLD"])
                pointer += size_bigUint

            elif (data_type == "Address") :

                struct[data_name] = Address(struct_raw[pointer: pointer+ADDRESS_SIZE]).bech32()
                pointer+=ADDRESS_SIZE

            elif (data_type in SIMPLE_DATA_SIZE) : 

                struct[data_name] = self.hex_to_num(struct_raw[pointer: pointer+SIMPLE_DATA_SIZE[data_type]]) 
                pointer += SIMPLE_DATA_SIZE[data_type]

            elif ("List" in data_type) : # Doesn't handle nested list and list of complex type (i.e. EsdtTokenPayment)

                element_size = SIMPLE_DATA_SIZE[data_type.split("<")[1].split(">")[0]]
                struct[data_name], pointer_shift = self.decode_vector(struct_raw[pointer:], element_size)
                pointer+=pointer_shift

            else :
                print("ERROR: format not recognized yet")

            data_index+=1
            if pointer == len(struct_raw) : 
                break
        
        return struct



    def decode_enum(self, enum_raw, enum_abi) : 
        # Not implemented yet
        pass    


    def decode_custom_type(self, type_name, data_raw) :

        data = None
        abi_custom_type = self.custom_types[type_name]

        if abi_custom_type["type"] == "struct" :

            data = self.decode_struct(data_raw, abi_custom_type["fields"])

        elif abi_custom_type["type"] == "enum" :

            data = self.decode_enum(data_raw, abi_custom_type["variants"])

        else :
            print("ERROR : custom type not recognized")

        return data


    
