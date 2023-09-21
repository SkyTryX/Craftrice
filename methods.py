from uuid import uuid4

def dec2bin(n: int, neg: bool) -> list[int]:
        if neg == True : n=n*-1
        decimal = n
        bin_inverse=[]
        while decimal != 0:
            bin_inverse.append(decimal % 2)
            decimal = decimal // 2
        while len(bin_inverse) < 3:
             bin_inverse.append(0)
        position=len(bin_inverse)
        binarie= []
        for i in bin_inverse:
            position-= 1
            binarie.append(bin_inverse[position])
        return binarie

def format_json(cmd:str):
    return {"header": {
                        "version": 1,
                        "requestId": f'{uuid4()}',
                        "messagePurpose": "commandRequest",
                        "messageType": "commandRequest"
                    },
                    "body": {
                        "version": 1,
                        "commandLine": cmd,
                        "origin": {
                            "type": "player"
                        }
                    }}