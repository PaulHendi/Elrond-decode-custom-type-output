import binascii

Test = False

class Formatter:

    def hex_to_text(self, hex_string) : 

        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")

        return ascii_string


    def text_to_hex(self, text) :
        hexa = binascii.hexlify(text.encode()).decode()
        if len(hexa)%2==1 :  
            return "0" + hexa
        return hexa


    # Sometimes need to add a 0 (if it's even, to be sure that it's grouped by bytes)
    def num_to_hex(self, num) : 
        hexa = format(num, "x")
        if len(hexa)%2==1 :  
            return "0" + hexa
        return hexa     


    def hex_to_num(self, hex_string) :
        return int(hex_string, base=16)           


    def int_to_BigInt(self, num, decimals) : 
        return int(f"{num*decimals:.1f}".split(".")[0])   

    def BigInt_to_int(self, num, decimals) : 
        return num/decimals


    def interpret_bool(self, raw_data) :
        if raw_data : 
            return True
        return False

    def interpret_enum(self, raw_data) :
        if raw_data : 
            return self.hex_to_num(raw_data[0].hex)
        return 0        
        


if Test : 

    formatter = Formatter()
    print(formatter.hex_to_num("056bc75e2d63100000")) # Should return 100000000000000000000 (100*1e18)
    print(formatter.hex_to_text("474e472d386437653035")) # Should return GNG-8d7e05 (GNG fake collection ID)
    print(formatter.text_to_hex("MEX")) # Should return 4d4558
    print(formatter.int_to_BigInt(100, 1000000000000000000)) # Should return 10000000000000000
    print(formatter.num_to_hex(1)) # Should return 01 (the function handles cases when the hex is odd)
