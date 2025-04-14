import pandas as pd
import numpy as np
class univar():
    def quanqual(dataset):
        quan = []
        qual = []
        for columnName in dataset.columns:
            if dataset[columnName].dtype == 'O':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan,qual
    
    def univariate_table(dataset, quan):
        descriptive = pd.DataFrame(index = ["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%","99%", "Q4:100%", "IQR", "1.5Rule", "lesser", "greater", "min", "max","kurtosis", "skew", "Variance", "Std_deviation"], columns = quan)
        for colname in quan:
            descriptive[colname]["Mean"]= dataset[colname].mean()
            descriptive[colname]["Median"]= dataset[colname].median()
            descriptive[colname]["Mode"]= dataset[colname].mode()[0]
            descriptive[colname]["Q1:25%"] = dataset.describe()[colname]["25%"]
            descriptive[colname]["Q2:50%"] = dataset.describe()[colname]["50%"]
            descriptive[colname]["Q3:75%"] = dataset.describe()[colname]["75%"]
            descriptive[colname]["99%"] = np.percentile(dataset[colname],99)#it is not the describe table, so used np.percentile function
            descriptive[colname]["Q4:100%"] = dataset.describe()[colname]["max"]
            ##finding IQR and lesser and greater outlier range
            descriptive[colname]["IQR"] = descriptive[colname]["Q3:75%"] - descriptive[colname]["Q1:25%"] #IQR = Q3-Q1
            descriptive[colname]["1.5Rule"] = 1.5 * descriptive[colname]["IQR"] #1.5*IQR 
            descriptive[colname]["lesser"] = descriptive[colname]["Q1:25%"] - descriptive[colname]["1.5Rule"] # Q1 - 1.5*IQR
            descriptive[colname]["greater"] = descriptive[colname]["Q3:75%"] + descriptive[colname]["1.5Rule"] # Q3 + 1.5*IQR
            descriptive[colname]["min"] = dataset[colname].min()
            descriptive[colname]["max"] = dataset[colname].max()
            descriptive[colname]["kurtosis"] = dataset[colname].kurtosis()
            descriptive[colname]["skew"] = dataset[colname].skew()
            descriptive[colname]["Variance"] = dataset[colname].var()
            descriptive[colname]["Std_deviation"] = dataset[colname].std()
        return descriptive
    
    def find_outliers_columns(quan, descriptive):
        lesser_outliers =[]
        greater_outliers =[]
        for colname in quan:
            if (descriptive[colname]["min"] <  descriptive[colname]["lesser"]):
                lesser_outliers.append(colname)
            if (descriptive[colname]["max"] >  descriptive[colname]["greater"]):
                greater_outliers.append(colname)
        return lesser_outliers, greater_outliers
                
    def replace_outliers(dataset, descriptive, lesser_outliers, greater_outliers):
        for col in lesser_outliers:
            dataset[col][dataset[col] < descriptive[col]["lesser"]]= descriptive[col]["lesser"]

        for col in greater_outliers:
            dataset[col][dataset[col] > descriptive[col]["greater"]]= descriptive[col]["greater"]
            
    def freq_table(colname, dataset):
        frequency_table = pd.DataFrame(columns = ["Unique_Values", "Frequency", "Relative_Frequecy","CumSum"])
        frequency_table["Unique_Values"] = dataset[colname].value_counts().index
        frequency_table["Frequency"] = dataset[colname].value_counts().values
        frequency_table["Relative_Frequecy"] = frequency_table["Frequency"] / len(dataset[colname]) # len of data set is total number of rows
        frequency_table["CumSum"] = frequency_table["Relative_Frequecy"].cumsum()
        return frequency_table
    
    #write  a function for PDF since we don't have in built function
    def get_pdf_probability(dataset, start_range, end_range):
        from matplotlib import pyplot
        from scipy.stats import norm
        import seaborn as sns
        #plot the dataset in a histogram graph, kde is kernel and it is Green. Then the color for the curve is blue
        sns.distplot(dataset, kde=True, kde_kws={'color':'blue'}, color='Green')
        #plot verical line on the start range and end range in Red color
        #axvline means axis vertical line
        pyplot.axvline(start_range, color='Red')
        pyplot.axvline(end_range, color ='Red')
        #create a sample
        sample = dataset
        #find mean and standard deviation for sample
        mean = sample.mean()
        std_deviation = sample.std()
        #print the mean and standard deviation only with 3 digits decimall
        # % is a place holder
        #The tuple  contains the values to be inserted into the placeholders in the string. The first value () replaces the first , and the second value () replaces the second 
        #print("Mean=%.3f, Standard deviation=%.3f" % (mean, std_deviation))
        #simple approach is below with f string
        print(f"Mean={mean:.3f}, Standard deviation={std_deviation:.3f}")
        #define the distribution
        dist = norm(mean, std_deviation)
        #create a list of range (one line code)
        values = [value for value in range(start_range, end_range)]

        #sample probablity for a range of outcome
        #find probablity and store them in a list again
        probabilities  = [dist.pdf(value) for value in values]
        #Add all the probablities in the list for each value in range
        prob = sum(probabilities)

        print("The area between range({},{}):{}".format(start_range, end_range, prob))

        #simple approach to print with with f string is
        #print(f"The area between range({start_range},{end_range}):{prob}")

        return prob
        
        
    #write  a function for SND since we don't have in built function
    def stdNBgraph(dataset):
        """Converts normal disribution into standrd normal distribution"""
        import seaborn as sns
        mean = dataset.mean()
        std_deviation = dataset.std()

        #create a list that contains values of the input colum from dataset

        Values = [i for i in dataset]

        # find z_score value for each value in the above list value and store in a list "z_score"
        # formula for z_core = (x-μ)/σ 

        z_score = [(x-mean)/std_deviation for x in Values]

        # plot the z_score using seaborn library
        sns.distplot(z_score, kde=True, color="Green", kde_kws = {"color" : "blue"})

        #find average for z_score in the list "z_socre"
        print(f' The average z_score for salary is {sum(z_score) / len(z_score)}')