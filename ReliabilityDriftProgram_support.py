#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.21
#  in conjunction with Tcl version 8.6
#    Apr 25, 2019 01:32:38 AM +0800  platform: Windows NT
# We use Glob to work with files
import glob
import os
import re
import sys
from tempfile import TemporaryFile
from tkinter import filedialog
from tkinter.filedialog import askdirectory, askopenfilenames

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
from tqdm import tqdm

import tkinter as tk
import tkinter.ttk as ttk

global progress_var
progress_var = 0


def universal_load_csv(filepath):
    """
    This function reads .csv files for any test type.
    """
    with open(filepath) as f, TemporaryFile("w+") as t:
        # Clean the text file so that it can be parsed by the pandas .read_csv method
        for line in f:
            t.write(line.replace(" ", ""))
        t.seek(0)
        ln = len(line.strip().split(","))
        header = t.readline().strip().split(",")
        header += range(ln)
        # Read the temporary file into a dataframe
        df_raw = pd.read_csv(t, names=header)
        del t
        try:
            df_raw["LOT_ID"] = df_raw.at[11, "AMS_CSV_STANDARD_FORMAT"]
        except:
            df_raw["LOT_ID"] = "None"

        cols = df_raw.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        df_raw = df_raw[cols]

        try:
            idx = df_raw.index[
                df_raw["AMS_CSV_STANDARD_FORMAT"] == "PART_INDEX"
            ].tolist()
            df_new = df_raw.loc[idx[0] : :, "LOT_ID"::].reset_index()
            df_new.columns = df_new.iloc[1]
        except:
            df_new = df_raw.loc[0::, "LOT_ID"::].reset_index()
            df_new.columns = df_new.iloc[0]

        del df_raw

        df_new.columns = [
            "dropme",
            "LOT_ID",
            "PART_INDEX",
            "PART_X",
            "PART_Y",
            "PART_BIN",
            "SITE",
            "TOUCHDOWN_INDEX",
            "TIMESTAMP",
        ] + df_new.columns.tolist()[9:]
        df_new = (
            df_new.drop("dropme", axis=1)
            .drop([0, 1, 2, 3, 4, 5, 6])
            .reset_index()
            .drop("index", axis=1)
        )
        df_new = df_new[df_new.columns.dropna()]
        try:
            df_new["TIMESTAMP"] = pd.to_datetime(
                df_new["TIMESTAMP"], format="%d.%m.%Y%H:%M:%S"
            )
        except:
            df_new["TIMESTAMP"] = pd.to_datetime(
                df_new["TIMESTAMP"], format="%d.%m.%Y %H:%M:%S"
            )
        df_new.iloc[:, 8:] = df_new.iloc[:, 8:].astype(float)

        return df_new


# Convert dataframe into multi-indexed dataframe with cycle number as main index
def makemulti(frame, cyclenum):
    frame["Hours"] = cyclenum
    newframe = frame.set_index(["Hours"])
    return newframe


# Read cyclenum from filename
def cycle(filename):
    try:
        # Searches for HXXXX, CXXXX, XXXXC or XXXXH in the filename where XXXX is the cycle time number
        m = re.search(r"(\d{1,}).?[CHX]|[CHX].?(\d{1,})", filename, flags=re.IGNORECASE)
        numcycle = int(m.group(1))
    except:
        numcycle = 0
    return numcycle


# Read SNx from filename
def serial_number(filename):
    # Each actual SN number corresponds to a 'PART_X' and 'PART_Y' coordinate
    # We use this dictionary for the conversion
    convertdict = {
        1: [0, 0],
        2: [1, 0],
        3: [2, 0],
        4: [3, 0],
        5: [4, 0],
        6: [4, -1],
        7: [3, -1],
        8: [2, -1],
        9: [1, -1],
        10: [0, -1],
        11: [0, -2],
        12: [1, -2],
        13: [2, -2],
        14: [3, -2],
        15: [4, -2],
        16: [4, -3],
        17: [3, -3],
        18: [2, -3],
        19: [1, -3],
        20: [0, -3],
        21: [0, -4],
        22: [1, -4],
        23: [2, -4],
        24: [3, -4],
        25: [4, -4],
        26: [4, -5],
        27: [3, -5],
        28: [2, -5],
        29: [1, -5],
        30: [0, -5],
    }
    try:
        # We use regex search to obtain SN number
        m = re.search(r"SN(\d{1,2})", filename, flags=re.IGNORECASE)
        snx = int(m.group(1))
        index_xy = convertdict.get(snx)
        return index_xy
    except:
        return None


# Read Stress Type from filepath
def stress_type(filename):
    # We use regex search to obtain SN number
    m = re.search("(HTOL)|(HTSL)|(THB)|(TC)|(TH)", filename, flags=re.IGNORECASE)
    stress = str(m.group(1))
    return stress


def findtesttype(filename):
    """
    This function tries to find the test type of the file by looking through the filename for 'FFT', 'NFT' or 'LIV'. 
    Case is ignored in this search (ie. uppercase vs lowercase). 
    If a match cannot be found, the test type is taken to be 'Unknown' and will generate an error later on.
    """
    try:
        # Search for the words FFT, NFT or LIV in the filename in order to guess which test type it belongs to
        m = re.search("(FFT|NFT|LIV)", filename, flags=re.IGNORECASE)
        testtype = str(m.group(1).upper())
    except:
        testtype = "Unknown"
    return testtype


def combinecsv(listoffiles):
    """
    This function takes a list of files and combines them into a single dataframe,
    using universal_load_csv() to parse the files into dataframes,
    makemulti() to combine the dataframes with cycle() to identify 
    the hours for each of the files.
    """
    for file in listoffiles:
        if file == listoffiles[0]:
            main_df = makemulti(universal_load_csv(file), cycle(file))
        else:
            new_df = makemulti(universal_load_csv(file), cycle(file))
            main_df = main_df.append(new_df, sort=False)
            # main_df = main_df.sort_index(by=['TIMESTAMP'])
    return main_df


def plotMPIdata(test_dataframe):
    """
    Takes a test type (LIV, NFT or FFT) and a dataframe and creates an interactive grouped box plot via local host which
    opens in the user's default browser.

    The labels that the plots are grouped-by are taken from the dataframe headers fed into the plot function.
    """

    # Labels for plotting
    label_raw = test_dataframe.columns.values.tolist()
    testlabels = label_raw[9:]

    # Generate dictlist for data
    dict_list_data = []

    def dict_generator_data(label):
        new_dict = dict(
            type="box",
            y=test_dataframe[label],
            name="{}".format(label),
            transforms=[dict(type="groupby", groups=test_dataframe["Hours"])],
        )
        return new_dict

    for label in testlabels:
        dict_list_data.append(dict_generator_data(label))

    # Generate dictlist for the updatemenus
    dict_list_menu = []

    def dict_generator_menu(label, label_list):
        label_index = label_list.index(label)
        temporary_list = [False] * (len(label_list))
        temporary_list[label_index] = True
        plotname = "{:02d}_".format(label_index + 1) + label
        new_dict = dict(
            label=plotname, method="update", args=[{"visible": temporary_list}]
        )
        return new_dict

    for label in testlabels:
        dict_list_menu.append(dict_generator_menu(label, testlabels))

    # Put dictionary objects into the data construct
    data = dict_list_data

    # Put dictionary objects into the dropdownlist
    updatemenus = list(
        [
            dict(
                active=-1,
                buttons=dict_list_menu,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.1,
                yanchor="bottom",
            )
        ]
    )

    fig = dict({"data": data}, layout=dict(updatemenus=updatemenus))

    plotly.offline.plot(fig, validate=False)


def saveMPIdata_universal(test_dataframe, save_location, flyers=True):
    """
    This function plots boxplots with matplotlib and saves them in a specified save_location.
    """
    # Extract parameters from dataframe

    label_raw = test_dataframe.columns.values.tolist()
    testlabels = label_raw[9:]

    def series_values_as_dict(series_object):
        tmp = series_object.to_dict().values()
        return [y for y in tmp][0]

    def add_values(bp, ax):
        fontsize = 12
        fontspacing = 0.27  # 0.27

        """ This actually adds the numbers to the various points of the boxplots"""
        for element in ["whiskers", "medians", "caps"]:
            for line in bp[element]:
                # Get the position of the element. y is the label you want
                (x_l, y), (x_r, _) = line.get_xydata()
                # Make sure datapoints exist
                if not np.isnan(y):
                    x_line_center = x_l + (x_r - x_l) / 2
                    y_line_center = y

                    if y >= 100:
                        numformat = "%.1f"
                    elif y >= 1000:
                        numformat = "%.0f"
                    else:
                        numformat = "%.3f"
                    # overlay the value:  on the line, from center to right

                    if element == "medians":
                        ax.text(
                            x_line_center + fontspacing,
                            y_line_center,  # Position
                            numformat % y,  # Value (3f = 3 decimal float)
                            verticalalignment="center",  # Centered vertically with line
                            color="green",  # Value for median will be green
                            fontsize=fontsize,
                        )

                    elif element == "whiskers":
                        ax.text(
                            x_line_center + fontspacing,
                            y_line_center,  # Position
                            numformat % y,  # Value (3f = 3 decimal float)
                            verticalalignment="center",  # Centered vertically with line
                            color="tab:blue",  # Value for whiskers will be tableau blue
                            fontsize=fontsize,
                        )
                    else:
                        ax.text(
                            x_line_center + fontspacing,
                            y_line_center,  # Position
                            numformat % y,  # Value (3f = 3 decimal float)
                            verticalalignment="center",  # Centered vertically with line
                            fontsize=fontsize,
                        )

        fryers = bp[
            "fliers"
        ]  # Fliers are the 'outliers'. We want the values for these too!
        # Iterate over it!
        if flyers == True:
            for fly in fryers:
                fdata = fly.get_xydata()
                if fdata.any() == False:
                    pass
                else:
                    for btuple in fdata:
                        x, y = btuple
                        if not np.isnan(y):
                            # Settings the appearance of the outliers and its value
                            fly.set(
                                marker="o",
                                markerfacecolor="tab:orange",
                                markeredgecolor="tab:orange",
                            )
                            ax.text(
                                x - 0.3,
                                y,
                                numformat % y,
                                verticalalignment="center",
                                horizontalalignment="left",
                                color="tab:orange",
                                fontsize=fontsize,
                            )

    # Iterate through the test parameters and save a boxplot grouped by cycle time for each
    for label in testlabels:
        fig, axes = plt.subplots(1, figsize=(16, 10))
        boxplot = test_dataframe.boxplot(
            column=[label],
            by=["Hours"],
            grid=True,
            figsize=(12, 8),
            ax=axes,
            return_type="dict",
        )
        bp_dict = series_values_as_dict(boxplot)
        add_values(bp_dict, axes)
        plt.title("")
        plt.xlabel("Hours", fontsize=16)
        plt.ylabel(label, fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        # Save the boxplots in save_location
        plt.savefig(save_location + label + "_boxplot.png", transparent=True)
        plt.close()


# default_open_location = r"\\fstpdata\Team\Quality\Reliability\"


def build_database():
    """
    Invoked by the 'Compile Files to Database' button in the GUI.
    Takes a list of files for a single RTO and filters them based on the 
    appearance of the stress_test keywords 'HTOL, THB, TH, TC, HTSL' 
    followed by the measurement_type keywords 'NFT, LIV, FFT'.
    
    If there are any files that are singular SN measurements, these measurement
    values will be replace any older measurements made (based on measurement time/date)
    If any files are excel files, sheets with sheet names from 0 - 1000 will be
    processed into the dataset with empty sheets being ignored.

    Data is saved in .csv files stored in the same folder with the following directory structure:
    '[relative path] > [RTO Number] > [Stress_Test] > RTO-number_MeasurementType_Data.csv'.
    An example of this directory structure would be 
    'C:/Datalogs/RTO-4149/HTSL/RTO-4149_NFT_Data.csv'
    """
    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select an RTO folder"
    )

    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    # We create a separate list for each test type + stress type pair as we will save
    for stress_type in ("HTOL", "THB", "TH", "TC", "HTSL"):
        for measurement_type in ("FFT", "LIV", "NFT"):
            list_of_files = glob.glob(
                folderpath + "/{}/**/*{}.csv".format(stress_type, measurement_type),
                recursive=True,
            )
            # Determine RTO number of the folder

            if len(list_of_files) == 0:
                print(
                    "Folder for Stress: {} + Test: {} not found".format(
                        stress_type, measurement_type
                    )
                )
                pass

            else:
                m = re.search(r"RTO.(\d{1,})", list_of_files[0], flags=re.IGNORECASE)
                rto_num = str(m.group(1))

                # Define the location to save the files to
                savepath = folderpath + "/{}/RTO-{}_{}_Database.csv".format(
                    stress_type, rto_num, measurement_type
                )
                try:
                    main_df = combinecsv(list_of_files)
                    main_df.dropna(subset=["PART_INDEX"], inplace=True)
                    main_df.to_csv(savepath)
                except:
                    print("fail")

    print("RTO Database Build Completed")


def read_database(filepath):
    """
    Reads a database of the file format RTO-XXXX_[TestType]_Database.csv generated by build_database().
    """
    df = pd.read_csv(filepath)
    return df


def generate_drift_statistics(dataframe, savelocation):
    """    
    Calculates the following drift statistics: Average Drift, Absolute Average Drift, Maximum Absolute Drift
    and Mininum Absolute Drift.
    """

    # Labels for calculation
    dataframe.sort_values(by=["TIMESTAMP"], inplace=True)
    label_raw = dataframe.columns.values.tolist()
    labels = label_raw[9:]

    s = dataframe.PART_INDEX.unique()
    s = np.append(s, ["Min", "Max", "Mean", "Std"])

    #     raw_drift_template = pd.DataFrame(s, columns=['PART_INDEX'])
    #     abs_drift_template = pd.DataFrame(s, columns=['PART_INDEX'])
    hour_range = dataframe.Hours.unique().tolist()
    cols = ["PART_INDEX"]
    cols.extend(hour_range)
    print("Cycles Detected: ", cols[1:])
    dataframe.set_index(["Hours", "PART_INDEX"], inplace=True)

    # Create empty dictionaries to house Dataframes for Raw Drift and Absolute Drift
    dict_of_raw_drift = {}
    dict_of_abs_drift = {}

    #     hour_range = dataframe.index.get_level_values('Hours').unique().tolist()
    #     print(hour_range)

    with pd.ExcelWriter(savelocation + "RawDrift.xlsx") as rawwriter, pd.ExcelWriter(
        savelocation + "AbsoluteDrift.xlsx"
    ) as abswriter:
        for label in labels:
            baseline = dataframe[label][0]
            dict_of_raw_drift["{}".format(label)] = pd.DataFrame(
                s, columns=["PART_INDEX"]
            )
            dict_of_abs_drift["{}".format(label)] = pd.DataFrame(
                s, columns=["PART_INDEX"]
            )

            for hour in hour_range[1:]:
                # Calculate Raw Drift values
                curr_value = dataframe[label][hour]
                raw_drift = ((curr_value - baseline) / baseline) * 100
                # Calculate Raw Drift Summary statistics
                describe_raw_drift = pd.Series(
                    data=[
                        raw_drift.min(),
                        raw_drift.max(),
                        raw_drift.mean(),
                        raw_drift.std(),
                    ],
                    index=["Min", "Max", "Mean", "Std"],
                ) 
                all_raw_drift = raw_drift.append(describe_raw_drift) # Append Summary Statistics to Raw Values
                dict_of_raw_drift["{}".format(label)][hour] = all_raw_drift.values # Add values to Dataframe in Dictionary
                
                abs_drift = abs(raw_drift) # Calculate Absolute Drift Values
                #Calculate Abs Drift Summary Statistics
                describe_abs_drift = pd.Series( 
                    data=[
                        abs_drift.min(),
                        abs_drift.max(),
                        abs_drift.mean(),
                        abs_drift.std(),
                    ],
                    index=["Min", "Max", "Mean", "Std"],
                )
                all_abs_drift = abs_drift.apyippend(describe_abs_drift) # Append Summary Statistics to Absolute Values
                dict_of_abs_drift["{}".format(label)][hour] = all_abs_drift.values # Add values to Dataframe in Dictionary
            
            # Stack Dataframes in excelwriter objects
            dict_of_raw_drift["{}".format(label)].to_excel(rawwriter, sheet_name=label[:30], index = False) 
            dict_of_abs_drift["{}".format(label)].to_excel(abswriter, sheet_name=label[:30], index = False)
        # Save excelwriter objects to Excel Files with each Excel Sheet generated from one Dataframe
        rawwriter.save()
        abswriter.save()
    print("Drift Calculation Completed")


def drift_calculation():
    """
    Invoked by the 'Compute Drift' button in the GUI.
    Reads a database .csv file generated using build_database() 
    for a single Reliability Test Order and calculates drift statistics
    using generate_drift_statistics()

    After calculation, a save prompt is invoked. Saves drift statistics as an excel file.
    """
    stringoffiles = askopenfilenames(
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    # This prevents the program from hanging if the task is cancelled
    if stringoffiles == "":
        return root.update()

    listoffiles = root.tk.splitlist(stringoffiles)
    for file in listoffiles:
        # try:
        m = re.search(r"RTO.(\d{1,})", file, flags=re.IGNORECASE)
        rto_num = str(m.group(1))
        measurement_type = findtesttype(file)
        savepath = (
            os.path.dirname(file)
            + "/Drift Calculation/"
            + "RTO-{}_{}_".format(rto_num, measurement_type)
        )

        if not os.path.exists(os.path.dirname(file) + "/Drift Calculation/"):
            os.makedirs(os.path.dirname(file) + "/Drift Calculation/")

        print("Saving calculations to: ", os.path.dirname(file) + "/Drift Calculation/")

        main_df = pd.read_csv(file)

        generate_drift_statistics(main_df, savepath)

    # except:
    #     print('calc failed')

    sys.stdout.flush()


def file_plot_interactive():
    """
    Invoked by the 'Select Files to Plot (interactive)' button in the GUI.
    Reads a database .csv file generated using build_database() 
    for a single Reliability Test Order. 
    
    Generates an interactive plot
    with plotly and serves it via localhost. Automatically opens in
    default browser
    """
    stringoffiles = askopenfilenames(
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    # This prevents the program from hanging if the task is cancelled
    if stringoffiles == "":
        return root.update()

    print(stringoffiles)
    listoffiles = root.tk.splitlist(stringoffiles)
    for i in listoffiles:
        # try:
        main_df = pd.read_csv(i)
        plotMPIdata(main_df)
        # except:
        #     print('interactive plot failed')

    sys.stdout.flush()


def folder_save_img():
    """
    Invoked by the "Plot All Files in Folder" button in the GUI.
    Reads multiple database .csv files of the format generated by 
    the build_database() function. Groups files by identifying
    folder structure. Groups first by RTO number, 
    followed by stress test type 'HTOL, THB, TH, TC, HSTL' 
    and finally by measurement type 'NFT, LIV, FFT'.

    Saves files in the second lowest folder ie.
    '[relative path] > [RTO Number] > [Stress_Test_Plot] > [Measurement_Type Plot Folder]'
    An example of this directory structure would be 
    'C:/Datalogs/RTO-4149/HTSL/NFT_boxplot'
    """
    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select a directory"
    )

    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    for stress_type in tqdm(("HTOL", "THB", "TH", "TC", "HTSL")):
        for measurement_type in tqdm(("FFT", "LIV", "NFT")):
            # We create a separate list for each test type as we will plot them separately
            # Determine RTO number of the folder
            database_files = glob.glob(
                folderpath
                + "/{}/*_{}_Database.csv".format(stress_type, measurement_type),
                recursive=True,
            )

            listlen = len(database_files)

            if listlen == 0:
                tqdm.write(
                    "Stress: {} and Test: {} not found".format(
                        stress_type, measurement_type
                    )
                )
                pass

            else:
                # database_files = glob.glob(folderpath+'/**/*Database.csv', recursive=True)
                pbar = tqdm(total=listlen)
                for file in database_files:
                    # try:
                    # main_df = combinecsv(listoffiles)
                    # plotMPIdata(read_test_type, main_df)
                    main_df = pd.read_csv(file)
                    # print(main_df.head())

                    save_location = folderpath + "/{}/{}_boxplot/".format(
                        stress_type, measurement_type
                    )
                    if not os.path.exists(save_location):
                        os.makedirs(save_location)

                    # main_df = main_df.dropna(axis='columns')
                    # main_df.to_csv(save_location+'{}hey4.csv'.format(findtesttype(listoffiles[0])))

                    saveMPIdata_universal(main_df, save_location)
                    del main_df  # Garbage Collect main_df to free up memory
                    pbar.update(1)
                    # except:
                    #     print('something went wrong')
                pbar.close()
    tqdm.write("Complete")
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == "__main__":
    import ReliabilityDriftProgram

    ReliabilityDriftProgram.vp_start_gui()
