from src.music_theory import get_interval_from_note_nums
from src.helpers import add_lag

def create_feature_matrix(joined, melody_note_lags=range(1,2), chord_root_lags=range(-1,-2,-1), chord_type_lags=range(-1,-2,-1), group_by_col='melid'):
    cols = ["chord_3rd", "chord_5th", "chord_7th", "chord_root_num", "melody_note_num"]
    if group_by_col is not None:
        cols = cols + [group_by_col]

    note_sequence_df = (
        joined[cols].copy()
        .pipe(add_lag, "melody_note_num", melody_note_lags, group_by_col)
        .pipe(add_lag, "chord_root_num", chord_root_lags, group_by_col)
        .pipe(add_lag, "chord_3rd", chord_type_lags, group_by_col)
        .pipe(add_lag, "chord_5th", chord_type_lags, group_by_col)
        .pipe(add_lag, "chord_7th", chord_type_lags, group_by_col)
    )

    lead_lag_cols = [col for col in note_sequence_df.columns if 'melody_note_num' in col or 'chord_root_num_lead' in col]

    for col in lead_lag_cols:
        note_sequence_df = get_interval_from_note_nums(note_sequence_df, 'chord_root_num', col, f"chord_root_{col.replace('_num', '')}_interval", return_numeric=False)
    
    drop_cols = lead_lag_cols + ['chord_root_num']
    if group_by_col is not None:
        drop_cols = drop_cols + [group_by_col]

    note_sequence_df = note_sequence_df.drop(drop_cols, axis=1)

    # pipe(get_interval_from_note_nums, 'chord_root_num', 'melody_note_num', 'chord_melody_interval').
    # pipe(get_interval_from_note_nums, 'chord_root_num', 'melody_note_num_lag_1', 'chord_melody_lag_1_interval').
    # pipe(get_interval_from_note_nums, 'chord_root_num', 'chord_root_num_lead_1', 'chord_root_lead_1_interval').
    # drop(["chord_root_num", "chord_root_num_lead_1", "melody_note_num", "melody_note_num_lag_1"], axis=1)
    
    note_sequence_df = note_sequence_df.dropna(axis=0)

    for col in note_sequence_df.columns:
        if note_sequence_df[col].dtype.name == 'category':
            note_sequence_df[col] = note_sequence_df[col].astype(str)


    return note_sequence_df