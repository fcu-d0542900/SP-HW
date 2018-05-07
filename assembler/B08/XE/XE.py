# -*- coding: utf-8 -*-
"""
Created on Wed May  2 19:23:16 2018

@author: YURU
"""

import math
import sys

xe=[]  #程式碼儲存
op={'ADD':['18',3],'ADDF':['58',3],'ADDR':['90',2],'AND':['40',3],
    'CLEAR':['4',2],'COMP':['28',3],'COMPF':['88',3],'COMPR':['A0',2],
    'DIV':['24',3],'DIVF':['64',3],'DIVR':['9C',2],'FIX':['C4',1],'FLOAT':['C0',1],'HIO':['F4',1],
    'J':['3C',3],'JEQ':['30',3],'JGT':['34',3],'JLT':['38',3],'JSUB':['48',3],
    'LDA':['00',3],'LDB':['68',3],'LDCH':['50',3],'LDF':['70',3],'LDL':['08',3],'LDS':['6C',3],'LDT':['74',3],'LDX':['04',3],'LPS':['D0',3],
    'MUL':['20',3],'MULF':['60',3],'MULR':['98',2],'NORM':['C8',1],'OR':['44',3],'RD':['D8',3],'RMO':['AC',2],'RSUB':['4C',3],
    'SHIFTL':['A4',2],'SHIFTR':['A8',2],'SIO':['F0',1],'SSK':['EC',3],'STA':['0C',3],'STB':['78',3],'STCH':['54',3],'STF':['80',3],
    'STI':['D4',3],'STL':['14',3],'STS':['7C',3],'STSW':['E8',3],'STT':['84',3],'STX':['10',3],'SUB':['1C',3],'SUBF':['5C',3],'SUBR':['94',2],'SVC':['B0',2],
    'TD':['E0',3],'TIO':['F8',1],'TIX':['2C',3],'TIXR':['B8',2],'WD':['DC',3]}
sym={}  #SYMTAB
locctr=0

#file=input('輸入檔案名稱(XE.txt): ')
file='XE.txt'
srcfile=open(file)  #開檔
lisfile=open(file.split('.')[0]+'_LISFILE.txt','w')
objfile=open(file.split('.')[0]+'_OBJFILE.txt','w')

print('\n輸入之SIC程式碼:')
for line in srcfile:
    print(line,end='')
    if '\t' in line:  #需增加錯誤行
        print(' ****Tab error !')
        lisfile.write(' ****Tab error !\n')
        sys.exit('Tab error !')
    if '.' in line:
        xe.append(['.',line.split('.')[1].strip()])
    else:
        xe.append([line[0:8].strip().upper(),line[8:17].strip().upper(),line[17:].strip().upper()])  #分割儲存字串
print()

for code in xe:  #計算位址
    if code[0]=='.':  #省略註解行
        continue
    if code[1]=='START':  #設定起始位置
        locctr=int(code[2],16)  #將16進位轉10進位
        code.insert(0,[locctr,str(hex(locctr))[2:].zfill(4).upper()])  #將位址(10&16進位)差在List最前方
        code.append('')
        continue
    code.insert(0,[locctr,str(hex(locctr))[2:].zfill(4).upper()])  #將前一次加完之位置存在陣列前方
    if code[1].strip() and code[1]!='.':  #如果標籤不為空，儲存至SYMTAB 
        sym[code[1]]=code[0][1]
    if code[2]=='END':  #遇到END則結束
        code.append(sym[code[3]].zfill(6))
        break
    elif code[2]=='WORD':  #直接寫出opcode並加在List最後面
        code.append(str(hex(int(code[3])))[2:].zfill(6).upper())  #轉換數字成16進位並補0
        locctr+=3  #每個WORD位址加3
    elif code[2]=='BYTE':  #直接寫出opcode並加在List最後面
        if code[3][0]=='C':  #將字元轉換成ASCII hex(ord())
            c=''
            for x in code[3][2:-1]:  #字元一一轉換
                c+=str(hex(ord(x))[2:])
            code.append(c)
            locctr+=len(code[3][2:-1])
        elif code[3][0]=='X':
            locctr+=math.ceil(len(code[3][2:-1])/2)  #math.ceil 無條件進位
    elif code[2]=='RESW':  
        code.append('')
        locctr+=3*int(code[3])
    elif code[2]=='RESB':
        code.append('')
        locctr+=int(code[3])
    elif code[2].find('+') != -1:
        locctr+=4
    elif code[2].find(',X') != -1:  #有X之OPCODE
            if code[2].split(',')[0] in op:  #切割至','前
                locctr+=op[code[2].split(',')[0]][1]
    elif code[2] in op:
        locctr+=op[code[2]][1]
    else:
        print(' ****Wrong OPCODE !')
        lisfile.write(' ****Wrong OPCODE !\n')
        sys.exit('Wrong OPCODE !')

for code in xe:  #產生object code
    if code[0]=='.':  #省略註解行
        continue
    if code[2].find('+') != -1:
        if code[2].find(',X') != -1:
            code.append(hex(int(op[code[2].split('+')[1]][0],16)+3)[2:]+'9'+code[0][1].zfill(5))
        else:
            code.append(hex(int(op[code[2].split('+')[1]][0],16)+3)[2:]+'1'+code[0][1].zfill(5))
    if code[2].find(',X') != -1:  #有X之OPCODE
        if code[2].split(',')[0] in op:
            #切割至','前之OPCODE + 放入之位址第一位加8並轉成16進位 + 加入放入之位址後3位
            code.append(op[code[2].split(',')[0]][0]+hex(int(sym[code[3]][0])+8)[2:].upper()+sym[code[3]][1:])
    if code[2] in op:
        if code[3].find('#') != -1:
            if 48<ord(code[2].split('#')[1])<57:
                print(hex(int(op[code[2].split('+')[1]][0],16)+1)[2:]+'1'+code[3].split('#')[1].zfill(3))
        elif op[code[2]][1]==2:
            print(code)
        else:
            print(code)
#            code.append(op[code[2]][0]+sym[code[3]]) #切割至','前之OPCODE + 加入放入之位址
    else:
        print('error')


srcfile.close()
lisfile.close()
objfile.close()
