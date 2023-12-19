# Solving Outliers Problems

In this project, I addressed issues related to outliers using the Titanic dataset. First, we'll define the Titanic dataset with the def_load() function. After briefly reviewing this function, we'll examine outliers in this dataset using the box plot method. Then, we'll proceed to write the following functions in sequence:
### outlier_thresholds()
Computes the upper and lower bounds of outliers for the given column using the IQR (Interquartile Range) method.
### check_outlier()
Checks whether there are outliers in the specified column.
### grab_col_names()
Identifies numeric, categorical, and cardinal columns in the dataset. The numeric columns we find using this function will facilitate the use of the functions we write later.
### grab_outliers()
Finds outliers and returns their indices if present.

After writing these functions, we will attempt to address issues related to outliers using the following methods:
For the first method, which is the deletion method, we will use the remove_outlier() function. With this method, all rows containing outliers are removed from the dataset. However, if we do not want to remove all rows containing outliers, we will employ the second method, which is the clipping method. With this method, rows containing outlier values are set equal to threshold values. We will use the replace_with_thresholds() function for this method.


