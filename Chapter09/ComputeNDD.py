# Exercice 9.2 from Practical astronomy
#=======================================================================
#- Sylvie Dagoret-Campagne
#- affliliation : IJCLAB/IN2P3/CNRS
#- creation date : May 10th 2020
#https://www.astro.ubc.ca/people/jvw/ASTROSTATS/pracstats_web_ed1.html#chapter9
# 9.2 Variance of estimators for $w(\theta)$ (D). Generate 20,000 data points randomly in the region $0^o < \alpha < 5^o$, $0^o < \delta < 5^o$. Estimate $w(\theta)$ using the Natural estimator $w_1$, the Peebles estimator $w_2$, the Landy-Szalay estimator $w_3$ and the Hamilton estimator $w_4$. (Average $DR$ and $RR$ over say 10 comparison sets each of 20,000 random points). Plot the results as a function of $\delta$ showing Poisson error bars $1/\sqrt{DD}$. Comment on the results - which estimator is best?

import numpy as np
import pandas as pd

from astropy import units as u
from astropy.coordinates import Angle

import time
from datetime import datetime,date
import dateutil.parser

ra0=0
dec0=0

def distance(ra,dec):
    return np.sqrt((ra-ra0)**2+(dec-dec0)**2)

def dist_row(row):
    return distance(row["ra"],row["dec"])



if __name__ == '__main__':
    today = date.today()
    string_date=today.strftime("%Y-%m-%d")


    # data file
    file_data = "Ex9_2_data.xlsx"

    df = pd.read_excel(file_data, header=2)
    # right ascenssion in hours
    df1 = pd.concat([df["ra1"], df["ra2"], df["ra3"], df["ra4"], df["ra5"]], axis=0)
    # declination in degrees
    df2 = pd.concat([df["dec1"], df["dec2"], df["dec3"], df["dec4"], df["dec5"]], axis=0)

    # use Angle to convert into degrees
    myra = Angle(df1.values, unit="hour")

    df_data = pd.DataFrame()

    df_data["ra"] = myra.degree  # convert right ascenssion into degrees
    df_data["dec"] = df2.values  # keep declination into degrees

    Nobj = len(df_data)
    array_shape = df_data.shape


    # histogram config
    THETAS = np.arange(0, 10, 0.05)
    NBINS = len(THETAS) - 1
    BINSIZE = (THETAS[-1] - THETAS[0]) / NBINS

    BINSTART = THETAS[0]
    BINSTOP = THETAS[-1] + BINSIZE
    NBINS += 1

    # loop on each element in the original dataframe
    df0 = df_data.copy()
    for index, row in df_data.iterrows():

        # isolate the current element
        ra0 = row['ra']
        dec0 = row['dec']

        if index % 1000 == 0:
            print(index, " ra0=", ra0, " dec0=", dec0)

        df0.drop(index, inplace=True)  # erase one by one

        df0["dist"] = df0.apply(dist_row, axis=1)

        if index == 0:
            histo = np.histogram(df0["dist"].values, bins=NBINS, range=(BINSTART, BINSTOP))[0]
        else:
            histo += np.histogram(df0["dist"].values, bins=NBINS, range=(BINSTART, BINSTOP))[0]

    # save histo

    NDD=histo

    filename_histo = string_date + "_ndd.npy"
    np.save(filename_histo, NDD)



