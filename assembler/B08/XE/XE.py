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
reg={'A':'0','X':'1','L':'2','B':'3','S':'4','T':'5','F':'6'}
sym={}  #SYMTAB
M=[]  #M卡片
locctr=0

file=input('輸入檔案名稱(XE.txt): ')
#file='XE.txt'
srcfile=open(file)  #開檔
lisfile=open(file.split('.')[0]+'_LISFILE.txt','w')
objfile=open(file.split('.')[0]+'_OBJFILE.txt','w')

print('\n輸入之SIC程式碼:')
for line in srcfile:
    print(line,end='')
    if '\t' in line:  #需增加錯誤行
        print(' ****Tab Error !')
        lisfile.write(' ****Tab Error !\n')
        sys.exit('Tab Error !')
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
    if code[1]=='BASE':
        code.insert(0,'')
        code.append('')
        continue
    if code[1]=='ORG':
        if code[2] in sym:
            PC=locctr
            locctr=sym[code[2]]
        elif code[2] == '':
            locctr=PC
        else:
            print(' ****ORG Error !')
            lisfile.write(' ****ORG Error !\n')
            sys.exit('ORG Error !')
            break
        code.insert(0,'')
        code.append('')
        continue
    code.insert(0,[locctr,str(hex(locctr))[2:].zfill(4).upper()])  #將前一次加完之位置存在陣列前方
    if code[1].strip() and code[1]!='.':  #如果標籤不為空，儲存至SYMTAB 
        sym[code[1]]=code[0][0]  #儲存10進位位址
    if code[2]=='END':  #遇到END則結束
        code.append(hex(sym[code[3]])[2:].zfill(6))
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
            if len(code[3][2:-1])%2 ==1:
                code.append(code[3][2:-1]+' ')
            else:
                code.append(code[3][2:-1])
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

for i,code in enumerate(xe):  #產生object code
    if code[0]=='.':  #省略註解行
        continue
    if code[2]=='END':
        break
    if code[1]=='ORG':
        continue
    while xe[i+1][0]=='.' or xe[i+1][2]=='BASE'or xe[i+1][2]=='ORG':  #遇到註解行跳過
        i=i+1
    PC=xe[i+1][0][0]
    if code[2]=='BASE':
        B=sym[code[3]]
    if code[2].find('+') != -1:  # e=1
        if code[2].find(',X') != -1:  # x=1，一般，ni=3，PC、B必=0
            code.append(hex(int(op[code[2].split('+')[1]][0],16)+3)[2:].zfill(2).upper()+'9'+code[0][1].zfill(5))
        if code[3].find('#') != -1:  #立即模式 ni=1
            if 47<ord(code[3].split('#')[1][0])<58:  #接數字
                code.append(hex(int(op[code[2].split('+')[1]][0],16)+1)[2:].zfill(2).upper()+'1'+code[3].split('#')[1].zfill(5))
            else:  #接標籤，需寫M卡片
                M.append(str(hex(code[0][0]+1))[2:].zfill(6).upper())
                code.append(hex(int(op[code[2].split('+')[1]][0],16)+1)[2:].zfill(2).upper()+'1'+hex(sym[code[3].split('#')[1]])[2:].zfill(5))
        else:
            code.append(hex(int(op[code[2].split('+')[1]][0],16)+3)[2:].zfill(2).upper()+'1'+code[0][1].zfill(5))
    if code[2].find(',X') != -1:  #有X之OPCODE
        if code[2].split(',')[0] in op:
            #切割至','前之OPCODE + 放入之位址第一位加8並轉成16進位 + 加入放入之位址後3位
            code.append(op[code[2].split(',')[0]][0]+hex(int(sym[code[3]][0])+8)[2:].upper()+sym[code[3]][1:])
    if code[2] in op:
        if code[3].find('#') != -1:  #立即模式
            if 47<ord(code[3].split('#')[1][0])<58:  #接數字
                code.append(hex(int(op[code[2]][0],16)+1)[2:].zfill(2).upper()+code[3].split('#')[1].zfill(4))
            else:  #接標籤
                if -2049 < sym[code[3].split('#')[1]]-PC < 2048:  #減PC
                    code.append(hex(int(op[code[2]][0],16)+1)[2:].zfill(2).upper()+'2'+hex(sym[code[3].split('#')[1]]-PC)[2:].zfill(3).upper())
                elif -1 < sym[code[3].split('#')[1]]-B < 4096:  #減B
                    code.append(hex(int(op[code[2]][0],16)+1)[2:].zfill(2).upper()+'4'+hex(sym[code[3].split('#')[1]]-B)[2:].zfill(3).upper())
                else:
                    print(' ****Relative Error!')
                    lisfile.write(' ****Relative Error !\n')
                    sys.exit('Relative Error !')
        elif code[3].find('@') != -1:  #間接模式
            if -2049 < sym[code[3].split('@')[1]]-PC < 2048:  #減PC
                code.append(hex(int(op[code[2]][0],16)+2)[2:].zfill(2).upper()+'2'+hex(sym[code[3].split('@')[1]]-PC)[2:].zfill(3).upper())
            elif -1 < sym[code[3].split('@')[1]]-B < 4096:  #減B
                code.append(hex(int(op[code[2]][0],16)+2)[2:].zfill(2).upper()+'4'+hex(sym[code[3].split('@')[1]]-B)[2:].zfill(3).upper())
            else:
                print(' ****Relative Error!')
                lisfile.write(' ****Relative Error !\n')
                sys.exit('Relative Error !')
        elif op[code[2]][1]==2:  #format 2
            code.append(op[code[2]][0]+reg[code[3].split(',')[0]]+reg[code[3].split(',')[1]])
        else:  #一般，ni=3，減PC or B
            if -2049 < sym[code[3]]-PC < 2048:  #減PC
                code.append(hex(int(op[code[2]][0],16)+3)[2:].zfill(2).upper()+'2'+hex(sym[code[3]]-PC)[2:].zfill(3).upper())
            elif -1 < sym[code[3]]-B < 4096:  #減B
                code.append(hex(int(op[code[2]][0],16)+3)[2:].zfill(2).upper()+'4'+hex(sym[code[3]]-B)[2:].zfill(3).upper())
            else:
                print(' ****Relative Error!')
                lisfile.write(' ****Relative Error !\n')
                sys.exit('Relative Error !')
                

print('\n輸出之LISFILE: ')
for code in xe:  #輸出LISFILE
    if code[0]=='.':  #顯示整行註解
        lisfile.write(' '*14+'.'+code[1]+'\n')
        print(' '*14+'.'+code[1])
    elif code[2]=='BASE' or code[2]=='ORG':
        lisfile.write(' '*14+'{0:<9}{1:<8}{2}\n' .format(code[1],code[2],code[3]))
        print(' '*14+'{0:<9}{1:<8}{2}' .format(code[1],code[2],code[3]))
    elif code[2]=='END':
        lisfile.write('{0:<4}'.format(code[0][1])+' '*10+'{0:<9}{1:<8}{2}\n' .format(code[1],code[2],code[3]))
        print('{0:<4}'.format(code[0][1])+' '*10+'{0:<9}{1:<8}{2}' .format(code[1],code[2],code[3]))
    else:
        lisfile.write('{0:<4} {1:<8} {2:<9}{3:<8}{4}\n' .format(code[0][1],code[4],code[1],code[2],code[3]))
        print('{0:<4} {1:<8} {2:<9}{3:<8}{4}' .format(code[0][1],code[4],code[1],code[2],code[3]))

print('\n輸出之OBJFILE: ')
length=str(hex(xe[-1][0][0]-xe[0][0][0]))[2:].zfill(6).upper()  #計算總長度
#輸出 H卡片
print('H'+'{0:<6}'.format(xe[0][1])+xe[0][3].zfill(6)+length)
objfile.write('H'+'{0:<6}'.format(xe[0][1])+xe[0][3].zfill(6)+length+'\n')

objf=[]
l=-1
t=''
#輸出 T,M,E卡片
for i,code in enumerate(xe):
    if code[0]=='.' or code[4]=='':  #省略註解行 及 RESW RESB
        continue
    if code[2]=='END':  #遇到END輸出E卡片
        if t!='':  #前一行有剩餘未完成字串則輸出
            objfile.write(str(hex(l))[2:].zfill(2).upper()+t+'\n')
            print(str(hex(l))[2:].zfill(2).upper()+t)
            t=''
        #輸出 M卡片
        for m in M:
            objfile.write('M'+m+'05\n')
            print('M'+m+'05')
        objfile.write('E'+hex(sym[code[3]])[2:].zfill(6).upper()+'\n')
        print('E'+hex(sym[code[3]])[2:].zfill(6).upper())
        break
    elif l==-1:  #T卡片開頭
        objfile.write('T'+code[0][1].zfill(6))
        print('T'+code[0][1].zfill(6),end='')
        t+=code[4]
        l+=1+math.ceil(len(code[4])/2)
    elif l<=30: #卡片長度不超過30則繼續寫入
        l+=math.ceil(len(code[4])/2)
        t+=code[4]
    while xe[i+1][0]=='.':  #遇到註解行跳過
        i=i+1
    if xe[i+1][2]!='BASE' and (math.ceil(len(xe[i+1][4])/2)+l>30 or xe[i+1][4]==''):  #如果加入下行object code即超過30 or 下行object code為空 則換卡片
        objfile.write(str(hex(l))[2:].zfill(2).upper()+t+'\n')
        print(str(hex(l))[2:].zfill(2).upper()+t)
        t=''
        l=-1


srcfile.close()
lisfile.close()
objfile.close()
