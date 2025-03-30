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
        descriptive = pd.DataFrame(index = ["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%","99%", "Q4:100%", "IQR", "1.5Rule", "lesser", "greater", "min", "max"], columns = quan)
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
        