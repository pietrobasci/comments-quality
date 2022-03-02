from nltk import word_tokenize
from nltk.corpus import stopwords
from textstat.textstat import textstat
from distutils.dir_util import mkpath

import os
import re
import sys


percorso = sys.argv[1]
pac = sys.argv[2]

path_SourceCode = percorso + pac

mkpath( os.getcwd() + "/file/metriche/" )
mkpath( os.getcwd () + "/file/" + pac )


outfile = open(os.getcwd () + "/file/metriche/Metriche_" + pac + ".txt", "w")



def find_comment(path):
    numero_classi = 0
    numero_metodi = 0
    numero_variabili = 0
    numero_commenti_classi = 0
    numero_commenti_metodi = 0
    numero_commenti_variabili = 0
    numero_commentiIN = 0
    numero_commentiSp = 0
    numero_commentiJV = 0
    numero_classi2 = 0 
    loc = 0
    line_comment = 0

    # Creo una lista con tutti i path delle classi con estensione ".java" del codice sorgente
    javafiles = [os.path.join ( root, name )
                 for root, dirs, files in os.walk ( path )
                     for name in files
                         if name.endswith ( ".java" )]


    for el in javafiles:
        numero_classi = numero_classi + 1   
        
        temp = el.split ( "/" )
        temp1 = temp[temp.__len__ () - 1].split ( "\\" )
        path_tempComment = os.getcwd () + "/file/" + pac + "/" + temp1[temp1.__len__ () - 1] + ".txt"
        temp_comment_file = open ( path_tempComment, 'w' )
        file = open ( el, 'r' )

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
            comment_line = re.match ( "\s*((\/\/)|(\/\*)|(\/\*\*)|(\*))\s*.*", line )
            if comment_line:
                line_comment = line_comment + 1
            else:
                loc = loc + 1

            # cerco i nomi di tutte le classi nei file con estensione ".java"
            class_name = re.search (
                "((^(?!(\/ | \*).+))\s*((public|private|protected)\s+)?((abstract|final|static)\s+)*((class|interface)\s+\S*)+((extends|implements)\s+\S+)*\s*\{?)",
                line )

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

            if (class_name):
                numero_classi2 = numero_classi2 + 1
            
            # cerco i nomi di tutti i metodi nel file
            method_name = re.search (
                "((^(?!(\/ | \*).+))\s*(public|private|protected)?\s+((abstract|final|static)\s+)?((abstract|final|static)\s+)?\S+\s\S+\s*\(.*\)?.*\{?)",                
                line )
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

            if(method_name):
                numero_metodi = numero_metodi + 1
            
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
            if comment_line:
                nome_variabile = None
                    
            if(nome_variabile):
                numero_variabili = numero_variabili + 1

            # verifico se i commenti hanno annotazioni di sole variabili, se sono commenti autogenerati o (non-Javadoc)
            annotation = re.search ( "^(\s*\*\s*@\w+\s*\w+)", line )
            java_doc_comment = re.search ( "\s*\/?\s*\**\(non-Javadoc\)", line )
            special_annotation = re.search ( "\s*\**\s*(@author|@since|@revision|@see|@link)\s*", line ) ##
            auto_generated_block = re.search ( "\s*\/*\s*\**.*(TODO|FIXME|HACK|XXX)", line )
            special_annotationVar = re.search ( "\s*\**\s*(@param|@return|@throws)\s*", line )
            if special_annotationVar:
                numero_commentiSp = numero_commentiSp + 1
            if java_doc_comment:
                numero_commentiJV = numero_commentiJV + 1

            if comment_line:
                if not (java_doc_comment or special_annotation or auto_generated_block):
                    new_line = line.strip ()
                    if not (new_line.__eq__ ( "" ) or new_line.__eq__ ( "/" ) or new_line.__eq__ ( "/**" ) or new_line.__eq__ ( "*/" )):
                        if line.__contains__ ( "*" ):
                            split_star = new_line.split ( "*" )
                            split_line = split_star[1]
                        elif line.__contains__ ( "//" ):
                            split_slash = new_line.split ( "//" )
                            split_line = split_slash[1]
                        elif line.__contains__ ( "/*" ):
                            split_slashStar = new_line.split ( "/*" )
                            split_line = split_slashStar[1]
                        strip_line = split_line.strip ()
                        more_word_line = strip_line.split ()
                        
                        if brackets > 1:
                            found_comm_inline = True
                        elif brackets == 1 and found_comm_inline == True:
                            found_comm_inline = False
                            
                        if (annotation and len ( more_word_line ) > 2):
                            new_line = ""
                            for el in more_word_line:
                                new_line = new_line + " " + el
                                strip_line = new_line.strip ()
                            comment_found = True
                            string_consecutive_comment = string_consecutive_comment + strip_line + "\n"
                        elif (not annotation and len ( more_word_line ) > 1):
                            comment_found = True
                            string_consecutive_comment = string_consecutive_comment + strip_line + "\n"
            elif class_name:
                temp_comment_file.write ("Classe: " + class_name.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                if comment_found:
                    numero_commenti_classi = numero_commenti_classi + 1
                string_consecutive_comment = ""
                comment_found = False
            elif method_name:
                temp_comment_file.write ("Metodo: " + method_name.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                if comment_found:
                    numero_commenti_metodi = numero_commenti_metodi + 1
                string_consecutive_comment = ""
                comment_found = False
            elif nome_variabile:
                temp_comment_file.write ("Variabile: " + nome_variabile.group ( 0 ) + "\n" + string_consecutive_comment + "\n" )
                if comment_found:
                    numero_commenti_variabili = numero_commenti_variabili + 1
                string_consecutive_comment = ""
                comment_found = False            
            elif found_comm_inline == True and comment_found == True:
                temp_comment_file.write ("In-Line: " + "\n" + string_consecutive_comment + "\n" )
                if comment_found:
                    numero_commentiIN = numero_commentiIN + 1
                string_consecutive_comment = ""
                comment_found = False
            else:
                string_consecutive_comment = ""
                comment_found = False
    
    temp_comment_file.close ()
    
    
    commentiTotali = numero_commenti_classi + numero_commenti_metodi + numero_commenti_variabili + numero_commentiIN
    anyj = (numero_commenti_classi + numero_commenti_metodi + numero_commenti_variabili) / float(numero_classi2 + numero_metodi + numero_variabili)
    if numero_metodi == 0:
        anyc = 1.0
    else:
        anyc = numero_commenti_metodi / float(numero_metodi)
    densityComments = (line_comment / float(line_comment + loc)) * 100


    outfile.write("\nNumber_of_Classes: " + str ( numero_classi2 ))
    outfile.write("\nNumber_of_Methods: " + str ( numero_metodi ))
    outfile.write("\nNumber_of_Variables: " + str ( numero_variabili ))
    outfile.write( "\nNumber_of_Comments_on_Classes: " + str ( numero_commenti_classi ) )
    outfile.write( "\nNumber_of_Comments_on_Methods: " + str ( numero_commenti_metodi ) )
    outfile.write( "\nNumber_of_Comments_on_Variables: " + str ( numero_commenti_variabili ) )
    outfile.write( "\nNumber_of_In_Line_Comments: " + str ( numero_commentiIN ) )
    outfile.write("\nTotal_Number_of_Comments: " + str(commentiTotali))
    outfile.write("\nANYJ: " + str(anyj))
    outfile.write ("\nANYC: " + str(anyc))
    outfile.write("\nLOC: " + str(loc))
    outfile.write("\nLine_of_Comment: " + str(line_comment))
    outfile.write("\nComments_Density: " + str(densityComments))

        
    return commentiTotali



def removeStopWords(tokens):
    
    stop_words = set ( stopwords.words ( 'english' ) )
    stop_words.update (
        ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',
         '<','>','$','``','id',' '' ',
         #campi aggiunti
         'The','To','an','For','If','In','It','Then'
         ] )
    
    filtered_sentence = []
    for w in tokens:
        if w not in stop_words:
            filtered_sentence.append ( w )
    
    return filtered_sentence



def WPJC(path, n_comment):
    f = open(path, 'rU')
    text = f.read()
    token_text = word_tokenize (text)
    filtered_tokens = removeStopWords(token_text)
    n_token = len(filtered_tokens)
    if n_comment == 0:
        n_comment = 1
    wpjc = n_token / float(n_comment)
    outfile.write("\nWPJC: " + str(wpjc))
  
  
 
 
path = os.getcwd() + "/file/Totale_" + pac + ".txt" 
com = find_comment ( path_SourceCode ) 
WPJC(path, com)

