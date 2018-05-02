# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:24:11 2018

@author: YURU
"""
import math

sic=[]
op={'ADD':['18',3],'ADDR':['90',2],'AND':['40',3],'CLEAR':['4',2],'COMP':['28',3],'DIV':['24',3],'DIVR':['9C',2],
    'FIX':['C4',1],'J':['3C',3],'JEQ':['30',3],'JGT':['34',3],'JLT':['38',3],'JSUB':['48',3],
    'LDA':['00',3],'LDB':['68',3],'LDCH':['50',3],'LDL':['8',3],'LDS':['6C',3],'LDT':['74',3],'LDX':['4',3],
    'MUL':['20',3],'MULF':['60',3],'MULR':['98',2],'OR':['44',3],'RMO':['AC',2],'RSUB':['4C',3],
    'SIO':['F0',1],'SSK':['EC',3],'STA':['0C',3],'STB':['78',3],'STCH':['54',3],
    'STF':['80',3],'STI':['D4',3],'STL':['14',3],'STS':['7C',3],'STSW':['E8',3],
    'STT':['84',3],'STX':['10',3],'SUB':['1C',3],'SUBF':['5C',3],'SUBR':['94',2],'SVC':['B0',2],
    'TD':['E0',3],'TIO':['F8',1],'TIX':['2C',3],'TIXR':['B8',2],'WD':['DC',3]}
sym={}
locctr=0

#srcfile=open(input('輸入檔案名稱(SIC.txt): '))
srcfile=open('SIC.txt')
lisfile=open('LISFILE.txt','w')
objfile=open('OBJFILE.txt','w')

for line in srcfile:
    if('\t' in line):  #需增加錯誤行
        print('Tab error')
    else:
        sic.append([line[0:9].strip(),line[9:17].strip(),line[17:].strip()])

print(sic)

for code in sic:
    if code[1]=='START':  #設定起始位置
        locctr=int(code[2],16)  #將16進位轉10進位
        code.insert(0,[locctr,str(hex(locctr))[2:].zfill(4).upper()])  #將位址(10&16進位)差在List最前方
        continue
    
    code.insert(0,[locctr,str(hex(locctr))[2:].zfill(4).upper()])  #將前一次加完之位置存在陣列前方
    if code[1].strip() and code[1]!='.':  #如果標籤不為空，儲存至SYMTAB 
        sym[code[1]]=code[0][1]
    if code[2]=='END':  
        print(code[2])
    elif code[2]=='WORD':  #直接寫出opcode
        code.append(str(hex(int(code[3])))[2:].zfill(6).upper())  #加在最後面
        locctr+=3
    elif code[2]=='BYTE':  #直接寫出opcode
        if code[3][0]=='C':  #需轉換ASCII hex(ord())
            c=''
            for x in code[3][2:-1]:
                c+=str(hex(ord(x))[2:])
            code.append(c)  #加在最後面 
            locctr+=len(code[3][2:-1])
        elif code[3][0]=='X':
            locctr+=math.ceil(len(code[3][2:-1])/2)
    elif code[2]=='RESW':  
        locctr+=3*int(code[3])
    elif code[2]=='RESB':
        locctr+=int(code[3])
    elif code[2].find(',X') != -1: #有X 
            if code[2].split(',')[0] in op:
                locctr+=op[code[2].split(',')[0]][1]
    elif code[2] in op:
        locctr+=op[code[2]][1]
    elif code[1]=='.':
        continue
    else:
        print(code,'error')


for code in sic:
    if code[2].find(',X') != -1: #有X 
        if code[2].split(',')[0] in op:
            code.append(op[code[2].split(',')[0]][0]+hex(int(sym[code[3]][0])+8)[2:].upper()+sym[code[3]][1:])
    if code[2] in op:
            code.append(op[code[2]][0]+sym[code[3]])
    
    

for code in sic:
    print(code)


srcfile.close()
lisfile.close()
objfile.close()
