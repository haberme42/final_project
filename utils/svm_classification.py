#!/usr/bin/env python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC,SVC, NuSVC
from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import pickle
import sys

# lambda function to load sets.
load_set = lambda path, desc : load_files(path, description=desc, shuffle=False, encoding="utf8",
                                          decode_error="ignore", random_state=42)


# The function fit pipe with optimal setting for the train set.
def fitPipe(train_set_path):
    # Load the train set.
    print("\nLoading the train set files.")
    train_set = load_set(train_set_path, "Train")

    # Set the pipe.
    pipe = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.85, ngram_range=(1, 2), use_idf=True)),
        ('clf', LinearSVC(C=10, loss='squared_hinge')),
    ])

    # Fit the pipe.
    print("Fitting the pipe.")
    pipe.fit(train_set.data, train_set.target)
    return pipe


# Load a pipe using pickle.
#   NOTE: the file should be in the main folder named 'pipe.pickle'.
def loadPipe():
    try:
        print("\nLoading the pipe from the pickle file.")
        return pickle.load(open("pipe.pickle", "rb"))
    except Exception as e:
        print("file missing. Please put the file in the main folder or check the name is 'pipe.pickle'.")
        sys.exit(0)


# The function search for the best setting pipe for the train set. The classification can be
#   "LinearSVC" or "SVC". the function can print all the results if needed and can save the
#   found pipe.
def searchFitPipe(train_set_path, classification="LinearSVC", show_results=False, save_pipe=False):
    print("\nLoading the train set files.")
    train_set = load_set(train_set_path, "Train")

    # Set the LinearSVC classification search.
    if classification == "LinearSVC":
        check_pipe = Pipeline([
            ('vect', TfidfVectorizer(min_df=3, max_df=0.85)),
            ('clf', LinearSVC()),
        ])
        param = {
            'vect__ngram_range': [(1, 1), (1, 2)],
            'vect__use_idf' : [True, False],
            'clf__C' : [10, 100, 1000],
            'clf__loss' : ['hinge', 'squared_hinge'],
        }

    # Set the SVC classification search.
    elif classification == "SVC":
        check_pipe = Pipeline([
            ('vect', TfidfVectorizer(min_df=3, max_df=0.85)),
            ('clf', SVC()),
        ])
        param = {
            'vect__ngram_range': [(1, 1), (1, 2)],
            'vect__use_idf' : [True, False],
            'clf__C' : [10, 100],
            'clf__kernel' : ['linear', 'poly', 'rbf', 'sigmoid'],
        }

    else:
        print("Pipe option not avilable. Please consult the documentation for available methods.")
        sys.exit(0)

    # Run the Search.
    print("Start serching best parameters for the pipe.")
    grid_search = GridSearchCV(check_pipe, param, cv=5, error_score=0, n_jobs=-1,
                               return_train_score=True, iid=False)
    grid_search.fit(train_set.data, train_set.target)
    print("Serching done")

    # Print the Best result and the rest if show_results - True.
    print(f"\nBest parameters for {classification} are: {grid_search.best_params_}\n")

    if show_results:
        print("The rest of the search results are:")

        for i in range(len(grid_search.cv_results_['params'])):
            print(f"{(1 + i):02d}) params: {grid_search.cv_results_['params'][i]}.")
            line = f"    mean train: {grid_search.cv_results_['mean_train_score'][i]:.2f}, "
            line += f"std train: {grid_search.cv_results_['std_train_score'][i]:.2f}, "
            line += f"mean test: {grid_search.cv_results_['mean_test_score'][i]:.2f}, "
            line += f"std test: {grid_search.cv_results_['std_test_score'][i]:.2f}, "
            line += f"rank test: {grid_search.cv_results_['rank_test_score'][i]:02d}.\n"
            print(line)

    # Set the pipe with the best result.
    if classification == "LinearSVC":
        pipe = Pipeline([
            ('vect', TfidfVectorizer(min_df=3,
                                     max_df=0.85,
                                     ngram_range=grid_search.best_params_["vect__ngram_range"],
                                     use_idf=grid_search.best_params_["vect__use_idf"])),
            ('clf', LinearSVC(C=grid_search.best_params_["clf__C"],
                              loss=grid_search.best_params_["clf__loss"])),
        ])

    else: # classification == "SVC"
        pipe = Pipeline([
            ('vect', TfidfVectorizer(min_df=3,
                                     max_df=0.85,
                                     ngram_range=grid_search.best_params_["vect__ngram_range"],
                                     use_idf=grid_search.best_params_["vect__use_idf"])),
            ('clf', SVC(C=grid_search.best_params_["clf__C"],
                        kernel=grid_search.best_params_["clf__kernel"])),
        ])

    # Fit the pipe.
    print("Fitting the pipe.")
    pipe.fit(train_set.data, train_set.target)

    # Save the pipe.
    if save_pipe:
        print("Saveing the pipe as 'pipe.pickle'.")
        pickle.dump(pipe, open("pipe.pickle", "wb"))

    return pipe


# the function take test set path and a pipe and run the pipe on the test set.
#   If print_report True the function print the classification report of the test set.
def runTest(test_set_path, pipe, print_report=False):
    # Load the test set.
    print("\nLoading the test set files.")
    test_set = load_set(test_set_path, "Test")

    # Run the pipe on the test set.
    predicted = pipe.predict(test_set.data)
    accuracy = 100 * np.mean(predicted == test_set.target)
    print(f"Test set accuracy: {accuracy:.2f}%")

    # Print the classification report
    if print_report:
        print(metrics.classification_report(test_set.target, predicted,
                                            target_names=test_set.target_names))
