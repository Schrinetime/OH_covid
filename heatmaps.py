# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 18:43:04 2020

@author: schri
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.dates as md
import datetime as dt

csv_loc = "https://coronavirus.ohio.gov/static/COVIDSummaryData.csv"
df = pd.read_csv(csv_loc,thousands=',')

df = df[df['Onset Date'] != 'Total']

for col in ['Onset Date','Date Of Death','Admission Date']:
    df[col] = pd.to_datetime(df[col],errors='coerce')

#%%

outcomes = [
    'Case Count',
    'Death Count',
    'Hospitalized Count'
    ]

for outcome in outcomes:
    age_fig, age_ax = plt.subplots()
    
    age_ranges = list(df.groupby('Age Range').groups.keys())
    age_ranges.remove('Unknown')
    
    df['date_bin'] = pd.cut(df['Onset Date'],bins=26)
    date_bins = list(df.groupby('date_bin').groups.keys())
    
    count = np.zeros((len(age_ranges), len(date_bins)))
    
    for i, age_range in enumerate(age_ranges):
        
        for j, date_range in enumerate(date_bins):
            
            count[i, j] = np.sqrt(df.loc[df['Age Range'].isin([age_range]) & df['date_bin'].isin([date_range]),outcome].sum())
    
    apply_num = False
    if apply_num == True:
        cmap_key = 'bone'
        for i in range(i+1):
            for j in range(j+1):
                age_ax.annotate(f'{count[i,j]**2:.0f}',(j,i),color='orangered',rotation=90,ha='center',va='center')
    else:
        cmap_key = 'inferno'

    hm = age_ax.imshow(count, cmap=cmap_key, origin="lower", interpolation="nearest", aspect="auto")

    age_ax.set_yticks(range(i+1))
    age_ax.set_yticklabels(age_ranges)
    
    s=5
    age_ax.set_xticks(range(j+1)[::s])
    age_ax.set_xticklabels([d.left.date().strftime('%m-%d') for d in date_bins][::s])
    
    cb = age_fig.colorbar(hm)
    cb.ax.set_yticklabels(f'{x**2:.0f}' for x in list(cb.ax.get_yticks()))
    
    outcome_name = outcome.split()[0]
    age_fig.suptitle(f'Heatmap of OH COVID {outcome}\nBy Age Over Time',fontsize=14)
    age_fig.text(0,0.02,"Cases with 'Unknown' age range are excluded" +\
                 "\n'Onset Date' used for visualization" +\
                 "\nData as of 2020-07-14 from https://coronavirus.ohio.gov/static/COVIDSummaryData.csv" +\
                 "\nCreated by: Scott Schriner @schrinetime (Credit: Marc Bevand @zorinaq)")
           
    age_fig.tight_layout(rect=[0,.16,1,.9])
    age_fig.savefig(f'OH_COVID_{outcome_name}_heatmap_num{apply_num}.png')


