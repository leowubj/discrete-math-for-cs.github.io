from userFunctions import *
from zipfile import ZipFile
import re
from os.path import basename

#function which creates zip file with all images and tex file 
def zip_file(filename, path): 
    #this is the current path of the tex file 
    currentPath = "generated/notes/"+path+"/"+filename+".tex" 
    
    #new path of the tex file
    newPath=  "generated/notes/"+path+"/new-"+filename+".tex"
    
    #file object of the tex file, opened from current path
    texFile=""; 
    try: 
            texFile = open(currentPath, "r+")
    except IOError as e:
            print(e)
            return
    texString = texFile.readlines()

    #contents of new tex file will be in this string
    newTexFile = open(newPath, "w") 
    newTexString = ""
    

    #zip object created with tex file and associated images
    zipObj= ""; 
    try:
        zipObj = ZipFile("generated/notes/"+path+"/"+filename+".zip", 'w')
    except IOError as e:
        print(e)
        return
    
    

    #image list with image file names such as "image.png"
    imageList = [] 


    #what this for loop does: 
    #1. finds the lines starting with include graphics and alters 
    #the path of the images from ../../resources/images/image.png, to just be
    #image.png 
    #2. stores the image file name ("image.png") in imageList in order to write it 
    #to the zip file
    for line in texString:
        if ("\includegraphics" in line):
            replaced = line.replace("../","").replace("resources/images/","")
            #DEBUG
            #print(replaced)
            #newTexString += replaced 
            
            #include graphics in regex 
            #handles edge case where things like "\begin{center}"  
            # is on the same line as image, as we are taking the filename from between brackets 
            # and "center" does not count as an image name
            imageFile = re.findall(r'\{.*?\}', line)
            for element in imageFile :
                if "/images" in element:
                    element = element.replace("{","").replace("}","").replace("../","")
                    imageList.append(element) 
        else : 
            newTexString += line
        

    #write replaced image file paths into the new tex files 
    newTexFile.write(newTexString)

    #set(imageList) will remove any duplicates of the same image file name 
    imageList = list(set(imageList))

    #DEBUG
    #nlines=texString.count('\n')
    #print(nlines)
    #print(filename)
    #print(imageList)

    if(len(imageList)!=0):
        zipObj.write(newPath,basename(newPath))
        for element in imageList:
            zipObj.write(element, basename(element)) 
        
        return "../notes/"+path+"/"+filename+".zip" 
    else: 
        
        return "../notes/"+path+"/"+filename+".tex"

#DEBUG test
#zip_file("Week2", "lessons-flat")