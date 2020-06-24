#load python included modules
import tkinter as tk
from tkinter import filedialog
#load additional python modules
import numpy as n
import pandas as pd
import matplotlib.pyplot as plt

#add image standard deviation on plot?
stdev_on_plot = True
#add genotype standard deviation in header?
stdev_in_head = True
#add image number to plot?
imagenumber_in_plot = True

#required for the dialog box
root = tk.Tk()
root.withdraw()

#ask for a file
file_path = filedialog.askopenfilename(title = "Select the compiled DNA content results file")

#open file
df_cells = pd.read_excel(file_path, index_col=None)

#define genotypes to be plotted
ls_gt = list(df_cells.genotype.unique())
n_gt = len(ls_gt)

#find max number of cells to define plot limits
max_cells = 64
for gt in ls_gt:
    cells = df_cells.loc[df_cells['genotype'] == gt].shape[0]
    if cells > max_cells:
        max_cells = cells

#create figure
axis = [0, max_cells, 0, 3]
plt.figure(figsize=(6,10))
pos=1

for gt in ls_gt:
    #define plot position
    plt.subplot(n_gt,1,pos)
    #select values to plot
    df_gt = df_cells.loc[df_cells['genotype']==gt]
    #sort cysts according to standard deviation
    df_gt = df_gt.sort_values('img_stdev', ascending = True)
    x = range(0,len(df_gt))
    y = df_gt['norm signal'].values
    #give alternate colors to cells from different cysts
    color = ["black","red"]*len(df_gt['ImageNumber'].unique())
    for image in df_gt['ImageNumber'].unique():
        df_gt.loc[df_gt['ImageNumber'] == image, "color"] = color[0]
        color.pop(0)
    c = df_gt["color"].values
    
    #set plot settings
    plt.scatter(x, y, c=c, s=2)
    plt.axis(axis)
    plt.yticks([0,0.5,1,1.5,2,2.5,3], [0,'', 1, '', 2, '', 3])
    plt.grid(color='gray', linestyle='--', linewidth=1, axis='y')
    pos = pos+1
    plt.title(gt)
    
    #add standard deviation to the plot titles
    if stdev_in_head:
        gt_stdev = df_gt.loc[(df_gt['genotype'] == gt) & (df_gt['ObjectNumber'] == 1), 'mean_img_stdev'].values[0]
        plt.title(gt + " (stdev: " + str(round(gt_stdev,2)) + ')')
        
    #add image labels to plot
    if imagenumber_in_plot:
        for image in df_gt['ImageNumber'].unique():
            df_gt = df_gt.reset_index(drop=True)
            the_middle = len(df_gt[df_gt.ImageNumber == image].index)/2
            the_x = df_gt[df_gt.ImageNumber == image].index[int(the_middle)]
            plt.text(the_x, 0.1, image, fontsize=5)

    #add standard deviation as grey lines to plot
    if stdev_on_plot:
        y2 = df_gt["img_stdev"].values + 1
        plt.scatter(x, y2, c="gray", s=1)
        y3 = -df_gt["img_stdev"].values + 1
        plt.scatter(x, y3, c="gray", s=1)

#create plot
plt.tight_layout()
plt.show()



