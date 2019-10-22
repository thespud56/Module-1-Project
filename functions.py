"""Functions for Stuart and Nicole's Mod1 project"""

def creatematrix(df, col_name):
    """Fills in a matrix (columns appended to df) with boolean values \
    where column names match elements of list within target column"""
    for row_index, row in df.iterrows():
        for key, value in (dict(row)).items():
            if key == col_name:
                for el in value.split(","):
                    df.loc[row_index, el] = 1
    df.fillna(0, inplace=True)
    return df
