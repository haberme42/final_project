#!/usr/bin/env python
from utils import svm_classification as sc
from utils import data_handler as dh
from argparse import ArgumentParser
import sys


def main(parser):
    # build the train and test sets and get their pathes.
    train_set_path, test_set_path = dh.main(parser)

    # build the pipe and run it on the test set.
    if parser.pipe == "fit":
        pipe = sc.fitPipe(train_set_path)
    elif parser.pipe == "load":
        pipe = sc.loadPipe()
    else: # parser.pipe == "search":
        pipe = sc.searchFitPipe(train_set_path, parser.classification, parser.show_results,
                                parser.save_pipe)

    # Run the pipe on the test and print the result.
    sc.runTest(test_set_path, pipe, parser.print_report)

    # Delete the train and test folders.
    # dh.setFolderHandler(parser.set_path)


if __name__ == "__main__":
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
                        help="set the test-train divider.")
    parser.add_argument("--only_rambam",
                        action="store_true",
                        help="will use only the rambam for the train set.")
    parser.add_argument("--test_source",
                        type=str,
                        choices=["rambam", "ben", "kizur", "tur"],
                        default="rambam",
                        help="set the source for the test.")
    parser.add_argument("--classification",
                        type=str,
                        choices=["LinearSVC", "SVC"],
                        default="LinearSVC",
                        help="The type of classification that will be use. The classification can be LinearSVC or SVC.")
    parser.add_argument("--pipe",
                        type=str,
                        choices=["fit", "load", "search"],
                        default="fit",
                        help="Set the operation to set the pipe. fit - Fit a pipe with the recommenet value. load - Load a pickled pipe the pickle should be named 'pipe.pickle' and put in the main folder. search - Search for the best values for the train data.")
    parser.add_argument("--show_results",
                        action="store_true",
                        help="Show all the result of the search for the best arguments for the pipe. NOTE: used with search option.")
    parser.add_argument("--save_pipe",
                        action="store_true",
                        help="Save the fitted pipe. NOTE: used with search option.")
    parser.add_argument("--print_report",
                        action="store_true",
                        help="Print the classification report.")

    # Run the program itself with the parameters
    parser = parser.parse_args()

    # If the test set is the rambam the ratio need to divide it thus it cannot be 1
    #   as 1 put all the data in the train set.
    if (parser.test_source == "rambam") and (parser.train_ratio == 1.):
        print("The usage of the rambam as a test set can't have train ratio of 1")
        sys.exit(0)

    main(parser)
