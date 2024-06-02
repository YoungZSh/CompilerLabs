action={0:{'id':'s2'},
        1:{'$':'Acc'},
        2:{':':'s17'},
        3:{'(':'s7','id':'s8'},
        4:{'+':'s9','$':'r1','-':'s18'},
        5:{'+':'r4','-':'r4','*':'s10','/':'s11','$':'r4',')':'r4'},
        6:{'+':'r7','-':'r7','*':'r7','/':'r7','$':'r7',')':'r7'},
        7:{'(':'s7','id':'s8'},
        8:{'+':'r9','-':'r9','*':'r9','/':'r9','$':'r9',')':'r9'},
        9:{'(':'s7','id':'s8'},
        10:{'(':'s7','id':'s8'},
        11:{'(':'s7','id':'s8'},
        12:{'+':'s9',')':'s16','-':'s18'},
        13:{'+':'r2','-':'r2','*':'s10','/':'s11','$':'r2',')':'r2'},
        14:{'+':'r5','-':'r5','*':'r5','/':'r5','$':'r5',')':'r5'},
        15:{'+':'r6','-':'r6','*':'r6','/':'r6','$':'r6',')':'r6'},
        16:{'+':'r8','-':'r8','*':'r8','/':'r8','$':'r8',')':'r8'},
        17:{'=':'s3'},
        18:{'(':'s7','id':'s8'},
        19:{'+':'r3','-':'r3','*':'s10','/':'s11','$':'r3',')':'r3'}}
 
goto={0:{'S':1},
      3:{'E':4,'T':5,'F':6},
      7:{'E':12,'T':5,'F':6},
      9:{'T':13,'F':6},
      10:{'F':14},
      11:{'F':15},
      18:{'T':19,'F':6}
}
 
ss={'s0':0,'s1':1,'s2':2,'s3':3,'s4':4,'s5':5,'s6':6,'s7':7,'s8':8,'s9':9,'s10':10,'s11':11,'s12':12,'s13':13,'s14':14,'s15':15,'s16':16,'s17':17,'s18':18,'s19':19}
rs={'r0':[1,'S`'],'r1':[4,'S'],'r2':[3,'E'],'r3':[3,'E'],'r4':[1,'E'],'r5':[3,'T'],'r6':[3,'T'],'r7':[1,'T'],'r8':[3,'F'],'r9':[1,'F']}
 
ID={'F':{},'E':{},'T':{},'id':{}}
'''
[0]	S’ → S   
[1]	S → i := E      emit(id:=E.place)
[2]	E → E1+T1       E.place:=newtemp
                    emit(E.place:=E1.place+T1.place:)
[3]	E → E1-T1       E.place:=newtemp
                    emit(E.place:=E1.place-T1.place:)
[4]  E → T1         E.place:=T1.place
[5]  T → T1*F1      T.place:=newtemp
                    emit(E.place:=T1.place*F1.place:)
[6]  T → T1/F1      T.place:=newtemp
                    emit(E.place:=T1.place/F1.place:)
[7]	T →F1           T.place:=F1.place
[8]  F→ (E1)        F.place:=E1.place
[9]  F→ i           F.place:=id
'''
 
#生成中间变量
newtemp=[]
def mk_newtemp():
    i=len(newtemp)
    i+=1
    t="t%s"%i
    newtemp.append(t)
    return t
 
#插入符号表中
def insert_ID(word,val=None):
    if word=='id':
        i=len(ID['id'])+1
        t="id%s"%i
        ID['id'][t]={}
        ID['id'][t]['val']=val
        return t
    if word=='F':
        i = len(ID['F']) + 1
        t = "F%s" % i
        ID['F'][t]={}
        ID['F'][t]['val'] = val
        return t
    if word=='T':
        i = len(ID['T']) + 1
        t = "T%s" % i
        ID['T'][t]={}
        ID['T'][t]['val'] = val
        return t
    if word=='E':
        i = len(ID['E']) + 1
        t = "E%s" % i
        ID['E'][t]={}
        ID['E'][t]['val'] = val
        return t
 
#规则处理
def regulate(oder,lis):
    if oder=='r1':
        print('id:=',ID['E'][lis[0]]['val'])
        rs1='S'
        rs2='S'
        return rs1, rs2
    if oder=='r2':
        t=mk_newtemp()
        val="{0}+{1}".format(ID['E'][lis[2]]['val'],ID['T'][lis[0]]['val'])
        print(t,'=',val)
        rs1 = insert_ID('E',t)
        rs2='E'
        return rs1, rs2
    if oder=='r3':
        t = mk_newtemp()
        val = "{0}-{1}".format(ID['E'][lis[2]]['val'], ID['T'][lis[0]]['val'])
        print(t, '=', val)
        rs1 = insert_ID('E', t)
        rs2='E'
        return rs1, rs2
    if oder=='r4':
        val = "{0}".format(ID['T'][lis[0]]['val'])
        rs1 = insert_ID('E', val)
        rs2='E'
        return rs1, rs2
    if oder=='r5':
        t = mk_newtemp()
        val = "{0}*{1}".format(ID['T'][lis[2]]['val'], ID['F'][lis[0]]['val'])
        print(t, '=', val)
        rs1 = insert_ID('T', t)
        rs2='T'
        return rs1, rs2
    if oder=='r6':
        t = mk_newtemp()
        val = "{0}/{1}".format(ID['T'][lis[2]]['val'], ID['F'][lis[0]]['val'])
        print(t, '=', val)
        rs1 = insert_ID('T', t)
        rs2='T'
        return rs1, rs2
    if oder=='r7':
        val = "{0}".format(ID['F'][lis[0]]['val'])
        rs1 = insert_ID('T', val)
        rs2='T'
        return rs1, rs2
    if oder=='r8':
        val = "{0}".format(ID['E'][lis[1]]['val'])
        rs1 = insert_ID('F', val)
        rs2='F'
        return rs1, rs2
    if oder=='r9':
        val = "{0}".format(ID['id'][lis[0]]['val'])
        rs1 = insert_ID('F', val)
        rs2='F'
        return rs1, rs2
 
def analise(lis):
    stack=[0]
    word=[]
    i=1
    while i<len(lis):
        first=lis[i].split(',')[0][1:]
        second=lis[i].split(',')[1][0]
        if first =='id':
            t=insert_ID('id',second)
            word.append(t)
        else:
            word.append(second)
        i+=1
    word.append('$')
    print(word)
    while len(word) > 0:
        word_st = stack[0]
        word1 = word[0]
        word_r = []  # 保存归约的句子
        # 归约时按原处理
        if 'id' in word1:
            word1 = 'id'
        if 'F' in str(word_st):
            word_st = 'F'
        if 'T' in str(word_st):
            word_st = 'T'
        if 'E' in str(word_st):
            word_st = 'E'
 
        if action[word_st][word1] == 'Acc':
            return True
        if action[word_st][word1][0] == 's':
            stack.insert(0, word[0])
            stack.insert(0, ss[action[word_st][word1]])
            word.pop(0)
        else:
            i = rs[action[word_st][word1]][0] * 2
            for j in range(1,i,2):
                word_r.append(stack[j])
            while i > 0:
                stack.pop(0)
                i -= 1
            rs1,rs2=regulate(action[word_st][word1],word_r)
            stack.insert(0, rs1)
            stack.insert(0, goto[stack[1]][rs2])
    return False
 
def main():
    with open('demo3.txt',encoding='utf-8') as words:
        contents = words.read()
        first_w = contents.split('\n') #将文件内句子拆分
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        list6=[]
        i=0
        n=0
        while i<len(first_w):
            if first_w[i]=='1、':
                for j in range(i+1,len(first_w)):
                    if first_w[j] == '2、':
                        n=j
                        break
                    list1.append(first_w[j])
            if first_w[i]=='2、':
                for j in range(i+1,len(first_w)):
                    if first_w[j] == '3、':
                        n=j
                        break
                    list2.append(first_w[j])
            if first_w[i]=='3、':
                for j in range(i+1,len(first_w)):
                    if first_w[j] == '4、':
                        n=j
                        break
                    list3.append(first_w[j])
            if first_w[i]=='4、':
                for j in range(i+1,len(first_w)):
                    if first_w[j] == '5、':
                        n = j
                        break
                    list4.append(first_w[j])
            if first_w[i]=='5、':
                for j in range(i+1,len(first_w)):
                    if first_w[j] == '6、':
                        n = j
                        break
                    list5.append(first_w[j])
            if first_w[i]=='6、':
                for j in range(i+1,len(first_w)):
                    list6.append(first_w[j])
                n=len(first_w)
            i=n
    try:
        if analise(list1):
            print("语法正确!")
        else:
            print("语法错误!")
    except:
        print("语法错误!")
main()