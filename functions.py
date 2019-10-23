"""Functions for Stuart and Nicole's Mod1 project"""


def cleanbudgetdata(df):
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