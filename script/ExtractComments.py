
import os
import re
import sys
from distutils.dir_util import mkpath


percorso = sys.argv[1]
pac = sys.argv[2]

path_SourceCode = percorso + pac

mkpath(os.getcwd() + "/file/")



def formatt_comment(path_tempComment):
    file = open(path_tempComment,'r')
    path_NewCommentFile = os.getcwd() + "/file/Totale_" + pac + ".txt"
    path_NewCommentFile_Class = os.getcwd() + "/file/Comment_Class.txt"
    new_temp_file = open(path_NewCommentFile,'w')
    new_temp_file_Class = open(path_NewCommentFile_Class,'w')
    
    exp_newLine = "^\s+"
    exp_specialTag = "<(/)?\w*>"
    exp_dollar = "\$"
    exp_nome_classe = "^Classe:"
    exp_nome_metodo = "^Metodo:"
    exp_nome_variabile = "^Variabile:"   
    exp_in_line = "^In-Line:"
    nome = ""

    sentences = ""
    
    for line in file:
        new_line = re.search(exp_newLine, line)
        dollar = re.search(exp_dollar,line)
        specialTag = re.search(exp_specialTag, line)
        nome_classe = re.search(exp_nome_classe,line)
        nome_metodo = re.search(exp_nome_metodo,line)
        nome_variabile = re.search ( exp_nome_variabile, line )
        in_line = re.search ( exp_in_line, line )
        if nome_classe or nome_metodo or nome_variabile or in_line:
            nome = line

        if not (new_line or dollar or nome_classe or nome_metodo or nome_variabile or in_line):
            if specialTag:
                split_openTag = line.split(">")
                open_tag = split_openTag[1]
                split_closedTag = open_tag.split("</")
                closed_tag = split_closedTag[0]
                splitNewLine = closed_tag.strip()
                lengtNewLine = splitNewLine.split()
                if len(lengtNewLine) > 2:
                    l = splitNewLine
                else:
                    l = ""
            else:
                l = line.strip()
            sentences = sentences + " " + l
        else:
            #Se la frase contiene solo una parola nn viene salvato nel file temporaneo il commento
            if(len(sentences.split()) > 1):
                sent_strip = sentences.strip()
                new_temp_file.write(sent_strip + "\n")
                new_temp_file_Class.write(nome + "" + sent_strip + "\n")
            sentences = ""

    new_temp_file.close()
    new_temp_file_Class.close()



def find_comment(path):
    #Creo una lista con tutti i path delle classi con estensione ".java" del codice sorgente
    javafiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
                 for name in files
                     if name.endswith(".java")]

    #File contenente tutti i commenti presenti nel codice sorgente
    path_tempComment = os.getcwd() + "/file/comment.txt"
    temp_comment_file = open(path_tempComment,'w')
    
    for el in javafiles:
        file = open(el,'r')

        # creo una stringa temporanea dove salvare i commenti consecutivi
        string_consecutive_comment = ""

        comment_found = False
        found_comm_inline = False
        moreLineClass = False  
        classHeader = ""  
        moreLineMethod = False  
        methodHeader = ""  
        brackets = 0

        for line in file:
            
            notEmptyLine = re.search ( "\S", line )
            if not notEmptyLine:
                continue
            
            # espressione regolare per determinare se una stringa e' o meno un commento
            comment_line = re.match("\s*((\/\/)|(\/\*)|(\/\*\*)|(\*))\s*.*", line)

            # cerco i nomi di tutte le classi nei file con estensione ".java"
            class_name = re.search(
                "((^(?!(\/ | \*).+))\s*((public|private|protected)\s+)?((abstract|final|static)\s+)*((class|interface)\s+\S*)+((extends|implements)\s+\S+)*\s*\{?)",
                line)

            if class_name and not line.__contains__("{"):
                moreLineClass = True
                classHeader = line.strip()
                continue
            if moreLineClass == True:
                classHeader = classHeader + " " + line.strip()
                line = classHeader
                if not line.__contains__("{"):
                    continue
                moreLineClass = False
                class_name = re.search(".*", line)
            
            # cerco i nomi di tutti i metodi nel file
            method_name = re.search(
                "((^(?!(\/ | \*).+))\s*(public|private|protected)?\s+((abstract|final|static)\s+)?((abstract|final|static)\s+)?\S+\s\S+\s*\(.*\)?.*\{?)",                
                line)
            if not method_name:
                method_name = re.search("((^(?!(\/ | \*).+))\s*(public|private|protected)\s+((abstract|final|static)\s+)?((abstract|final|static)\s+)?(\S+\s)?)", line)
                if method_name:
                    moreLineMethod = True
                    methodHeader = line.strip()
            if not method_name:
                method_name = re.search("((^(?!(\/ | \*).+))\s*((public|private|protected)\s+)?(abstract|final|static)\s+((abstract|final|static)\s+)?(\S+\s)?)", line)
                if method_name:
                    moreLineMethod = True
                    methodHeader = line.strip()
                    
            if line.__contains__(";"):
                method_name = None 
                moreLineMethod = False
            if re.search("(\sif\s)|(\selse\s)(\sfor\s)|(\swhile\s)|(\sdo\s)|(\s}\s)|(\stry\s)|(\scatch\s)|(\s&&\s)|(\s\|\|\s)|(\snew\s)|(\sclass\s)|(\s\/\/\s)|(\s(\+|-|<|>|=|==|<=|>=)\s)", line):
                method_name = None
                moreLineMethod = False
            if method_name and not line.__contains__("{"):
                moreLineMethod = True
                methodHeader = line.strip()
                continue
            if moreLineMethod == True:
                if line.__contains__(";"): 
                    method_name = None     
                    moreLineMethod = False 
                methodHeader = methodHeader + " " + line.strip()
                line = methodHeader
                if not line.__contains__("{"):
                    continue
                moreLineMethod = False
                method_name = re.search(".*\(.*\).*{", line)
                                 
            # cerco i nomi di tutte le varibili nel file
            nome_variabile = re.search ( 
                "(\s*(public|private|protected)?\s+((abstract|final|static)\s+)?\S+\s\S+\s*(.+)?\;)",
                line )
            
            if(line.__contains__("{")):
                brackets = brackets + 1
            elif(line.__contains__("}")):
                brackets = brackets - 1
                
            if nome_variabile and brackets > 1:
                nome_variabile = None
            
            #verifico se i commenti hanno annotazioni di sole variabili, se sono commenti autogenerati o (non-Javadoc)
            annotation = re.search("^(\s*\*\s*@\w+\s*\w+)", line)
            java_doc_comment = re.search("\s*\/?\s*\**\(non-Javadoc\)", line)
            special_annotation = re.search("\s*\**\s*(@author|@since|@revision|@see|@link)\s*", line) 
            auto_generated_block = re.search("\s*\/*\s*\**.*(TODO|FIXME|HACK|XXX)", line)


            if comment_line:
                if not (java_doc_comment or special_annotation or auto_generated_block):
                    new_line = line.strip()
                    if not (new_line.__eq__("*") or new_line.__eq__("/*") or new_line.__eq__("/**") or new_line.__eq__("*/")):
                        if line.__contains__("*"):
                            split_star = new_line.split("*")
                            split_line = split_star[1]
                        elif line.__contains__("//"):
                            split_slash = new_line.split("//")
                            split_line = split_slash[1]
                        elif line.__contains__("/*"):
                            split_slashStar = new_line.split("/*")
                            split_line = split_slashStar[1]
                        strip_line = split_line.strip()
                        more_word_line = strip_line.split()
                        
                        if brackets > 1:
                             found_comm_inline = True
                        elif brackets == 1 and found_comm_inline == True:
                             found_comm_inline = False
                             
                        if (annotation and len(more_word_line) > 2):
                            if more_word_line[0] == "@return":
                                more_word_line = more_word_line[2:]
                            else:
                                more_word_line = more_word_line[2:]
                            new_line = ""
                            for el in more_word_line:
                                new_line = new_line + " " + el
                                strip_line = new_line.strip()
                            comment_found = True
                            string_consecutive_comment = string_consecutive_comment + strip_line + "\n"
                        elif (not annotation and len(more_word_line) > 1):
                            comment_found = True
                            string_consecutive_comment = string_consecutive_comment + strip_line + "\n"
            elif (class_name or method_name or nome_variabile or found_comm_inline == True) and comment_found == True:
                if class_name:
                    temp_comment_file.write ("Classe: " + class_name.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                    string_consecutive_comment = ""
                    comment_found = False
                elif method_name:
                    temp_comment_file.write ("Metodo: " + method_name.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                    string_consecutive_comment = ""
                    comment_found = False
                elif nome_variabile:
                    temp_comment_file.write ("Variabile: " + nome_variabile.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                    string_consecutive_comment = ""
                    comment_found = False                
                elif found_comm_inline == True:
                    temp_comment_file.write ("In-Line: " + "\n" + string_consecutive_comment + "\n" )
                    string_consecutive_comment = ""
                    comment_found = False
            else:
                string_consecutive_comment = ""
                comment_found = False
                    
                    
    temp_comment_file.close()
    formatt_comment(path_tempComment)




find_comment(path_SourceCode)


