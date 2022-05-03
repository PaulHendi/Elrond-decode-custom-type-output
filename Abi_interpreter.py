import json
from erdpy.accounts import Address
from formatter import Formatter
from const import *


class ABI_Interpreter (Formatter):

    def __init__(self, abi_filename) :

        abi = json.loads(open(abi_filename).read())
        self.custom_types = abi["types"]
        self.endpoints = abi["endpoints"]

        self.custom_type_names = self.custom_types.keys()


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


    def decode_struct(self, struct, struct_raw, struct_abi, data_name_above) : 
        

        data_index = 0
        pointer = 0
        if data_name_above : # We are in recursion
            struct[data_name_above] = {}
        while True : 

            data_type = struct_abi[data_index]["type"]
            data_name= struct_abi[data_index]["name"]

            #print(len(struct_abi))
            print(struct_raw[pointer:])

            if (data_type == "bytes" or data_type == "TokenIdentifier"):  

                size_bytes = 2*self.hex_to_num(struct_raw[pointer:pointer+SIMPLE_DATA_SIZE["size"]])
                pointer += SIMPLE_DATA_SIZE["size"]
                struct[data_name_above][data_name] = self.hex_to_text(struct_raw[pointer: pointer+size_bytes])
                pointer += size_bytes

            elif (data_type == "BigUint"):

                size_bigUint = 2*self.hex_to_num(struct_raw[pointer:pointer+SIMPLE_DATA_SIZE["size"]])
                pointer += SIMPLE_DATA_SIZE["size"]
                struct[data_name_above][data_name] = self.hex_to_num(struct_raw[pointer: pointer+size_bigUint]) # Can use self.BigInt_to_int(blabla, DECIMALS["EGLD"]) if necessary
                pointer += size_bigUint

            elif (data_type == "Address") :

                struct[data_name_above][data_name] = Address(struct_raw[pointer: pointer+ADDRESS_SIZE]).bech32()
                pointer+=ADDRESS_SIZE

            elif (data_type in SIMPLE_DATA_SIZE) : 

                struct[data_name_above][data_name] = self.hex_to_num(struct_raw[pointer: pointer+SIMPLE_DATA_SIZE[data_type]]) 
                pointer += SIMPLE_DATA_SIZE[data_type]

            elif ("List" in data_type) : # Doesn't handle nested list and list of complex type (i.e. EsdtTokenPayment)

                element_size = SIMPLE_DATA_SIZE[data_type.split("<")[1].split(">")[0]]
                struct[data_name_above][data_name], pointer_shift = self.decode_vector(struct_raw[pointer:], element_size)
                pointer+=pointer_shift

            elif ("Option" in data_type) :  

                nested_data_type = data_type.split("<")[1].split(">")[0]
                if nested_data_type in SIMPLE_DATA_SIZE :
             
                    element_size = SIMPLE_DATA_SIZE[nested_data_type]
                    some_or_none = struct_raw[pointer:pointer+2]
                    pointer+=2

                    if some_or_none == "00" : 
                        struct[data_name_above][data_name] = "None"
                    else :
                        struct[data_name_above][data_name] = "Some(" + str(self.hex_to_num(struct_raw[pointer:pointer+element_size])) + ")"
                
                elif nested_data_type in self.custom_type_names : 


                    some_or_none = struct_raw[pointer:pointer+2]
                    pointer+=2



                    if some_or_none == "00" : 
                        struct[data_name_above][data_name] = "None"
                    else : 
                        struct, pointer = self.decode_custom_type(struct, nested_data_type ,struct_raw[pointer:], data_name)   


            elif data_type in self.custom_type_names : 

                struct, pointer = self.decode_custom_type(struct, data_type ,struct_raw[pointer:], data_name)
                


            else :
                print("ERROR: format not recognized yet")

            print(struct)
            data_index+=1
            if data_index==len(struct_abi) :
                break
        
        return struct, pointer



    def decode_enum(self, struct, enum_raw, enum_abi) : 
        # Not implemented yet
        pass    


    def decode_custom_type(self, struct, type_name, data_raw, data_name="") :

        data = None
        abi_custom_type = self.custom_types[type_name]

        if abi_custom_type["type"] == "struct" :

            data = self.decode_struct(struct, data_raw, abi_custom_type["fields"], data_name)

        elif abi_custom_type["type"] == "enum" :

            data = self.decode_enum(struct, data_raw, abi_custom_type["variants"], data_name)

        else :
            print("ERROR : custom type not recognized")

        return data


    
