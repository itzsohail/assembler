import re
import streamlit as st
def remove_comments(code):
    code = re.sub(r'#.*', '', code)
    code = re.sub(r'\'\'\'(.*?)\'\'\'', '', code, flags=re.DOTALL)
    code = re.sub(r'\"\"\"(.*?)\"\"\"', '', code, flags=re.DOTALL)
    code = re.sub(r'\n\s*\n', '\n', code)
    return code.strip()
# Streamlit UI
st.title("Assembly to Machine Code Converter")
st.write("Enter your assembly code below:")

assembly_code = st.text_area("Assembly Code", height=200)
assembly_code= remove_comments(assembly_code)
myct0 = {
    "ld": "01110",
    "st": "01111"
}

myct1 = {
    "nop": "01101",
    "ret": "10100"
}
myct2 = {
    "beq": "10000",
    "bgt": "10001",
    "b": "10010",
    "call": "10011"}

myct4 = {
    "add": "00000",
    "sub": "00001",
    "mul": "00010",
    "div": "00011",
    "mod": "00100",
    "and": "00110",
    "or": "00111",
    "lsl": "01010",
    "lsr": "01011",
  "asr": "01100"}

myct3 = {
    "cmp": "00101",
    "not": "01000",
    "mov": "01001"}
myreg = {"R0": "0000",
         "r1": "0001",
         "r2": "0010",
         "r3": "0011",
         "r4": "0100",
         "r5": "0101",
         "r6": "0110",
         "r7": "0111",
         "r8": "1000",
         "r9": "1001",
         "r10": "1010",
         "r11": "1011",
         "r12": "1100",
         "r13": "1101",
         "r14": "1110",
         "r15": "1111"}
playlist = { "saksham":"10ai"}

def bina(decimal):
    if decimal >= 0:
        binary = bin(decimal)[2:].zfill(27)
    else:
        binary = bin((1 << 27) + decimal)[2:]
    return binary

def assembly(code, cot):
    cot = int(cot)
    code = code.replace(" ", ",")
    code = code.lower()
    mylist = code.split(',')
    an = len(mylist)
    bn = mylist[0]
    if mylist[0] == "ld" or mylist[0] == "st":
        if mylist[2].startswith('r'):
            return (myct0.get(mylist[0]) + '0' + myreg.get(mylist[1],"rega") + myreg.get(mylist[3],"rega") + myreg.get(mylist[2],"rega") + ("0" * 14))
        else:
            return (myct0.get(mylist[0]) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[3],"rega") + mylist[2] + ("0" * 14))

    elif an == 1:
        if len(myct1.get(code, bn.zfill(5)) + ("0" * 27))==32:
             return (myct1.get(code, bn.zfill(5)) + ("0" * 27))
        return
    elif (an == 2):
        return (myct2.get(mylist[0], bn.zfill(5)) + bina(int(playlist[mylist[1]]) - cot))

    elif (an == 4):
        if mylist[3].startswith('r'):
            return (myct4.get(mylist[0], bn.zfill(5)) + '0' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega") + myreg.get(mylist[3],"rega") + ("0" * 14))
        elif mylist[0][:2] != "or":

            if (len(mylist[0]) == 4 and mylist[0][3] == "h"):
                return(myct4.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"10" + f'{int(mylist[3]):016b}')
            elif (len(mylist[0]) == 4 and mylist[0][3] == "u"):
                return(myct4.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"01" + f'{int(mylist[3]):016b}')
            else:
                return(myct4.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"00" + f'{int(mylist[3]):016b}')
        else:

            if (len(mylist[0]) == 3 and mylist[0][2] == "h"):
                return(myct4.get(mylist[0][:2], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"10" + f'{int(mylist[3]):016b}')
            elif (len(mylist[0]) == 3 and mylist[0][2] == "u"):
                return(myct4.get(mylist[0][:2], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"01" + f'{int(mylist[3]):016b}')
            else:
                return(myct4.get(mylist[0][:2], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega")+"00" + f'{int(mylist[3]):016b}')

    if (an == 3):
        if mylist[0] == "mov" or mylist[0] == "movh" or mylist[0] == "movu" or mylist[0] == "not" or mylist[
            0] == "noth" or mylist[0] == "notu":
            if mylist[2].startswith('r'):
                return(myct3.get(mylist[0], bn.zfill(5)) + '0' + myreg.get(mylist[1],"rega") + ("0" * 4) + myreg.get(mylist[2],"rega") + ("0" * 14))
            else:

                if len(mylist[0]) == 4 and mylist[0][3] == "h":
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + ("0" * 4)+"10" + f'{int(mylist[2]):016b}')
                elif len(mylist[0]) == 4 and mylist[0][3] == "u":
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + ("0" * 4)+"01" + f'{int(mylist[2]):016b}')
                else:
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + myreg.get(mylist[1],"rega") + ("0" * 4)+"00" + f'{int(mylist[2]):016b}')
        elif mylist[0] == "cmp" or mylist[0] == "cmph" or mylist[0] == "cmpu":
            if mylist[2].startswith('r'):
                return(myct3.get(mylist[0], bn.zfill(5)) + ('0' * 5) + myreg.get(mylist[1],"rega") + myreg.get(mylist[2],"rega") + ("0" * 14))
            else:

                if len(mylist[0]) == 4 and mylist[0][3] == "h":
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + ("0" * 4) + myreg.get(mylist[1],"rega")+"10" + f'{int(mylist[2]):016b}')
                elif len(mylist[0]) == 4 and mylist[0][3] == "u":
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + ("0" * 4) + myreg.get(mylist[1],"rega")+"01" + f'{int(mylist[2]):016b}')
                else:
                    return(myct3.get(mylist[0][:3], bn.zfill(5)) + '1' + ("0" * 4) + myreg.get(mylist[1],"rega")+"00" + f'{int(mylist[2]):016b}')
        else:
            return(code)


if st.button("Convert to Machine Code"):
    instruction_lines = assembly_code.split("\n")
    lines = []
    cin = 0
    machinecode=[]
    for b in instruction_lines :
       # if b.lower() == "exit":
        #   break
        if b.count(":") == 1:
           playlist.update({b[:(b.find(":"))]: cin})
        b = b[((b.find(":")) + 1):]
        lines.append(b)
        cin += 1
    cin = 0
    for i in lines:
       machinecode.append( assembly(i, cin))
       cin += 1
    st.write("### Machine Code Output")
    st.code("\n".join(machinecode), language="plaintext")

