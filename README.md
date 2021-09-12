# Final Project
## Rambam classifier

A research project deteined to create general classifier that can calssify Shutim to Halachot from the Rambam.
For more information, see דו"ח סופי.pdf


## Dependencies
* argparse==v.1.1
* sklearn==v.0.20.1
* numpy==v.1.15.4


## User guide
To use the program first put the train and test set in their respective folder. you can also specify the location for the train and test set as well as the folder the program will use when building the set for the classifier. The program then build the sets, train and test the set for the optimal parameters. To load a pipe put the pipe in the main folder and use the appropriate flag. For more information, see ספר משתמש.pdf


### Additional flags
Flag | Default | Choices | Description
--- | --- | --- | ---
--train_path | ./data/train_data/ | - | Set the path to the data that the classifier will use for training.
--test_path | ./data/test_data/ | - | Set the path to the data that the classifier will be tested on.
--set_path | ./data_set/ | - | Set the path that the program will use to storeage the data set. NOTE: will be deleted when finished.
--no_shuffle | FALSE | TRUE, FALSE | The train sets Will NOT be shuffled. NOTE:if divided train to train-test it's best to use shuffle.
--train_ratio | 1.0 | 1.0 to 0.5 | set the ratio for the train-test divider. NOTE: putting 1 will send all the files to the train set.
--test_amount | 20 | any | set the amount for the test-train divider. NOTE: putting 0 will send all the files to the test set.
--only_rambam | FALSE | TRUE, FALSE | will use only the rambam for the train set.
--test_sorter | fit | full, amount, rambam | set the test-train divider.
--test_source | rambam | rambam, ben, kizur, tur | set the source for the test.
--classification | LinearSVC | LinearSVC, SVC | The type of classification that will be use. The classification can be LinearSVC or SVC.
--pipe | fit | fit, load, search | Set the operation to set the pipe. fit - Fit a pipe with the recommenet value. load - Load a pickled pipe the pickle should be named 'pipe.pickle' and put in the main folder. search - Search for the best values for the train data.
--show_results | FALSE | TRUE, FALSE | Show all the result of the search for the best arguments for the pipe. NOTE: used with search option.
--save_pipe | FALSE | TRUE, FALSE | Save the fitted pipe. NOTE: used with search option.
--print_report | FALSE | TRUE, FALSE | Print the classification report.


## Sources
* Rambam               - https://www.mechon-mamre.org/i/0.htm
* Chinuch              - http://www.daat.ac.il/daat/mitsvot/sefer.asp?sefer=1
* Noda_Biyhudah        - https://www.sefaria.org.il/Noda_BiYhudah_I?lang=he
* Ben-Ish Hai          - http://www.daat.ac.il/daat/vl/tohen.asp?id=771
* Kizur Shulchan Aruch - http://www.daat.ac.il/daat/vl/tohen.asp?id=670
* Tur                  - http://www.daat.ac.il/daat/vl/tohen.asp?id=770
