
key_list=['const','int','float','void','if','else','while','break','continue','return']#种别码1-10
op_list=['+','-','*','/','%',"==","!=",'<','>','<=','>=','!','&&','||','=']#种别码11-25
de_list=['{','}','[',']','(',')',',',';']#种别码 26-33
all_list=key_list+op_list+de_list#33个 34 literal 35 id
digit_list=[str(i) for i in range(10)]
constele_list=digit_list+['.']
alphabet_list=[chr(i) for i in range(97,123)]+[chr(i) for i in range(65,91)]
alphabet_list_plus_=alphabet_list+["_"]



signal_list=[" ","\n"]
comment_list=["//","*/","/*"]
def read_file(filename):#读取文件
    with open(filename,"r") as f:
        origin_text=f.read()
        print(origin_text)
    return origin_text


def reduce_comment(text):#删除注释
    i=0
    while(i<len(text)):
        if text[i]=="/" and i+1<len(text) and text[i+1]=="/":
            try:
                while text[i+2]!="\n":
                    text=text[:i+2]+text[i+3:]
            except:

                pass

        elif text[i]=="/" and i+1<len(text) and text[i+1]=="*":

            try:
                while not (text[i+2]=="*" and text[i+3]=="/"):
                    text=text[:i+2]+text[i+3:]
            except:


                pass
        i+=1

    return text


def divide(text):#分割单词
    word_list=[]
    new_word=""
    i=0
    while(i<len(text)):
        if(text[i]) in signal_list:
            if new_word:
                word_list.append(new_word)
                new_word=""
            i+=1

        elif (i+1<len(text)  and text[i]+text[i+1] in op_list+de_list+comment_list):
            if new_word:
                word_list.append(new_word)
                new_word = ""
            word_list.append(text[i]+text[i+1])
            i+=2

        elif  text[i] in op_list+de_list:
            if new_word:
                word_list.append(new_word)
                new_word = ""
            word_list.append(text[i])
            i+=1

        elif i+1==len(text) and new_word:
            word_list.append(new_word)

        else:
            new_word+=text[i]
            i+=1

    return word_list#

def is_id(word):#是identifier
    if not word[0] in alphabet_list_plus_:
        return False

    for i in range(1,len(word)):
        if not word[i] in alphabet_list_plus_+digit_list:
            return False

    return True

def is_keyword(word):#是关键字
    if word in key_list:
        return True
    return False

def is_op(word):#是运算符
    if word in op_list:
        return True
    return False

def is_de(word):#是分割符
    if word in de_list:
        return True
    return False


def is_literal(word): #是literal
    hex_digit=[str(i) for i in range(10)]+['a','b','c','d','e','f',
                                           'A','B','C','D','E','F']
    oct_digit=[str(i) for i in range(8)]
    if len(word) > 2 and word[0] + word[1] in ["0x", "0X"]:
        if not word[2] in hex_digit:
            return False
        if not word[len(word) - 1] in hex_digit:
            return False
        for i in range(1, len(word) - 1):
            if not word[i] in hex_digit+["."]:
                return False

    elif len(word)>1 and word[0]=="0":
        if not word[2] in oct_digit:
            return False
        if not word[len(word) - 1] in oct_digit:
            return False
        for i in range(1, len(word) - 1):
            if not word[i] in oct_digit+["."]:
                return False


    else:
        if not word[0] in [str(i) for i in range(1,10)]:
            return False
        if not word[len(word) - 1] in digit_list:
            return False
        for i in range(1, len(word) - 1):
            if not word[i] in constele_list:
                return False

    return True

def lexical(file):

    result=[]
    to_be_ana_text=reduce_comment(read_file(file))
    word_list=divide(to_be_ana_text)

    ####注释号，括号的对称性检查
    find=True
    for i in range(len(word_list)):#注释右侧点

        if word_list[i]=="/*":
            find=False
            for j in range(i+1,len(word_list)):
                if word_list[j]=="*/":
                    find=True
                    break
        if not find:
            exit("need '*/' for comment")

    find = 0
    for i in range(len(word_list)):  # 注释右侧点

        if word_list[i] == "{":find+=1
        if word_list[i] == "}": find -=1

    if find > 0:
            exit("need '}'")
    elif find < 0:
            exit("need '{'")


    find = 0
    for i in range(len(word_list)):  # 注释右侧点

        if word_list[i] == "(": find += 1
        if word_list[i] == ")": find -= 1

    if find > 0:
            exit("need ')'")
    elif find < 0:
            exit("need '('")

    i=0
    while i<len(word_list):#删除注释标记
        if word_list[i] in comment_list:
            del word_list[i]

            continue
        i+=1


    for i in word_list:
        if is_de(i) or is_op(i) or is_keyword(i):
            for j in range(len(all_list)):
                if all_list[j]==i:
                    result.append((j+1,i))

        elif is_literal(i):
            result.append((34,i))

        elif is_id(i):
            result.append((35,i))

        else:
            result.append(f"{i} invalid")
            exit(f"{i} invalid")


    return result

if __name__=="__main__":
    print("王育之 20计联 202030170238")
    file_name=input("please input file name")


    for i in range(len(all_list)):
        print(i + 1, all_list[i], "      ", end="")
        if (i + 1) % 7 == 0:
            print(end="\n")
    print(34, "literal", "       ", 35, "identifier")


    print(lexical(file_name))
