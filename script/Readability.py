from nltk import word_tokenize
from nltk.corpus import stopwords
from textstat.textstat import textstat
from distutils.dir_util import mkpath

import os
import re
import sys


pac = sys.argv[1]

mkpath( os.getcwd() + "/file/metriche/" )
mkpath( os.getcwd () + "/file/" + pac )


outfile = open(os.getcwd () + "/file/metriche/Metriche_" + pac + ".txt", "a")




def commentsReadability():
    path_comment = os.getcwd() + "/file/comment.txt"
    file = open ( path_comment, 'r' )
    path_NewCommentFile = os.getcwd () + "/file/comment_readability.txt"
    new_temp_file = open ( path_NewCommentFile, 'w' )
    
    total_flesch = 0
    total_kincaid = 0
    total_fog = 0
    num_comment = 0

    exp_newLine = "^\s"
    exp_nome_classe = "^Classe:"
    exp_nome_metodo = "^Metodo:"
    exp_nome_variabile = "^Variabile:"
    exp_in_line = "^In-Line:"
    nome = ""

    sentences = ""
    
    for line in file:
        new_line = re.match ( exp_newLine, line )
        nome_classe = re.search ( exp_nome_classe, line )
        nome_metodo = re.search ( exp_nome_metodo, line )
        nome_variabile = re.search ( exp_nome_variabile, line )
        in_line = re.search ( exp_in_line, line )
        if nome_classe or nome_metodo or nome_variabile or in_line:
            nome = line

        if not (new_line or nome_classe or nome_metodo or nome_variabile or in_line):
            l = line.strip()
            sentences = sentences + " " + l
        
        elif new_line:
            if (len ( sentences.split () ) > 1):
                sent_strip = sentences.strip ()
                new_temp_file.write (nome + sent_strip)
            sentences = ""
            
            flesch_reading_ease = textstat.flesch_reading_ease (sent_strip)
            total_flesch = total_flesch + flesch_reading_ease
            flesch_kincaid_grade = textstat.flesch_kincaid_grade (sent_strip)
            total_kincaid = total_kincaid + flesch_kincaid_grade
            gunning_fog = textstat.gunning_fog (sent_strip)
            total_fog = total_fog + gunning_fog

            new_temp_file.write ("\nflesch_reading_ease: " + flesch_reading_ease.__str__())
            new_temp_file.write ("\nflesch_kincaid_grade: " + flesch_kincaid_grade.__str__())
            new_temp_file.write ("\ngunning_fog: " + gunning_fog.__str__())
            new_temp_file.write ("\n\n" )
            
            num_comment = num_comment + 1

    new_temp_file.close ()
    
    if num_comment == 0:
        num_comment = 1
        
    averageFlesch = total_flesch / float(num_comment)
    averageKincaid = total_kincaid / float(num_comment)
    averageFog = total_fog / float(num_comment)

    outfile.write("\nflesch_reading_ease: " + averageFlesch.__str__())
    outfile.write ("\nflesch_kincaid_grade: " + averageKincaid.__str__())
    outfile.write("\ngunning_fog: " + averageFog.__str__())


  
commentsReadability()    
