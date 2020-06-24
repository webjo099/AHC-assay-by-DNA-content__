#load python included modules
import ntpath
import tkinter as tk
from tkinter import filedialog
#load additional python modules
import numpy as np
import pandas as pd

#required for the dialog box
root = tk.Tk()
root.withdraw()

#ask for a file
file_path = filedialog.askopenfilename(title = "Select the compiled DNA content results file")

#open file
df_cells = pd.read_excel(file_path, index_col=None)
dirName = ntpath.dirname(file_path)

#get a list with all the genotypes in the dataframe
gt_ls = df_cells.genotype.unique()

#calcute internal standard deviation for each image
for gt in gt_ls:
    img_ls = df_cells.loc[df_cells['genotype'] == gt].ImageNumber.unique()
    for img in img_ls:
        img_stdev = df_cells.loc[(df_cells['genotype'] == gt) & (df_cells['ImageNumber'] == img), 'norm signal'].std(axis=0)
        df_cells.loc[(df_cells['genotype'] == gt) & (df_cells['ImageNumber'] == img), 'img_stdev'] = img_stdev

    #calcute mean standard deviation each genotype
    mean_img_stdev = df_cells.loc[df_cells['genotype'] == gt].drop_duplicates(subset ="ImageNumber", keep = "first", inplace = False)["img_stdev"].mean(axis=0)
    df_cells.loc[(df_cells['genotype'] == gt), 'mean_img_stdev'] = mean_img_stdev

save_path = filedialog.asksaveasfilename(title='Save compiled results as ...',defaultextension = '.xlsx',initialdir = dirName, initialfile = "compiled DNA content results");
df_cells.to_excel(save_path, index=False)
print('done')
