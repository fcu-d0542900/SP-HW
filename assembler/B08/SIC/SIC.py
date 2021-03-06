# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:24:11 2018

@author: YURU
"""
import math
import sys

sic=[]  #程式碼儲存
op={'ADD':['18',3],'AND':['40',3],'COMP':['28',3],'DIV':['24',3],'FIX':['C4',1],
    'J':['3C',3],'JEQ':['30',3],'JGT':['34',3],'JLT':['38',3],'JSUB':['48',3],
    'LDA':['00',3],'LDCH':['50',3],'LDL':['8',3],'LDX':['4',3],'MUL':['20',3],'OR':['44',3],'RD':['D8',3],'RSUB':['4C',3],
    'STA':['0C',3],'STCH':['54',3],'STL':['14',3],'STX':['10',3],'SUB':['1C',3],'TD':['E0',3],'TIX':['2C',3],'WD':['DC',3]}
sym={}  #SYMTAB
locctr=0

file=input('輸入檔案名稱(SIC.txt): ')
#file='SIC.txt'
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
        sic.append(['.',line.split('.')[1].strip()])
    else:
        sic.append([line[0:9].strip().upper(),line[9:17].strip().upper(),line[17:].strip().upper()])  #分割儲存字串
print()
#print(sic)

for code in sic:  #計算位址
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
    elif code[2].find(',X') != -1:  #有X之OPCODE
            if code[2].split(',')[0] in op:  #切割至','前
                locctr+=op[code[2].split(',')[0]][1]
    elif code[2] in op:
        locctr+=op[code[2]][1]
    else:
        print(' ****Wrong OPCODE !')
        lisfile.write(' ****Wrong OPCODE !\n')
        sys.exit('Wrong OPCODE !')

for code in sic:  #產生object code
    if code[0]=='.':  #省略註解行
        continue
    if code[2].find(',X') != -1:  #有X之OPCODE
        if code[2].split(',')[0] in op:
            #切割至','前之OPCODE + 放入之位址第一位加8並轉成16進位 + 加入放入之位址後3位
            code.append(op[code[2].split(',')[0]][0]+hex(int(sym[code[3]][0])+8)[2:].upper()+sym[code[3]][1:])
    if code[2] in op:
        code.append(op[code[2]][0]+sym[code[3]]) #切割至','前之OPCODE + 加入放入之位址

'''
for code in sic:
    print(code)
'''

print('\n輸出之LISFILE: ')
for code in sic:  #輸出LISFILE
    if code[0]=='.':  #顯示整行註解
        lisfile.write(' '*12+'.'+code[1]+'\n')
        print(' '*12+'.'+code[1])
    elif code[2]=='END':
        lisfile.write('{0:<4}'.format(code[0][1])+' '*8+'{0:<9}{1:<8}{2}\n' .format(code[1],code[2],code[3]))
        print('{0:<4}'.format(code[0][1])+' '*8+'{0:<9}{1:<8}{2}' .format(code[1],code[2],code[3]))
    else:
        lisfile.write('{0:<4} {1:<6} {2:<9}{3:<8}{4}\n' .format(code[0][1],code[4],code[1],code[2],code[3]))
        print('{0:<4} {1:<6} {2:<9}{3:<8}{4}' .format(code[0][1],code[4],code[1],code[2],code[3]))
        
print('\n輸出之OBJFILE: ')
length=str(hex(sic[-1][0][0]-sic[0][0][0]))[2:].zfill(6).upper()  #計算總長度
#輸出 H卡片
print('H'+'{0:<6}'.format(sic[0][1])+sic[0][3].zfill(6)+length)
objfile.write('H'+'{0:<6}'.format(sic[0][1])+sic[0][3].zfill(6)+length+'\n')

objf=[]
l=-1
t=''
#輸出 T,E卡片
for i,code in enumerate(sic):
    if code[0]=='.' or code[4]=='':  #省略註解行 及 RESW RESB
        continue
    if code[2]=='END':  #遇到END輸出E卡片
        if t!='':  #前一行有剩餘未完成字串則輸出
            objfile.write(str(hex(l))[2:].zfill(2).upper()+t+'\n')
            print(str(hex(l))[2:].zfill(2).upper()+t)
            t=''
        objfile.write('E'+sym[code[3]].zfill(6)+'\n')
        print('E'+sym[code[3]].zfill(6))
        break
    elif l==-1:  #T卡片開頭
        objfile.write('T'+code[0][1].zfill(6))
        print('T'+code[0][1].zfill(6),end='')
        t+=code[4]
        l+=1+math.ceil(len(code[4])/2)
    elif l<=30: #卡片長度不超過30則繼續寫入
        l+=math.ceil(len(code[4])/2)
        t+=code[4]
    while sic[i+1][0]=='.':  #遇到註解行跳過
        i=i+1
    if math.ceil(len(sic[i+1][4])/2)+l>30 or sic[i+1][4]=='':  #如果加入下行object code即超過30 or 下行object code為空 則換卡片
        objfile.write(str(hex(l))[2:].zfill(2).upper()+t+'\n')
        print(str(hex(l))[2:].zfill(2).upper()+t)
        t=''
        l=-1
        
 
srcfile.close()
lisfile.close()
objfile.close()
