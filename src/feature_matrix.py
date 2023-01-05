from src.music_theory import get_interval_from_note_nums
from src.helpers import add_lag

def create_feature_matrix(joined):
    note_sequence_df = (
        joined[["melid", "chord_3rd", "chord_5th", "chord_7th", "chord_root_num", "melody_note_num"]].copy().
        pipe(add_lag, "melody_note_num", range(1, 2)).
        pipe(add_lag, "chord_root_num", range(-1, -2, -1)).
        pipe(add_lag, "chord_3rd", range(-1, -2, -1)).
        pipe(add_lag, "chord_5th", range(-1, -2, -1)).
        pipe(add_lag, "chord_7th", range(-1, -2, -1)).
        pipe(get_interval_from_note_nums, 'chord_root_num', 'melody_note_num', 'chord_melody_interval').
        pipe(get_interval_from_note_nums, 'chord_root_num', 'melody_note_num_lag_1', 'chord_melody_lag_1_interval').
        pipe(get_interval_from_note_nums, 'chord_root_num', 'chord_root_num_lead_1', 'chord_root_lead_1_interval').
        drop(["chord_root_num", "chord_root_num_lead_1", "melody_note_num", "melody_note_num_lag_1"], axis=1)
    )

    return note_sequence_df