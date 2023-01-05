# HELPER
def clean_col_names(df):
    df.columns=df.columns.str.lower().str.replace(' ','_')
    return df

def add_lag(df, column_name, lags):
    for lag in lags:
        if lag < 0:
            name = "lead"
        else:
            name = "lag"

        df[f'{column_name}_{name}_{abs(lag)}'] = df.groupby('melid')[column_name].shift(lag)
    return df