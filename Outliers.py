import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

pd.set_option('display.max_columns', None) #show all columns
pd.set_option('display.max_rows', None) #show all rows
pd.set_option('display.float_format', lambda x: '%.3f' % x) #show 3 digits after comma.
pd.set_option('display.width', 500)

def load():
    data = pd.read_csv(r"C:\Users\Asus\OneDrive\Masaüstü\titanic.csv")
    return data

df = load()
df.head()
df.columns

#Finding outliers using graphic method
sns.boxplot(x= df["Age"])
plt.show()

#Finding outliers with the Iqr method
df["Age"].mean()
q1 = df["Age"].quantile(0.25)
q3 = df["Age"].quantile(0.75)
iqr = q3 - q1
up = q3 + 1.5* iqr
low = q1 - 1.5 * iqr
df[(df["Age"]<low) | (df["Age"]>up)]
df[(df["Age"]<low) | (df["Age"]>up)].index

#Are there any outliers or not?
df[(df["Age"]<low) | (df["Age"]>up)].any(axis=None)
df[~((df["Age"]<low) | (df["Age"]>up))].any(axis=None)

#Functionalize Transactions
def outlier_thresholds(dataframe,  col_name, q1 = 0.25, q3 = 0.75): #Calculating the lower limit and upper limit.
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    iqr = quartile3 - quartile1
    up_limit = quartile3 + 1.5*iqr
    low_limit = quartile1 - 1.5*iqr
    dataframe[(dataframe[col_name]<low_limit) | (dataframe[col_name]>up_limit)]
    return low_limit, up_limit

outlier_thresholds(df,["Age"])
outlier_thresholds(df,["Fare"])

def check_outlier(dataframe,col_name): #Checking for outliers.
    low, up = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name]<low) | (dataframe[col_name]>up)].any(axis=None):
        return True
    else:
        return False

check_outlier(df,["Age"])

def grab_col_names(dataframe, cat_th =10, car_th = 20): #Detecting variable types.
    """
    Variable types.
     1. Categorical variable
     2. Numerical variable
     3. Categorical variable with numerical appearance
     4. Cardinal variable: A variable that has a categorical appearance, does not carry any information, and is very sparse.
    """
    #Categorical variables
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th
                   and dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th
                   and dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    #Numerical variables.
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat if "PassengerId" not in col]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols:{len(cat_cols)}")
    print(f"num_cols:{len(num_cols)}")
    print(f"cat_but_car:{len(cat_but_car)}")
    print(f"num_but_cat:{len(num_but_cat)}")
    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df) #The grab_col_names function is called and the returned values are assigned to the variables cat_cols, num_cols and cat_but_car. With this method, the outputs returned by the function can be used later.


def grab_outliers(dataframe, col_name, index =False): #Finding outliers and their indexes.
    low, up = outlier_thresholds(dataframe, col_name)
    if dataframe[((dataframe[col_name]<low) | (dataframe[col_name]>up))].shape[0] >10:
        print(dataframe[((dataframe[col_name]<low) | (dataframe[col_name]>up))].head())
    else:
        print(dataframe[((dataframe[col_name]<low) | (dataframe[col_name]>up))])
    if index:
        outlier_index = dataframe[((dataframe[col_name]<low) | (dataframe[col_name]>up))].index
        return outlier_index

grab_outliers(df, "Age")
grab_outliers(df,"Age", True)

#############################################
# Solving the Outlier Problem
#############################################

#1. Deleting outliers from the data set

def remove_outlier(dataframe, col_name): #Removes rows with outliers from the data set.
    low, up = outlier_thresholds(dataframe,col_name)
    df_without_outliers = dataframe[~((dataframe[col_name]<low) | (dataframe[col_name] > up))]
    return df_without_outliers

remove_outlier(df,"Age")

#Let's see how many rows remove_outlier deletes from the dataset.
for col in num_cols:
    new_df = remove_outlier(df,col)
df.shape[0] - new_df.shape[0]

#2. Suppression Method (re-assignment with thresholds)

def replace_with_thresholds(dataframe, variable): #Sets outliers equal to the lower and upper limits.
    low_limit, up_limit = outlier_thresholds(dataframe,variable)
    dataframe.loc[(dataframe[variable]<low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable]>up_limit), variable] = up_limit

#Let's use replace_with_thresholds for numeric columns.
for col in num_cols:
    replace_with_thresholds(df,col)

#Let's check if replace_with_thresholds is working.
for col in num_cols:
    print(col,check_outlier(df,col))
