# UTILITY
import settings
import pandas as pd
import numpy as np

from src.helpers import clean_col_names

def read_table(filepath):
    table = pd.read_csv(filepath)
    table = clean_col_names(table)

    return table

MIDI_NOTE_TABLE = read_table(settings.MIDI_NOTE_TABLE_FILEPATH)
ENHARMONIC_NOTES = read_table(settings.ENHARMONIC_NOTES_FILEPATH)
SCALE_DEGREES = read_table(settings.SCALE_DEGREES_FILEPATH)
CHORD_TYPES = read_table(settings.CHORD_TYPES_FILEPATH)
CHORD_TONES = read_table(settings.CHORD_TONES_FILEPATH)

def add_enharmonic_notes(df, note_column_name):
    df = df.merge(ENHARMONIC_NOTES.rename(columns={"note": note_column_name, "enharmonic": f"enharmonic_{note_column_name}"}), on=note_column_name, how="left")

    return df

def add_note_number(df, note_column_name):
    semitone_mapper = MIDI_NOTE_TABLE.query("octave==1").copy()
    semitone_mapper["midi_note"] -= 23

    df = add_enharmonic_notes(df, note_column_name)

    df = df.merge(semitone_mapper[["midi_note", "enharmonic_note"]].rename(columns={"midi_note": f"{note_column_name}_num", "enharmonic_note": f"enharmonic_{note_column_name}"}), on=f"enharmonic_{note_column_name}", how="left")

    df = df.drop(labels=f"enharmonic_{note_column_name}", axis=1)

    return df


def get_interval_from_note_nums(df, note_1_col, note_2_col, interval_name, return_numeric=False):
    df["semitone_difference"] = df[note_2_col] - df[note_1_col]
    df = df.assign(semitone_difference = np.where(df["semitone_difference"] < 0, df["semitone_difference"] + 12, df["semitone_difference"]))

    if not return_numeric:
        df = (
            df.merge(SCALE_DEGREES[["semitones", "degree"]].rename(columns={"semitones": "semitone_difference", "degree": f"{interval_name}"}), on="semitone_difference", how="left")
        )

        df[f"{interval_name}"] = pd.Categorical(df[f"{interval_name}"], categories=['1', 'b2', '2', 'b3', '3', '4', '#4', '5', 'b6', '6', 'b7' ,'7'], ordered=True)

    else:
        df[f"{interval_name}"] = df["semitone_difference"]
    
    df = df.drop(labels="semitone_difference", axis=1)

    return df

def calculate_note_from_interval(df, note_col, interval_col, new_note_col_name='new_note'):
    df = df.pipe(add_note_number, note_col)
    df = df.merge(SCALE_DEGREES[["semitones", "degree"]].rename(columns={"semitones": "semitone_difference", "degree": f"{interval_col}"}), on=f'{interval_col}', how='left')
    df = df.assign(new_note_num = lambda x: x[f'{note_col}_num'] + x['semitone_difference'])
    df = df.merge(MIDI_NOTE_TABLE[["midi_note", "enharmonic_note"]].rename(columns={"midi_note": "new_note_num", "enharmonic_note": f"{new_note_col_name}"}).assign(new_note_num = lambda x: x.new_note_num.astype(float) - 23), on="new_note_num", how="left")
    df = df.drop(labels=[f'{note_col}_num', 'semitone_difference', 'new_note_num'], axis=1)

    return df
