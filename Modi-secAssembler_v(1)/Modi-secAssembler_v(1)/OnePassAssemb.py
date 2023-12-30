import csv
from node import Node,LinkedList

INSTR_OPCODE = {
 "ADD": "18","AND": "40","COMP": "28","DIV" : "24","J" : "3C","JEQ" : "30",
 "JGT" : "34","JLT" : "38","JSUB" : "48","LDA" : "00","LDCH" : "50","LDL" : "08",
 "LDX" : "04","MUL" : "20","OR" : "44","RD" : "D8","RSUB" : "4C","STA" : "0C" ,
 "STCH" : "54","STL" : "14","STSW" : "E8","STX" : "10","SUB" : "1C",
 "TD" : "E0","TIX" : "2C","WD" : "DC","FIX" : "C4","FLOAT" : "C0","HIO" : "F4",
 "NORM" : "C8","SIO" : "F0","TIO" : "F8"
}
Format_one=["FIX","FLOAT","HIO","NORM","SIO","TIO"]
def b2h(x):
   decimal_number = int(x, 2)
   hex_number = hex(decimal_number)[2:]
   return(hex_number)

def peek_next_line(file_path, current_line_number):
    with open(file_path, 'r') as file:
        # Use islice to get to the next line without moving the cursor
        from itertools import islice
        next_line = next(islice(file, current_line_number, current_line_number + 2), None)
    return next_line

Symtab={}
OPcodes=[]
locctr=0
Trecords=[]
Hrecord=""
MaskBits=""
proglen="000000"
progstrt=0
Rflag=0
Bflag=0
STRT=""
Pstrt=''
Foundflag=0
c=1
locadd=0
INDEXFLAG=0
IMMFLAG=0
IN_file=open("Input.txt","r")
file_iterator = iter(IN_file)
for line in IN_file: #reading from input file line by line
    parts = line.split()
    if parts: #Checking whether it is an empty line or not
        if len(parts)>1: #Checking whether the instruction contains more than one string
            if parts[1].upper() == 'START': 
                locctr = int(parts[2], 16)
                progstrt=locctr
                STRT="00"+parts[2]
                Pstrt=STRT
                Hrecord="H^"+(parts[0].ljust(6)[:6])+"^00"+parts[2]+"^"
            #computing the length
            elif parts[0].upper() == 'END':
                proglen=hex(locctr-progstrt)[2:].zfill(6)
                Hrecord+=proglen
                Pstrt=Symtab[parts[1]]
            #handling the word instructions
            elif parts[1].upper() =='WORD':
                MaskBits+="0"
             
                if parts[0] in Symtab:
                    if  not isinstance(Symtab[parts[0]],str):
                        Foundflag=1

                else:
                    Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
            
                OPcodes.append(hex(int(parts[2]))[2:].zfill(6))
                locadd=3
                locctr+=locadd
            #handling the byte instruction
            elif parts[1].upper() =='BYTE':
                MaskBits+="0"
                if parts[0] in Symtab:
                    if  not isinstance(Symtab[parts[0]],str):
                        Foundflag=1
                
                else:
                    Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                if parts[2][0] == 'X':
                    #Bflag=1
                    value = parts[2][2:-1]
                    print(value)
                    OPcodes.append(value)
                    locadd=len(value) // 2
                    locctr += locadd
                    #################################################################################
                    ################################################################
                    peek=peek_next_line("Input.txt",c).split()
                    if(locadd!=3 and peek[1]!="RESW" and peek[1] !="RESB"):
                        Bflag=0
                elif parts[2][0] == 'C':
                    value = parts[2][2:-1].encode('utf-8').hex()
                    OPcodes.append(value)
                    locadd=len(value) // 2
                    locctr += locadd
                    ###############################################
                    ##########################################
                    peek=peek_next_line("Input.txt",c).split()
                    if(locadd!=3 and peek[1]!="RESW" and peek[1] !="RESB"):
                        Bflag=0
            elif parts[1].upper() == 'RESW':
            
                peek=peek_next_line("Input.txt",c).split()
                if peek[1] !="RESW" and peek[1] !="RESB":
                    Rflag=1
                
                if parts[0] in Symtab: 
                    if  not isinstance(Symtab[parts[0]],str):
                        Foundflag=1

                else:
                    Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                locadd=3 * int(parts[2])
                locctr+= locadd

            elif parts[1].upper() == 'RESB':
                peek=peek_next_line("Input.txt",c).split()
                if peek[1] !="RESW" and peek[1] !="RESB":
                    Rflag=1

                if parts[0] in Symtab:
                    if  not isinstance(Symtab[parts[0]],str):
                        Foundflag=1

                else:
                    Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                locadd=int(parts[2])
                locctr+= locadd
          
        if parts[0].upper() in INSTR_OPCODE :
            if  parts[0].upper() not in Format_one:
                MaskBits+="1"
                op=INSTR_OPCODE[parts[0]]
                ref=""
                if parts[0]=="RSUB":
                    op+="0000"
                    MaskBits=MaskBits[:-1]
                    MaskBits+="0"

                elif parts[1][-2:] == ",X":
                    ref=parts[1][:-2]
                    INDEXFLAG=1
                elif parts[1][1] !="#":
                    ref=parts[1]
                    INDEXFLAG=0
                if len(parts)>1:
                    if parts[1][0] =="#":
                        IMMFLAG=1
                        clear=int(op,16)+1
                        op=hex(clear)[2:].zfill(2)
                        op+=parts[1][1:5].zfill(4)
                        print(op)
                        MaskBits=MaskBits[:-1]
                        MaskBits+="0"
                    else:
                        IMMFLAG=0

                if ref in Symtab and isinstance(Symtab[ref],str) : 
                    if INDEXFLAG :
                        Sym=int(Symtab[ref],16)+pow(2,15)
                        Sym=hex(Sym)[2:].zfill(4)
                        op+=Sym
                    else:
                        op+=Symtab[ref]
            
                elif ref !="" and IMMFLAG==0:
                    op+="0000"
                    if ref not in Symtab:
                        Symtab[ref]=LinkedList()
                        Symtab[ref].append(hex(locctr)[2:].zfill(4))
                    else:
                        Symtab[ref].append(hex(locctr)[2:].zfill(4))

                OPcodes.append(op)
                locadd=3
                locctr += locadd
            else:
                #############################################################
                ################################################3
                peek=peek_next_line("Input.txt",c).split()
                if(peek[0]!="RESW" and peek[0] !="RESB"):
                    Bflag=0
                #Bflag=1
                ###############################
                MaskBits+="0"
                op=INSTR_OPCODE[parts[0]]
                OPcodes.append(op)
                locadd=1
                locctr+=locadd

        if len(parts)>1:
            if parts[1].upper() in INSTR_OPCODE:
                if  parts[1].upper() not in Format_one:
                    MaskBits+="1"
                    if parts[0] in Symtab:
                        if not isinstance(Symtab[parts[0]],str):
                            Foundflag=1
                    else:
                        Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                    op=INSTR_OPCODE[parts[1]]

                    ref=""
                    #handling the indexed instructions
                    if parts[2][-2:] == ",X":
                        ref=parts[2][:-2]
                        INDEXFLAG=1
                    elif parts[1][1] !="#":
                        ref=parts[2]
                        INDEXFLAG=0

                    if len(parts)>1:
                        #handling the immediate instructions
                        if parts[1][0] =="#":
                            IMMFLAG=1
                            op+=parts[1][1:5].zfill(4)
                            print(op)
                            MaskBits=MaskBits[:-1]
                            MaskBits+="0"
                        else:
                            IMMFLAG=0

                    if ref in Symtab and isinstance(Symtab[ref],str) :

                        if INDEXFLAG :
                            Sym=int(Symtab[ref],16)+pow(2,15)
                            Sym=hex(Sym)[2:].zfill(4)
                            op+=Sym
                        else:
                            op+=Symtab[ref]
            
                    elif ref !="" and IMMFLAG==0:
                        op+="0000"
                        if ref not in Symtab: #Create a linked list to store the location of the unfound symbol
                            Symtab[ref]=LinkedList()
                            Symtab[ref].append(hex(locctr)[2:].zfill(4))
                        else:
                            Symtab[ref].append(hex(locctr)[2:].zfill(4))
                    OPcodes.append(op)
                    locadd=3
                    locctr += locadd
                else:
                    Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                    peek=peek_next_line("Input.txt",c).split()
                    #if(peek[1]!="RESW" and peek[1] !="RESB"):
                        #Bflag=1
                    Bflag=1
                    MaskBits+=0
                    op=INSTR_OPCODE[parts[1]]
                    OPcodes.append(op)
                    locadd=1
                    locctr+=locadd

        #stop reading and start writing Trecord in temproray array if opcodes count are 10 or the program ends 
        #or we got reserves or we got a one byte instruction
        
        if len(OPcodes) ==10 or parts[0].upper()=="END" or Rflag==1 or Bflag ==1 or Foundflag==1:

            #reseting one byte opcode flag
            if Bflag==1:
                Bflag=0
            
            #removing extra opcode in the array
            v=""
            m=""
            if  Foundflag==1 and (parts[1]!="RESW" and  parts[1]!="RESB"):
                v=OPcodes.pop()
                locctr-=len(v)//2
                m=MaskBits[-1]
                MaskBits=MaskBits[:-1]

            MaskBits=MaskBits.ljust(12, '0')
            Top=""
            for i in OPcodes:
                Top+=i
            if OPcodes:
                T ="T^"+STRT+"^"+hex(len(Top)//2)[2:].zfill(2)+"^"+b2h(MaskBits).zfill(3)+"^"+Top
            MaskBits=''
            STRT=hex(locctr)[2:].zfill(6)
            if  T not in Trecords:
                Trecords.append(T)
            OPcodes=[]
            if  Foundflag==1 and (parts[1]!="RESW" and  parts[1]!="RESB"):
                OPcodes.append(v)
                locctr+=len(v)//2
                MaskBits+=m

            if Foundflag==1:
                locctr-=locadd
                while Symtab[parts[0]].head:
                    dt= Symtab[parts[0]].get_last_element()
                    dt=hex(int(dt,16)+1)[2:].zfill(6)
                    T="T^"+dt+"^02^000^"+hex(locctr)[2:].zfill(4)
                    Trecords.append(T)
                    Symtab[parts[0]].delete_last_node()
                Symtab[parts[0]]=hex(locctr)[2:].zfill(4)
                locctr+=locadd
                
            #adding removed opcode again in the new loop array  and resetting reserve flag
            if  Foundflag==1:
                Foundflag=0
            if Rflag==1:
                Rflag=0
    c+=1

IN_file.close()

Erecoed="E^"+Pstrt

#writing HTE records in the file
HTE=open("Output.txt","w")
HTE.write(Hrecord+"\n")
for i in Trecords:
    HTE.write(i+"\n")
HTE.write(Erecoed)
HTE.close()

#writing sympol table in file
Sym=open("SymbolTable.txt","w")
writer = csv.writer(Sym, delimiter='\t')
writer.writerow(['Symbol', 'Address'])
for key, value in Symtab.items():
    writer.writerow([key, value])
Sym.close()