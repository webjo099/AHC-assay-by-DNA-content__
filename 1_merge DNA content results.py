#load python included modules
import os
import ntpath
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
#load additional python modules
import numpy as np
import pandas as pd


#create function to get a list of all files in a directory and its subdirectories
def getListOfFiles(dirName):
    #list files in directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)           
    return allFiles

# define a function to search for DNA content results files and merge them
def findAndMerge(filelist):
    # Prepare a dataframe
    df_out = pd.DataFrame()
    ImageNumber = 1
    for file in filelist:
        file_name = ntpath.basename(file)
        dir_name = ntpath.dirname(file)
        #when finding a DNA content results file at the data to the dataframe, adjust image number
        if " DNA content.xls" in file_name:
            df_cells = pd.read_csv(file, sep='\t')
            df_cells["ImageNumber"] = ImageNumber
            df_out = df_out.append(df_cells, sort=False, ignore_index=True)
            ImageNumber = ImageNumber + 1
            print("I found results table " + file_name)
    return df_out

#required for the dialog boxes
root = tk.Tk()
root.withdraw()

#create empty dataframe
df_merged = pd.DataFrame()

#loop until all genotypes are merged
go_on = True
while(go_on):
    #ask for a directory
    dirName = filedialog.askdirectory(title = "Choose a folder containing results from 1 genotype")

    #get filelist and 
    filelist = getListOfFiles(dirName)
    df_out = findAndMerge(filelist)

    #ask user to specify the genotype
    genotype = simpledialog.askstring(title = None, prompt = "Enter genotype")
    df_out["genotype"] = genotype
    df_merged = df_merged.append(df_out, sort = False, ignore_index = True)
    go_on = messagebox.askyesnocancel(title = None, message="Add another genotype?")

#set the label of the first column to objectnumber
df_merged.columns.values[[0]] = ["ObjectNumber"]

#save
save_path = filedialog.asksaveasfilename(title='Save compiled results as ...',defaultextension = '.xlsx',initialdir = dirName, initialfile = "compiled DNA content results");
df_merged.to_excel(save_path, index=False)
print('done')
