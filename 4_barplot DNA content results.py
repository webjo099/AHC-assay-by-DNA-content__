#load python included modules
import tkinter as tk
from tkinter import filedialog
#load additional python modules
import numpy as n
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#required for the dialog box
root = tk.Tk()
root.withdraw()

#ask for a file
file_path = filedialog.askopenfilename(title = "Select the compiled DNA content results file")

#open file
df_cells = pd.read_excel(file_path, index_col=None)

#define genotypes to be plotted
ls_gt = list(df_cells.genotype.unique())
data = df_cells.drop_duplicates(subset=['genotype','ImageNumber'], keep='first', inplace=False)

#define plot
plt.figure(figsize=(4,6))
ax = plt.subplot(1,1,1)
ax.set_title('DNA content variation per cyst')
#add columns to plot
sns.barplot(x="genotype", y="img_stdev", data=data, errwidth=1, capsize=0.3, color="white", ci="sd", linewidth=1, edgecolor="black", order = ls_gt)
#add datapoints to plot
sns.stripplot(x="genotype", y="img_stdev", data=data, jitter=True, color="green", size=4, linewidth=0, order = ls_gt)

# create plot
plt.xticks(rotation=90)
plt.tight_layout()
plt.margins(x=None, y=0.4, tight=True)
plt.show()
