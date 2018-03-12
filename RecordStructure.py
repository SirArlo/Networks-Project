#SENDING
f = open('TEST (2).txt', 'r')
hex_string = ""
for line in f:
    hex_string = ""
    for x in range(0, len(line)):
        if hex(ord(line[x])) == "0xff":
            hex_string = hex_string + "ffff"
        else:
            if len(hex(ord(line[x]))[2:]) < 2 :
                hex_string = hex_string + "0"
            hex_string = hex_string + hex(ord(line[x]))[2:]
    hex_string = hex_string + "ff01"
    print(hex_string)
print("ff02\n")

#RECEIVING
f = open('TEST.txt', 'r')
output_string = ""
y = ""
flag = False
for line in f:
    for x in range(0, len(line)-2, 2):
        if flag == True:
            flag = False
            continue
        if line[x:x+2] == "ff" and line[x+2:x+4] == "ff":
            y = "ff"
            flag = True
            output_string = output_string + chr(int("0x" + y[0:1],0))
            continue
        else:
            y = line[x:x+2]
            yforward = line[x+2:x+4] 
            
        if (y + yforward) == "ff02":
            break

        if (y + yforward) == "ff01":
            output_string = output_string + " -> END-OF-RECORD\n"
            break
        else:
            output_string = output_string + chr(int("0x" + y, 0))
    if (y + yforward) == "ff02":
        print(output_string)
        print("END-OF-FILE")
        break