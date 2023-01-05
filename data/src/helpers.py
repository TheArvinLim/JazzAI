# HELPER
def clean_col_names(df):
    df.columns=df.columns.str.lower().str.replace(' ','_')
    return df