#load python included modules
import math
import random
import tkinter as tk
from tkinter import filedialog
import itertools as itt
#load additional python modules
import numpy as np
import pandas as pd

#define DNA content of drosophila chromosomes in Mb
X=22.4
Y=40
chr2=44.1
chr3=52.4
chr4=1.4

#function to create 4 spermatids with normal segregation in meiosis I and II
def spermatid_wt():
    #create spermatids
    spermatidA = [X, chr2, chr3, chr4]
    spermatidB = [Y, chr2, chr3, chr4]
    #calculate DNA content
    DNA_spermA = disc_from_sphere(sum(spermatidA))
    DNA_spermB = disc_from_sphere(sum(spermatidB))
    #return 4 values of DNA content
    return [DNA_spermA, DNA_spermB, DNA_spermA, DNA_spermB]

#function to create 4 spermatids with random segregation in meiosis I but normal segregation in meiosis II
def spermatid_random():
    #create spermatids
    spermatidA = []
    spermatidB = []
    for c in [X, Y, chr2, chr2, chr3, chr3, chr4, chr4]:
        if random.choice([0,1]) == 1:
            spermatidA.append(c)
            spermatidB.append(0)
        else:
            spermatidA.append(0)
            spermatidB.append(c)
    #calculate DNA content
    DNA_spermA = disc_from_sphere(sum(spermatidA))
    DNA_spermB = disc_from_sphere(sum(spermatidB))

    #return 4 values of DNA content
    return [DNA_spermA, DNA_spermB, DNA_spermA, DNA_spermB]

#function to create 4 spermatids with random segregation of autosomes in meiosis I but normal segregation in meiosis II
def spermatid_random_autosomes():
    #create spermatids
    spermatidA = [X]
    spermatidB = [Y]
    for c in [chr2, chr2, chr3, chr3, chr4, chr4]:
        if random.choice([0,1]) == 1:
            spermatidA.append(c)
            spermatidB.append(0)
        else:
            spermatidA.append(0)
            spermatidB.append(c)
    #calculate DNA content
    DNA_spermA = disc_from_sphere(sum(spermatidA))
    DNA_spermB = disc_from_sphere(sum(spermatidB))
    #return 4 values of DNA content
    return [DNA_spermA, DNA_spermB, DNA_spermA, DNA_spermB]

#create a cyst of 64 spermatids with the defined segregation mode
def make_cyst(mode):
    cyst = []
    for i in range(16):
        if (mode == 'wt'):
            cyst.extend(spermatid_wt())
        if (mode == 'random'):
            cyst.extend(spermatid_random())
        if (mode == 'autosomal_random'):
            cyst.extend(spermatid_random_autosomes())
    #normalize DNA content in cyst and randomize the order
    cyst = cyst/np.average(cyst)
    random.shuffle(cyst)
    return cyst

#function that converst the volume of a sphere into the area of the equator disc
def disc_from_sphere(volume):
    area = pow(math.pi, 1/3)*pow(6*volume, 2/3)
    return area

#calculate average stdev within a cyst for each segregation mode
for mode in ['wt', 'random', 'autosomal_random']:
    ls_stdev = []
    for i in range(1000):
        cyst = make_cyst(mode)
        ls_stdev.append(np.std(cyst))
    print("average intracyst standard deviation for mode " + mode)
    print(np.mean(ls_stdev))
    print("intercyst standard deviation for mode " + mode)
    print(np.std(ls_stdev))
    
#create a dataframe with modeled data to export as .xlsx
modeled_df = pd.DataFrame()
for mode in ['wt', 'random', 'autosomal_random']:
    mode_df = pd.DataFrame()
    for i in range(20):
        cyst = make_cyst(mode)
        data = {'ObjectNumber': range(1,65), 'norm signal': cyst}
        cyst_df = pd.DataFrame(data = data)
        #optional: mimic limits of the DNA content analyses by removing all nuclei that have less than 10Mb of DNA
        #cyst_df = cyst_df.loc[cyst_df['norm signal'] >= 10]
        cyst_df["ImageNumber"] = i+1
        cyst_df["img_stdev"] = np.std(cyst)
        mode_df = mode_df.append(cyst_df)
    mode_df["genotype"] = "modeled data, segregation type " + mode
    #calcute mean standard deviation
    mean_img_stdev = mode_df.drop_duplicates(subset ="ImageNumber", keep = "first", inplace = False)["img_stdev"].mean(axis=0)
    mode_df["mean_img_stdev"] = mean_img_stdev
    #mode_df["mean_img_stdev"] = cyst_df['img_stdev'].unique().mean(axis=0)
    modeled_df = modeled_df.append(mode_df)

#required for the dialog box
root = tk.Tk()
root.withdraw()

#export as .xlsx
save_path = filedialog.asksaveasfilename(title='Save modeled results as ...',defaultextension = '.xlsx', initialfile = "modeled DNA content results");
modeled_df.to_excel(save_path, index=False)
print('done')





