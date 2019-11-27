#!/usr/bin/env python
from argparse import ArgumentParser
from collections import defaultdict
from . import dataset_extractor as de
from random import shuffle
import glob
import sys
import os

RAMBAM_PATH = "Rambam/"
CHINUCH_PATH = "Chinuch/Chinuch.txt"
NODA_BIYHUDAH_PATH = "Noda_Biyhudah/Noda Biyhudah.txt"
BEN_ISH_HAI_PATH = "Ben-Ish Hai/"
KIZUR_SHULCHAN_ARUCH_PATH = "Kizur Shulchan Aruch/"
TUR_PATH = "Tur/"
REDUCED_TO_AMOUNT = 40

# The function take a path that the train and test sets will be put in and clean it.
#   if the initialize is True the function also ready the folder for building the sets.
def setFolderHandler(path, initialize=False):
    # Clean the folders in the path.
    try:
        if os.path.isdir(path):
            for set_folder in glob.glob(path + "/*"): # train_set folder and test_test folder.
                for label in glob.glob(set_folder + "/*"): # all the labels in each set folder.
                    for file in glob.glob(label + "/*"):
                        os.remove(file)
                    os.rmdir(label)
                os.rmdir(set_folder)
            os.rmdir(path)

    except Exception as e:
        print(f"The program can't delete the folder at {path}. Please delete it manually before rerunning the program.")
        sys.exit(0)

    # set the path and make the train and test sets folders.
    if initialize:
        train_set_path = path + "/train_set/"
        test_set_path = path + "/test_set/"

        os.mkdir(path)
        os.mkdir(train_set_path)
        os.mkdir(test_set_path)

        return train_set_path, test_set_path


# The function take all the labels at the train sets and make sure they exist in the
#   test set folder since the pipe need to get all the labels he was trained on. (Helps
#   if the test set don't contain all the labels)
def fillTestLabels(train_set_path, test_set_path):
    # Get the labels from the train set.
    for label in os.listdir(train_set_path):
        # Check the label exist in the test set otherwise it make a empty folder for the label.
        path = test_set_path + label
        if not os.path.isdir(path):
            os.mkdir(path)


# the function take a data set in the form of defaultdict(list) where the keys are the label,
#   a sorter (to sort the data to main and secondary set), and at least one set path to write
#   the data in. if the sorter divide the data into two sets a secondary path should be given.
#   The function then take sort and write the data set and essentially 'build' the sets.
#   NOTE: the function shuffle the data before dividing it unless no_shuffle set True.
def buildSet(data_set, data_sorter, main_path, secondary_path=None, no_shuffle=False):
    # The sub-function take path and data and write the data into files.
    #   The sub-function write the files as a continuation of the files already in the
    #   path as '#i.txt' where the 'i' is the following number starting with 0.
    def writeToPath(path, data):
        # Make the folder if it didn't exist.
        if not os.path.isdir(path):
            os.mkdir(path)

        # Get the current nuber of file to write.
        i = len(os.listdir(path))

        # Write the data to the path.
        for segment in data:
            file = open(f"{path}#{i}.txt", "w", encoding="utf8")
            file.write(segment)
            file.close()
            i += 1

    for label in data_set:
        # Shuffle and sort the data into sets.
        if not no_shuffle: shuffle(data_set[label])
        main, secondary = data_sorter(data_set[label])

        # Write the first set.
        main_label_path = f"{main_path}{label}/"
        writeToPath(main_label_path, main)

        # If the sorter create two sets, write the second set.
        if secondary:
            secondary_label_path = f"{secondary_path}{label}/"
            writeToPath(secondary_label_path, secondary)


# Create a sorter that divide the data into two sets based on the ratio (float).
#   NOTE: mainly used for train sets.
#   SPECIAL CASE USE: setting the ratio to 1 put all the data in the first set
def ratioBasedSorter(ratio):
    def data_sorter(data):
        return data[:int(len(data) * ratio)], data[int(len(data) * ratio):]

    return data_sorter


# Create a sorter that divide the data into two sets based on the amount (int).
#   NOTE: mainly used for test sets.
#   SPECIAL CASE USE: setting the amount to 0 put all the data in the first set
def amountBasedSorter(amount):
    def data_sorter(data):
        return data[amount:], data[:amount]

    return data_sorter


# Create a sorter that divide the data into two sets train and test based on the amount
#   (float). The function start by taking all data with the word "rambam" (in hebrew)
#   and put it in the train set with respect to the requested amount. If in the end
#   the amount was not filled it will be filled with data from the test set.
#   NOTE: mainly used for test sets.
def rambamSpecificSorter(amount):
    def data_sorter(data):
        segment_to_add = amount
        train = []
        test = []

        # Search for segment with the word "rambam" (in hebrew) and put them in the train.
        for segment in data:
            if (('רמב"ם' in segment) or ('רמבם' in segment)) and segment_to_add:
                segment_to_add -= 1
                train.append(segment)
            else:
                test.append(segment)

        # Add segment if the amount wasn't filled.
        if segment_to_add:
            train.extend(test[:segment_to_add])
            test = test[segment_to_add:]

        return test, train

    return data_sorter


# The function reduce the number of file in a set to.
def reduceSetFile(path, amount):
    # Since the files start from 0 and not 1.
    amount -= 1

    # Delete files greater then amount
    for folder in glob.glob(path + "/*"):
        for file in glob.glob(folder + "/*"):
            name = int(file.split('#')[1].split('.')[0])
            if name > amount:
                os.remove(file)


# The main function. If unsure use it as it can built all possible sets.
def main(parser):
    print("Clean the set path.")
    # Set the folders of the sets and get the pathes
    train_set_path, test_set_path = setFolderHandler(parser.set_path, True)

    print("Build the Rambam train set.")
    # Build the Rambam train set.
    sorter = ratioBasedSorter(parser.train_ratio)
    path = f"{parser.train_path}/{RAMBAM_PATH}"
    data_set = de.rambam_extractor(path)
    buildSet(data_set, sorter, train_set_path, test_set_path, parser.no_shuffle)

    # Build the other sources for the train.
    if not parser.only_rambam:
        print("Build the other train set.")
        # The Rambam file should be in relation to the rest so they need to be reduced.
        reduceSetFile(train_set_path, REDUCED_TO_AMOUNT)

        # All the data goes to the train.
        sorter = ratioBasedSorter(1.)

        # Build the Chinuch set into the train set.
        path = f"{parser.train_path}/{CHINUCH_PATH}"
        data_set = de.chinuch_extractor(path)
        buildSet(data_set, sorter, train_set_path, test_set_path, parser.no_shuffle)

        # Build the Noda Biyhudah set into the train set.
        path = f"{parser.train_path}/{NODA_BIYHUDAH_PATH}"
        data_set = de.noda_biyhudah_extractor(path)
        buildSet(data_set, sorter, train_set_path, test_set_path, parser.no_shuffle)

    print("Build the Rambam test set.")
    # If the test set is the Rambam it was alredy built with the sorter of the Rambam.
    if parser.test_source == "rambam":
        return train_set_path, test_set_path

    # Build the Ben Ish Hai set into the test set.
    elif parser.test_source == "ben":
        path = f"{parser.test_path}/{BEN_ISH_HAI_PATH}"
        data_set = de.ben_ish_hai_extractor(path)

    # Build the Kizur Shulchan Aruch set into the test set.
    elif parser.test_source == "kizur":
        path = f"{parser.test_path}/{KIZUR_SHULCHAN_ARUCH_PATH}"
        data_set = de.kizur_shulchan_aruch_extractor(path)

    # Build the Tur set into the test set.
    elif parser.test_source == "tur":
        path = f"{parser.test_path}/{TUR_PATH}"
        data_set = de.tur_extractor(path)

    # Set the sorter for the test.
    #   NOTE: choosing "amount" or "rambam" will build some of the test set into
    #   the train set.
    if parser.test_sorter == "full":
        sorter = amountBasedSorter(0)
    elif parser.test_sorter == "amount":
        sorter = amountBasedSorter(parser.test_amount)
    elif parser.test_sorter == "rambam":
        sorter = rambamSpecificSorter(parser.test_amount)

    buildSet(data_set, sorter, test_set_path, train_set_path)
    fillTestLabels(train_set_path, test_set_path)

    # Return the pathes of the train and test sets.
    return train_set_path, test_set_path


if __name__ == '__main__':
    parser = ArgumentParser(description="Rambam data handler")
    parser.add_argument("--train_path",
                        type=str,
                        default="./data/train_data/",
                        help="Set the path to the data that the classifier will use for training.")
    parser.add_argument("--test_path",
                        type=str,
                        default="./data/test_data/",
                        help="Set the path to the data that the classifier will be tested on.")
    parser.add_argument("--set_path",
                        type=str,
                        default="./data_set/",
                        help="Set the path that the program will use to storeage the data set. NOTE: will be deleted when finished.")
    parser.add_argument("--no_shuffle",
                        action="store_true",
                        help="The train sets Will NOT be shuffled. NOTE:if divided train to train-test it's best to use shuffle.")
    parser.add_argument("--train_ratio",
                        type=float,
                        choices=[x / 100 for x in range(50, 101)],
                        default=1.,
                        help="set the ratio for the train-test divider. NOTE: putting 1 will send all the files to the train set.")
    parser.add_argument("--test_amount",
                        type=int,
                        default=20,
                        help="set the amount for the test-train divider. NOTE: putting 0 will send all the files to the test set.")
    parser.add_argument("--test_sorter",
                        type=str,
                        choices=["full", "amount", "rambam"],
                        default="full",
                        help="set the test-train divider")
    parser.add_argument("--only_rambam",
                        action="store_true",
                        help="will use only the rambam for the train set")
    parser.add_argument("--test_source",
                        type=str,
                        choices=["rambam", "ben", "kizur", "tur"],
                        default="rambam",
                        help="set the source for the test.")

    # Run the program itself with the parameters
    parser = parser.parse_args()

    # If the test set is the rambam the ratio need to divide it thus it cannot be 1
    #   as 1 put all the data in the train set.
    if (parser.test_source == "rambam") and (parser.train_ratio == 1.):
        print("The usage of the rambam as a test set can't have train ratio of 1")
        sys.exit(0)

    main(parser)
