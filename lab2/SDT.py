
import sys
sys.setrecursionlimit(3000)
key_list=['const','int','float','void','if','else','while','break','continue','return']#种别码1-10
op_list=['+','-','*','/','%',"==","!=",'<','>','<=','>=','!','&&','||','=']#种别码11-25
de_list=['{','}','[',']','(',')',',',';']#种别码 26-31
import copy
all_list=key_list+op_list+de_list#33个 34 literal 35id

def LL1(result):
    token=""
    quadra_list=[]
    input_list=copy.deepcopy(result)
    input_list.append((36,"END"))
    symbol_table={}
    tn=0#临时变量t1,t2。。。。的使用情况


    def getnext():
        this_token=input_list[0]
        return this_token

    def MAIN():

        nonlocal token
        token=getnext()
        while(token[0]!=36):
            if token[0] in [i for i in range(1, 11)]:
                CompUnit()

            elif token[0]==26:
                Block()

            else:
                exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")




    def CompUnit():


        nonlocal token
         #compunit->blockitem compunit_
                             #compunit_=(blockitem compunit_)  | none
            #compunit->blockitem compunit|None
        if token[0] in [i for i in range(1,11)]:
            Decl()
            CompUnit_()

        elif token[0]!=36:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")
            return False

    def CompUnit_():

        # compunit->blockitem compunit_
        # compunit_=(blockitem compunit_)  | none
        # compunit->blockitem compunit|None
        nonlocal token
        if token[0] in [i for i in range(1,11)]:
            Decl()
            CompUnit_()

        # elif token[0] !=36:
        #     exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")
        #     return False
        else:pass

    def Block():

        nonlocal token
        while token[0]==26:
            del input_list[0]
            token = getnext()
            while token[0]!=27:
                Blockitem()
                if token[0]==27:

                    del input_list[0]
                    token = getnext()
                    break


    def Blockitem():

        nonlocal token
        if token[0] in [1,2,3]:
            Decl()
        elif token[0] in [4,5,6,7,8,9,10,26,33,35]:
            Stmt()
        else:exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")

    def Decl():#声明

        nonlocal token
        if token[0]==1:
            Constdecl()


        elif token[0] in [2,3]:
            Vardecl()


    def Constdecl():#常量声明
        nonlocal token
        if token[0]==1:
            del input_list[0]
            token=getnext()
        Btype()
        Constdef()
        while token[0]==32:#,
            del input_list[0]
            token = getnext()
            Constdef()

        if token[0]==33:
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


    def Vardecl():#变量声明

        nonlocal token
        Btype()
        Vardef()
        while token[0] == 32:  # ,
            del input_list[0]
            token = getnext()
            Vardef()

        if token[0] == 33:
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


    def Btype():

        nonlocal token
        if token[0] in [2,3]:
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


    def Constdef():#常量定义
        nonlocal token,symbol_table
        qua_4=""
        if token[0]==35:
            qua_4=token[1]
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


        if token[0]==25:
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


        val=Addexp()

        quadra_ele=(":=",val,"_",qua_4)
        quadra_list.append(quadra_ele)
        symbol_table['qua_4']=val

        return len(quadra_list)-1



    def Vardef():#变量定义

        qua_4=""
        nonlocal token
        if token[0] == 35:
            qua_4 = token[1]
            del input_list[0]
            token = getnext()

        else:
            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")

        nonlocal symbol_table
        if token[0] ==25:
            del input_list[0]
            token = getnext()
            val = Addexp()
            symbol_table[qua_4] = val

            quadra_ele = (":=", val, "_", qua_4)
            quadra_list.append(quadra_ele)


        else:

            symbol_table[qua_4]=None

        return len(quadra_list) - 1



#constinitval 和 initval 直接转化成add exp,这之后都是语句

    def Stmt():


        nonlocal token

        if token[0]==5:#if
            del input_list[0]
            token = getnext()
            if token[0] == 30:#(
                del input_list[0]
                token = getnext()
                Cond()#这条emit所有的条件表达式
                condpos=len(quadra_list)-1#条件表达式最后一条标号

                if token[0] == 31:#)
                    del input_list[0]
                    token = getnext()
                    #j< 跳转真出口，不然直接假出口
                    Stmt()#把表达式的也写了
                    #quadra_list.insert(condpos + 1, ('j', "_", "_", len(quadra_list)))#jump
                    quadra_list[condpos]=(quadra_list[condpos][0],quadra_list[condpos][1],quadra_list[condpos][2],len(quadra_list))
                    if token[0] ==6:#else 中间先加一条j,_,_,pos2

                        del input_list[0]
                        token = getnext()
                        Stmt()


                else:
                    exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")

            else:
                exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")



        elif token[0]==7:#while
            del input_list[0]
            token = getnext()
            if token[0] == 30:
                del input_list[0]
                token = getnext()
                prepos=len(quadra_list)
                Cond()#条件布尔
                condpos = len(quadra_list) - 1  # 条件表达式最后一条标号
                if token[0] == 31:#)
                    del input_list[0]
                    token = getnext()
                    Stmt()#执行
                    quadra_list[condpos] = (
                    quadra_list[condpos][0], quadra_list[condpos][1], quadra_list[condpos][2], len(quadra_list))

                    quadra_list.append(("jump","_","_",prepos))
                    quadra_list.append(("jump","_","_","END"))

                    for i in range(len(quadra_list)):
                        if quadra_list[i][3]==len(quadra_list)-2:
                            quadra_list[i]=(quadra_list[i][0],quadra_list[i][1],quadra_list[i][2],len(quadra_list)-1)



                    return

                else:
                    exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


            else:
                exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


        elif token[0]==8:#break
            del input_list[0]
            token = getnext()
            if token[0]==33:
                del input_list[0]
                token = getnext()

            else:
                del input_list[0]
                token = getnext()

        elif token[0] == 9:  # continue
            del input_list[0]
            token = getnext()
            if token[0] == 33:
                del input_list[0]
                token = getnext()

            else:
                del input_list[0]
                token = getnext()

        elif token[0] == 10:  # return
            del input_list[0]
            token = getnext()
            if token[0] == 33:
                del input_list[0]
                token = getnext()

            else:
                Addexp()
                if token[0] == 33:
                    del input_list[0]
                    token = getnext()

                else:
                    exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


        elif token[0]==26:
            Block()

        elif token[0]==35:
            qua4=token[1]
            Lval()
            if token[0]==25:# =
                del input_list[0]
                token = getnext()
                res=Addexp()
                quadra_list.append((":=",res,"_",qua4))
                nonlocal symbol_table
                symbol_table[qua4]=res


                if token[0]==33:#分号
                    del input_list[0]
                    token = getnext()
            else:
                exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")


        elif token[0]==33:
            del input_list[0]
            token = getnext()

        else:
            Addexp()



    def Lval():#左值，属性为值

        nonlocal token,symbol_table
        res=0
        if token[0]==35 and token[1] in symbol_table.keys():
            res=token[1]
            del input_list[0]
            token = getnext()
        else:

            exit("identifier hasn't been decleared")

        return res


    def Cond():#条件语句
        nonlocal token
        Lorexp()


    def Primaryexp():#基本语句，属性为值
        nonlocal token
        if token[0]==30:
            del input_list[0]
            token = getnext()

            res=Addexp()[0]#(exp)
            if token[0] == 31:
                del input_list[0]
                token = getnext()

            else:
                exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")

            return res

        elif token[0]==35:
            res=Lval()
            return res

        elif token[0]==34:
            res=Number()
            return res

    def Number():


        nonlocal token
        res=float(token[1])
        del input_list[0]
        token = getnext()
        symbol_table[res]=res
        return res

    def Unaryexp():
        nonlocal token,symbol_table
        if token[0] in[30,35,34]:
            res=Primaryexp()
            return res
        elif token[0] in[11,12,22]:#+-!
            resa=Unaryop()
            resb=Unaryexp()
            if resa=="+":
                symbol_table[resb]=resb
            elif resa=="-":
                symbol_table[resb]=-resb
            else: symbol_table[resb]=-resb
            return resb

        else:

            exit(f"syntax error in token {token} of {[input_list[i][1] for i in range(len(input_list))]}")



    def Unaryop():
        nonlocal token
        res=0
        if token[0] in [11,12,22]:
            res=token[0]
            del input_list[0]
            token = getnext()
            return res

    def Mulexp():
        nonlocal tn

        nonlocal token


        resa=Unaryexp()
        resb = Mulexp_()
        if resb:
            tn+=1
            quadra_list.append((resb[0],resa,resb[1],f"t{tn}"))
            if resb[0]=="*":symbol_table[f"t{tn}"]=symbol_table[resa]*symbol_table[resb]
            elif resb[0]=="/":symbol_table[f"t{tn}"]=symbol_table[resa]/symbol_table[resb]
            else:symbol_table[f"t{tn}"]=symbol_table[resa]%symbol_table[resb]
            return f"t{tn}"
        else: return resa




    def Mulexp_():
        nonlocal token,tn
        if token[0] in [13,14,15]:
            res1=all_list[token[0]-1]#符号
            del input_list[0]
            token = getnext()
            res2=Unaryexp()
            res3=Mulexp_()


            if res3:
                tn+=1
                quadra_list.append((res1,res2,res3,f"t{tn}"))

                if res1 == "*":
                    symbol_table[f"t{tn}"] = symbol_table[res2] * symbol_table[res3]
                elif res1 == "/":
                    symbol_table[f"t{tn}"] = symbol_table[res2] / symbol_table[res3]
                else:
                    symbol_table[f"t{tn}"] = symbol_table[res2] % symbol_table[res3]

                return res1,f"t{tn}"
            else:
                return res1,res2

        else:
            pass


    def Addexp():

        nonlocal tn

        nonlocal token
        resa = Mulexp()
        resb = Addexp_()
        if resb:
            tn += 1
            quadra_list.append((resb[0], resa, resb[1], f"t{tn}"))
            if resb[0] == "+":
                symbol_table[f"t{tn}"] = symbol_table[resa] + symbol_table[resb[1]]
            else:
                symbol_table[f"t{tn}"] = symbol_table[resa]- symbol_table[resb[1]]

            return f"t{tn}"
        else:
            return resa

    def Addexp_():
        nonlocal token, tn
        if token[0] in [11,12]:
            res1 = all_list[token[0] - 1]  # 符号
            del input_list[0]
            token = getnext()
            res2 = Unaryexp()
            res3 = Mulexp_()

            if res3:
                tn += 1
                quadra_list.append((res1, res2, res3, f"t{tn}"))

                if res1 == "+":
                    symbol_table[f"t{tn}"] = symbol_table[res2] + symbol_table[res3]

                else:
                    symbol_table[f"t{tn}"] = symbol_table[res2] - symbol_table[res3]

                return res1, f"t{tn}"
            else:
                return res1, res2
        else:
            pass

    def Relexp():#关系表达式
        nonlocal token,tn

        nonlocal token
        resa = Addexp()
        resb = Relexp_()
        if resb:
            #quadra_list.append(("j"+resb[0], resa, resb[1], None))
            return ("j"+resb[0], resa, resb[1], None)


        else:
            return resa


    def Relexp_():#好像有点问题

        nonlocal token, tn
        if token[0] in [18,19,20,21]:
            res1 = all_list[token[0] - 1]  # 符号
            del input_list[0]
            token = getnext()
            res2 = Addexp()
            res3 = Relexp_()

            if res3:
                #quadra_list.append(("j" + res3[0], res2, res3[1], None))
                return res1, res3
            else:
                return res1, res2
        else:
            pass


    def Eqexp():  # 关系表达式

        nonlocal token, tn

        nonlocal token
        resa = Relexp()
        resb = Eqexp_()
        if resb:
            #quadra_list.append(("j" + resb[0], resa, resb[1], None))
            return ("j" + resb[0], resa, resb[1], None)


        else:
            return resa

    def Eqexp_():

        nonlocal token, tn
        if token[0] in [16,17]:
            res1 = all_list[token[0] - 1]  # 符号
            del input_list[0]
            token = getnext()
            res2 =Relexp()
            res3 = Eqexp_()

            if res3:
                # quadra_list.append(("j" + res3[0], res2, res3[1], None))
                return res1, res3
            else:
                return res1, res2
        else:
            pass


    def Landexp():  #与表达式
        nonlocal token
        qua1=Eqexp()
        process_list=[]
        process_list.append((qua1[0],qua1[1],qua1[2],"t"))
        process_list.append(("jump","_","_","f"))
        #len(quadra_list)+2)

        process_list.extend(Landexp_())
        return process_list




    def Landexp_():
        nonlocal token
        process_list=[]
        if token[0]==23:#&&
            del input_list[0]
            token = getnext()
            qua1=Eqexp()
            process_list.append((qua1[0], qua1[1], qua1[2], "t"))
            process_list.append(("jump", "_", "_", "f"))
            process_list.extend(Landexp_())
            return process_list

        else:
            return process_list


    def Lorexp():  #或表达式
        nonlocal token
        quatemp_list=Landexp()

        false_pos=len(quadra_list)+len(quatemp_list)#假出口都汇集到这里 假+1，真+2

        for i in range(len(quatemp_list)):

            if quatemp_list[i][3]== "t" and i<len(quadra_list)-2:
                quadra_list.append((quatemp_list[i][0], quatemp_list[i][1], quatemp_list[i][2], len(quadra_list) + 2))
            elif quatemp_list[i][3]== "t":
                quadra_list.append((quatemp_list[i][0], quatemp_list[i][1], quatemp_list[i][2], "t"))#直接真出口，执行stmt的代码
            else:quadra_list.append(("jump", "_", "_", false_pos))#汇集到假出口,不然则是下一个or

        Lorexp_()

        quadra_list[false_pos-2]=(quadra_list[false_pos-2][0], quadra_list[false_pos-2][1], quadra_list[false_pos-2][2], len(quadra_list)+1)#真出口。执行stmt


        quadra_list.append(("jump", "_", "_", 'f'))#假出口，要跳过stmt
        return len(quadra_list)-1




    def Lorexp_():
        nonlocal token
        if token[1]!="||":
            return

        quatemp_list = Landexp()

        false_pos = len(quadra_list) + len(quatemp_list)  # 假出口都汇集到这里 假+1，真+2

        for i in range(len(quatemp_list)):

            if quatemp_list[i][3] == "t" and i < len(quadra_list) - 2:
                quadra_list.append((quatemp_list[i][0], quatemp_list[i][1], quatemp_list[i][2], len(quadra_list) + 2))
            elif quatemp_list[i][3] == "t":
                quadra_list.append((quatemp_list[i][0], quatemp_list[i][1], quatemp_list[i][2], "t"))  # 直接真出口，执行stmt的代码
            else:
                quadra_list.append(("jump", "_", "_", false_pos))  # 汇集到假出口,不然则是下一个or

        Lorexp_()

        quadra_list[false_pos - 2] = (
        quatemp_list[false_pos - 2][0], quatemp_list[false_pos - 2][1], quatemp_list[false_pos - 2][2],
        len(quadra_list) + 1)  # 真出口。执行stmt

        quadra_list.append(("jump", "_", "_", 'f'))  # 假出口，要跳过stmt
        return len(quadra_list) - 1



    MAIN()

    print("output words:",input_list)
    if input_list==[(36,'END')]:
        print("syntax analysis success")
    for i in range(len(quadra_list)):

        print(i,quadra_list[i])


import lex


file_name=input("please input file name")
result=lex.lexical(file_name)
print(result)
LL1(result)







