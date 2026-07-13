#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By LB
# Read the output of the backward test and compare it to a previous version, if it exists
#
# After the test and Master branch update:
# To create a new reference version, you need to copy the bkw_test.txt to bkw_master.txt

import netCDF4 as nc
import numpy as np
import os

# Options:
return_flag = False
resolution = 0.01
compare = False

path1 = "./output_bkw/"
patheta = "./output_bkw_eta/"

# Comparing to previous version, if it exists
if os.path.isfile("./bkw_master.txt"):
    compare = True
    fr = open("./bkw_master.txt", "r")

with open("bkw_test.txt", "a") as f:
    # Read the output of the backward test
    with nc.Dataset(path1 + "grid_drydep_20090101030000.nc", "r") as ndata:
        # Get Concentrations
        temp = np.abs(ndata["spec001_mr"][:, :, 1, :, :, :])
        # Statistics
        mn_c = np.mean(temp)
        mx_c = np.max(temp)

    # Write to new output file
    f.write(" Dry:\t\tmean abs: %2.8e\tmax abs: %2.8e\n" % (mn_c, mx_c))

    # Compare to previous version
    if compare:
        tmp = fr.readline()
        tmp2 = tmp.split()
        mn_prev = float(tmp2[3])
        mx_prev = float(tmp2[6])
        diff_pr = np.abs(mn_c - mn_prev) / np.abs(mn_c) * 100.0
        if diff_pr > resolution:
            print(
                "WARNING: DRY deposition gives a different mean value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True
        diff_pr = np.abs(mx_c - mx_prev) / np.abs(mx_c) * 100.0
        if diff_pr > resolution:
            print(
                "WARNING: DRY deposition gives a different max value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True

    # Open the ETA version of the dry deposition output
    with nc.Dataset(patheta + "grid_drydep_20090101030000.nc", "r") as ndata:
        # Concentrations
        temp = np.abs(ndata["spec001_mr"][:, :, 1, :, :, :])
        mn_c = np.mean(temp)
        mx_c = np.max(temp)

    # Write to new output file
    f.write(" Dry ETA:\tmean abs: %2.8e\tmax abs: %2.8e\n" % (mn_c, mx_c))
    if compare:
        tmp = fr.readline()
        tmp2 = tmp.split()
        mn_prev = float(tmp2[4])
        mx_prev = float(tmp2[7])
        diff_pr = np.abs(mn_c - mn_prev) / np.abs(mn_c) * 100.0
        if diff_pr > resolution:
            print(
                "WARNING: DRY ETA deposition gives a different mean value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True
        diff_pr = np.abs(mx_c - mx_prev) / np.abs(mx_c) * 100.0
        if np.abs(mx_c - mx_prev) > (np.abs(mx_c) / resolution):
            print(
                "WARNING: DRY ETA deposition gives a different max value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True

    with nc.Dataset(path1 + "grid_wetdep_20090101030000.nc", "r") as ndata:
        # Concentrations
        temp = np.abs(ndata["spec001_mr"][:, :, 1, :, :, :])
        mn_c = np.mean(temp)
        mx_c = np.max(temp)

    # Write to new output file
    f.write(" Wet:\t\tmean abs: %2.8e\tmax abs: %2.8e\n" % (mn_c, mx_c))
    if compare:
        tmp = fr.readline()
        tmp2 = tmp.split()
        mn_prev = float(tmp2[3])
        mx_prev = float(tmp2[6])
        diff_pr = np.abs(mn_c - mn_prev) / np.abs(mn_c) * 100.0
        if diff_pr > resolution:
            print(
                "WARNING: WET deposition gives a different mean value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True
        diff_pr = np.abs(mx_c - mx_prev) / np.abs(mx_c) * 100.0
        if np.abs(mx_c - mx_prev) > (np.abs(mx_c) / resolution):
            print(
                "WARNING: WET deposition gives a different max value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True

    with nc.Dataset(patheta + "grid_wetdep_20090101030000.nc", "r") as ndata:
        # Concentrations
        temp = np.abs(ndata["spec001_mr"][:, :, 1, :, :, :])
        mn_c = np.mean(temp)
        mx_c = np.max(temp)

    # Write to new output file
    f.write(" Wet ETA:\tmean abs: %2.8e\tmax abs: %2.8e\n" % (mn_c, mx_c))
    if compare:
        tmp = fr.readline()
        tmp2 = tmp.split()
        mn_prev = float(tmp2[4])
        mx_prev = float(tmp2[7])
        diff_pr = np.abs(mn_c - mn_prev) / np.abs(mn_c) * 100.0
        if np.abs(mn_c - mn_prev) > (np.abs(mn_c) / resolution):
            print(
                "WARNING: WET ETA deposition gives a different mean value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True
        diff_pr = np.abs(mx_c - mx_prev) / np.abs(mx_c) * 100.0
        if np.abs(mx_c - mx_prev) > (np.abs(mx_c) / resolution):
            print(
                "WARNING: WET ETA deposition gives a different max value compared to the previous version."
            )
            print(diff_pr, "percent")
            return_flag = True

if return_flag:
    # This will cause the CI pipeline to fail, indicating that the new version deviates from the old one
    raise ValueError("Old and New version deviate")

elif compare:
    print(
        "Output from previous version is not significantly different from this version."
    )
