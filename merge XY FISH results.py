#load python included modules
import ntpath
import os
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
#load additional python modules
import numpy as np
import pandas as pd


# define a function to get the list of all the filename in a directory and its subdirectories
def getListOfFiles(dirName):
    # create a list
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory run the function on that directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        # If entry is a file then add the filename to the list
        else:
            allFiles.append(fullPath)
    return allFiles

# define a function to search for XY FISH results files and merge them
def findAndMerge(filelist):
    # Prepare a dataframe
    df_out = pd.DataFrame(columns=['directory', 'image', 'nul', 'X', 'Y', 'XY','genotype'])
    for file in filelist:
        file_name = ntpath.basename(file)
        dir_name = ntpath.dirname(file)
        #if a FISH results file extract the data and add it to the dataframe as a new row
        if "FISH results.txt" in file_name:
            print("I found a results table!")
            text_file = open(file, "r")
            lines = text_file.readlines()
            text_file.close()
            nul = int(re.findall('\d+',lines[-4])[0])
            X = int(re.findall('\d+',lines[-3])[0])
            Y = int(re.findall('\d+',lines[-2])[0])
            XY = int(re.findall('\d+',lines[-1])[0])
            imagename = file.replace('\\', '/').replace(dirName, '').split(' FISH results.txt')[0]
            df_temp = pd.DataFrame([[dirName, imagename, nul, X, Y, XY]], columns=['directory', 'image', 'nul', 'X', 'Y', 'XY'])
            df_out = df_out.append(df_temp, sort=False, ignore_index=True)
            print("It contains " + str(nul) + " nuls, " + str(X) + " X, " + str(Y) + " Y and " + str(XY) + " XY signal containing nuclei :o")
    return df_out

#required for the dialog boxes
root = tk.Tk()
root.withdraw()

# Prepare a dataframe
df_merged = pd.DataFrame(columns=['directory', 'image', 'nul', 'X', 'Y', 'XY','genotype'])

#loop until all genotypes are merged
go_on = True
while(go_on):
    #ask for a directory
    dirName = filedialog.askdirectory(title = "Choose a folder containing results from 1 genotype")

    #get filelist and search for chr3 FISH results files
    filelist = getListOfFiles(dirName)
    df_out = findAndMerge(filelist)

    #ask user to specify the genotype
    genotype = simpledialog.askstring(title = None, prompt = "Enter genotype")
    df_out["genotype"] = genotype
    df_merged = df_merged.append(df_out, sort = False, ignore_index = True)
    go_on = messagebox.askyesnocancel(title = None, message="Add another genotype?")

#calculate the aneuploidy ratio of spermatids
df_merged['aneuploidy ratio'] = ((2*df_merged['XY'])/(df_merged['Y']+df_merged['X']+2*df_merged['XY']))

#ask the user where to save the final dataframe
save_path = filedialog.asksaveasfilename(title='Save compiled results as ...',defaultextension = '.xlsx',initialdir = dirName, initialfile = "compiled FISH results");
df_merged.to_excel(save_path, index=False)
print('done')
                            
