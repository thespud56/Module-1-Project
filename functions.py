"""Functions for Stuart and Nicole's Mod1 project"""


def cleanbudgetdata(df):
    """Strips out $ signs, commas, and transforms strings into integers"""
    # Step 1. Strip out $ signs.
    df = df.applymap(lambda x: str(x).replace('$', ''))
    # Step 2. Strip away ','.
    df['worldwide_gross'] = df['worldwide_gross'].map(lambda x: str(x).replace(',', '_'))
    df['domestic_gross'] = df['domestic_gross'].map(lambda x: str(x).replace(',', '_'))
    df['production_budget'] = df['production_budget'].map(lambda x: str(x).replace(',', '_'))
    # Step 3. Transform string values into integers.
    df['worldwide_gross'] = df['worldwide_gross'].astype(int)
    df['domestic_gross'] = df['domestic_gross'].astype(int)
    df['production_budget'] = df['production_budget'].astype(int)
    return df    

def manipulatebudgetdata(df):
    """Creates ROI column"""
    # Create a new variable 'worldwide_roi' by calculating ROI.
    df['worldwide_roi'] = (df['worldwide_gross'] / df['production_budget']) *100
    # Sort dataframe by ROI, starting with highest ROI.
    df = df.sort_values('worldwide_roi', ascending=False)
    # There is one huge outlier that is in a category we can assume our client doesn't want to enter. Drop it.
    df = df.drop(5745, axis=0)
    # Reset our index, because we have removed an outlier and sorted our data.
    df = df.reset_index()
    df = df.drop('index', axis=1)
    return df

def createquint(df):
    """Creates quintiles based on ROI"""
    names = ['low', 'somewhat low', 'moderate', 'somewhat high', 'high']
    pd.qcut(df['worldwide_roi'], 5, labels=names)
    df['roi_category'] = pd.qcut(df['worldwide_roi'], 5, labels=names)
    return df

def executemerge(df1, df2):
    """Merges datasets and transforms for export"""
    df1['movie_year'] = df1['movie']+" (" + df1['release_date'].map(lambda x: x[-4: len(x)])+")"
    df2['movie_year'] = df2['primary_title']+" (" + df2['start_year'].astype(str)+")"
    df_new = df1.merge(df2, how='left', on='movie_year')
    df_new = df_new.loc[~df_new.isna().any(axis=1)]
    df_new.set_index("id", inplace=True)
    return df_new

def creatematrix(df):
    """Creates matrix of dummy variables from genres"""
    genreList = []
    for el in df['genres'].map(lambda x: str(x).split(",")):
        for el2 in el:
            genreList.append(el2)
    genreCols = set(genreList)
    genres = pd.DataFrame(columns = genreCols)
    blankMatrix = pd.concat([df, genres], axis = 1)
    for row_index, row in df.iterrows():
        for key, value in (dict(row)).items():
            if key == 'genres':
                for el in value.split(","):
                    df.loc[row_index, el] = 1
    for col, columnData in df.iteritems():
        if col in genreCols:
            df[col].fillna(0, inplace=True)
            df[col] = pd.to_numeric(df[col], downcast='integer')
    return df
    