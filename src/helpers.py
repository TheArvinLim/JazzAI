# HELPER
def clean_col_names(df):
    df.columns=df.columns.str.lower().str.replace(' ','_')
    return df

def add_lag(df, column_name, lags, group_by_col='melid'):
    for lag in lags:
        if lag < 0:
            name = "lead"
        else:
            name = "lag"

        if group_by_col is not None:
            df[f'{column_name}_{name}_{abs(lag)}'] = df.groupby(group_by_col)[column_name].shift(lag)
        else:
            df[f'{column_name}_{name}_{abs(lag)}'] = df[column_name].shift(lag)

    return df