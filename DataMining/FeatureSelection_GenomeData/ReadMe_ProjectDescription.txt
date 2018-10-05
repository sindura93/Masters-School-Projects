Feature Selection of Genome Data:
Programming Language: Python 3.0
Tools used: Spyder, Anaconda
  This project is about choosing a particular set of observations from the Genome Data, which when classified gives the most meaningful information about the data. 
  The method I have followed to choose this set of observations, i.e., to perform feature selection is, calculating F-Score of all the observations and I have picked top 100 observations that has the highest f-scores. Then I have split these 100 observations into train and test sets to classify the data using different classification models such as, KNN, Centroid, SVM and Linear Regression.
  
 F-Score calculation was done from the scratch using numpy and pandas, with the formula:
 
  
  
