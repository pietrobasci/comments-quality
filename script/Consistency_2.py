import os
import re
import sys
from distutils.dir_util import mkpath


pac = sys.argv[1]
mkpath( os.getcwd() + "/file/metriche/" )


path = os.getcwd() + "/file/" + pac
outfile = open(os.getcwd () + "/file/metriche/Metriche_" + pac + ".txt", "a")


txtfiles = [os.path.join ( root, name )
                 for root, dirs, files in os.walk ( path )
                     for name in files
                         if name.endswith ( ".txt" )]



def DIR():
    
    N_Methods = 0
    N_WithTag = 0
    
    
    for file in txtfiles:
        
        f1 = open(file,'r')
        methodCommentStart = False
        N_MethodsReturn = 0
        N_ReturnTag = 0    
        N_MethodsParam = 0
        N_ParamTag = 0 
        N_MethodsException = 0
        N_ExceptionTag = 0 
        found = 0
            
        for line in f1:
            methodFound = re.match("Metodo: ", line)
            
            if methodFound:
                MethodReturn = True
                MethodParam = True
                MethodExcept = True             
                N_MethodsReturn = 0
                N_ReturnTag = 0    
                N_MethodsParam = 0
                N_ParamTag = 0 
                N_MethodsException = 0
                N_ExceptionTag = 0 
                found = 0

                methodWords = line.split()
                returnType = methodWords[1:]
                N_MethodsReturn = N_MethodsReturn + 1      
                
                if re.match("(public|private|protected)", returnType[0]):
                    returnType = returnType[1:]
                if re.match("(final|static|abstract)", returnType[0]):
                    returnType = returnType[1:]
                if re.match("(final|static|abstract)", returnType[0]):
                    returnType = returnType[1:]
                if returnType[0] == "void":
                    N_MethodsReturn = N_MethodsReturn - 1 
                    MethodReturn = False     
                if returnType[0].__contains__("("):   
                    N_MethodsReturn = N_MethodsReturn - 1  
                    MethodReturn = False     
                

                parameterWord = methodWords
                parameter = []
                
                for word in methodWords:
                    if not parameterWord[0].__contains__("("):
                        parameterWord = parameterWord[1:]
                    else:
                        break
                
                for word in parameterWord:
                    if not parameterWord[(len (parameterWord) - 1)].__contains__(")"):
                        parameterWord = parameterWord[:(len (parameterWord) - 1)]
                    else:
                        break 
                 
                i = 0
                for word in parameterWord:
                    if i%2==1:
                        parameter.append(parameterWord[i].strip(",").strip("{").strip(")").strip(");").strip("[]"))
                    i = i + 1

                if len(parameter) == 0:
                    MethodParam = False
                else:
                    N_MethodsParam = N_MethodsParam + len(parameter)
                

                exceptionType = methodWords
                
                if re.search("(throws)", line):
                    for word in methodWords:
                        if not re.match("(throws)", exceptionType[0]):
                            exceptionType = exceptionType[1:]
                        else:
                            exceptionType = exceptionType[1:]
                            break
                    N_MethodsException = N_MethodsException + len(exceptionType)
                else:   
                    MethodExcept = False

                 
                if MethodReturn or MethodParam or MethodExcept:
                    N_Methods = N_Methods + 1  
                    methodCommentStart = True
                else:
                    methodCommentStart = False
             
                continue
            
            
            if methodCommentStart and not line == "\n":
                if re.search("@return", line) and N_MethodsReturn > N_ReturnTag:  
                    N_ReturnTag = N_ReturnTag + 1;  
                if re.search("@param", line) and N_MethodsParam > N_ParamTag:  
                    N_ParamTag = N_ParamTag + 1; 
                if re.search("@throws|@exception", line) and N_MethodsException > N_ExceptionTag:
                    N_ExceptionTag = N_ExceptionTag + 1;   
                if N_MethodsReturn == N_ReturnTag and N_MethodsParam == N_ParamTag and N_MethodsException == N_ExceptionTag:
                    if not (N_MethodsReturn + N_MethodsParam + N_MethodsException) == found: 
                        N_WithTag = N_WithTag + 1  
                        found = found + 1
            else:
                methodCommentStart = False


    print(str(N_WithTag) + " " + str(N_Methods)) 
    if N_Methods == 0:
        return 100
    else:
        return ( N_WithTag / float(N_Methods) ) * 100    



def RSYNC():
    
    N_Methods = 0
    N_ReturnTag = 0
    
    for file in txtfiles:
        
        f1 = open(file,'r')
        methodCommentStart = False

        for line in f1:
            methodFound = re.match("Metodo: ", line)

            if methodFound:
                N_Methods = N_Methods + 1
                methodCommentStart = True
                methodWords = line.split()
                returnType = methodWords[1:]
                
                if re.match("(public|private|protected)", returnType[0]):
                    returnType = returnType[1:]
                if re.match("(final|static|abstract)", returnType[0]):
                    returnType = returnType[1:]
                if re.match("(final|static|abstract)", returnType[0]):
                    returnType = returnType[1:]
                if returnType[0] == "void":
                    N_Methods = N_Methods - 1      
                    methodCommentStart = False    
                if returnType[0].__contains__("("):   
                    N_Methods = N_Methods - 1      
                    methodCommentStart = False    
                          
                continue
            
            if methodCommentStart and not line == "\n":
                if not re.search("@return", line):  
                    continue    
                if re.match("(@return " + returnType[0].strip("[]") + ".* .)", line):
                    N_ReturnTag = N_ReturnTag + 1
            else:
                methodCommentStart = False
   
    if N_Methods == 0:
        return 100
    else:
        return ( N_ReturnTag / float(N_Methods) ) * 100    

 
 
    
def PSYNC():
    
    N_Methods = 0
    N_ParameterTag = 0
    
    for file in txtfiles:
        
        f1 = open(file,'r')
        methodCommentStart = False
        found = 0

        for line in f1:
            methodFound = re.match("Metodo: ", line)

            if methodFound:
                N_Methods = N_Methods + 1

                methodCommentStart = True
                methodWords = line.split()
                parameterWord = methodWords
                parameter = []

                for word in methodWords:
                    if not parameterWord[0].__contains__("("):
                        parameterWord = parameterWord[1:]
                    else:
                        break
                
                for word in parameterWord:
                    if not parameterWord[(len (parameterWord) - 1)].__contains__(")"):
                        parameterWord = parameterWord[:(len (parameterWord) - 1)]
                    else:
                        break 
                 
                i = 0
                for word in parameterWord:
                    if i%2==1:
                        parameter.append(parameterWord[i].strip(",").strip("{").strip(")").strip(");").strip("[]"))
                    i = i + 1

                if len(parameter) == 0:
                    N_Methods = N_Methods - 1      
                    methodCommentStart = False

                continue
           
                        
            if methodCommentStart and not line == "\n":
                if not re.search("@param", line):  
                    continue 
                for word in parameter:
                    if re.match("(@param " + word + ".* .)", line):
                        found = found + 1

                if found == len (parameter):
                    N_ParameterTag = N_ParameterTag + 1
                    found = 0
                           
            else:
                methodCommentStart = False
    
    
    if N_Methods == 0:
        return 100
    else:
        return ( N_ParameterTag / float(N_Methods) ) * 100    

      
    

def ESYNC():
    
    N_Methods = 0
    N_ExeptionTag = 0
    
    for file in txtfiles:
        
        f1 = open(file,'r')
        methodCommentStart = False
        found = 0

        for line in f1:
            methodFound = re.match("Metodo: ", line)

            if methodFound:
                N_Methods = N_Methods + 1

                if not re.search("(throws)", line):
                    N_Methods = N_Methods - 1      
                    continue
                
                methodCommentStart = True
                methodWords = line.split()
                exceptionType = methodWords
                
                for word in methodWords:
                    if not re.match("(throws)", exceptionType[0]):
                        exceptionType = exceptionType[1:]
                    else:
                        exceptionType = exceptionType[1:]
                        break
                 
                continue
            
            
            if methodCommentStart and not line == "\n":
                if not re.search("@throws|@exception", line):
                    continue  
                for word in exceptionType:
                    if re.match("(@throws " + word.strip("{").strip(",").strip(";") + " .)", line):
                        found = found + 1
                    if re.match("(@exception " + word.strip("{").strip(",").strip(";") + " .)", line):
                        found = found + 1
                if found == len (exceptionType):
                    N_ExeptionTag = N_ExeptionTag + 1
                    found = 0
                           
            else:
                methodCommentStart = False
    
    print(str(N_Methods))
    print(str(N_ExeptionTag))
   
    if N_Methods == 0:
        return 100
    else:
        return ( N_ExeptionTag / float(N_Methods) ) * 100    

 
   
rsync = RSYNC()
psync = PSYNC()    
esync = ESYNC()  
dir = DIR()  

outfile.write("\nRSYNC: " + str(rsync) )
outfile.write("\nPSYNC: " + str(psync) )
outfile.write("\nESYNC: " + str(esync) )
outfile.write("\nDIR: " + str(dir) )

print("rsync: " + str(rsync))
print("psync: " + str(psync))
print("esync: " + str(esync))    
print("DIR: " + str(dir))    
