import pandas as pd
import numpy as np
from src.helpers import clean_col_names
from src.music_theory import add_note_number, get_interval_from_note_nums, MIDI_NOTE_TABLE, CHORD_TYPES, CHORD_TONES
import settings

# LOAD
def get_solo_metadata(conn):
    solo_metadata = pd.read_sql("SELECT * FROM solo_info", conn).merge(pd.read_sql("SELECT * FROM track_info", conn), on=["trackid", "recordid", "compid"], how="left")
    solo_metadata = solo_metadata.assign(key_center=solo_metadata['key'].str[:2].str.replace('\d+|-|j|m|s|\/|o|\+|NC', '', regex=True))
    solo_metadata = clean_col_names(solo_metadata)

    return solo_metadata

def get_solo_melody(conn):
    solo_melody = pd.read_sql("SELECT * FROM melody", conn).merge(MIDI_NOTE_TABLE.rename(columns={"midi_note": "pitch", "enharmonic_note": "melody_note"}), on="pitch", how="left")

    solo_melody = clean_col_names(solo_melody)


    return solo_melody

def get_solo_beats(conn):
    solo_beats = pd.read_sql("SELECT * FROM beats", conn)
    solo_beats["chord"] = solo_beats["chord"].replace(r'^\s*$', np.nan, regex=True).ffill()
    solo_beats["chord_root"] = solo_beats['chord'].str[:2].str.replace('\d+|-|j|m|s|\/|o|\+|NC', '', regex=True)
    solo_beats["chord_type"] = solo_beats.apply(lambda x: str(x["chord"])[len(str(x["chord_root"])):], 1)
    solo_beats = solo_beats.merge(CHORD_TYPES, on="chord_type", how="left")
    solo_beats = solo_beats.merge(CHORD_TONES, on="chord_type_base", how="left")

    solo_beats = clean_col_names(solo_beats)

    return solo_beats

def data_pipeline(solo_melody=get_solo_melody(settings.conn), 
                  solo_metadata=get_solo_metadata(settings.conn), 
                  solo_beats=get_solo_beats(settings.conn)):
    df = (
        solo_melody[["eventid", "melid", "onset", "pitch", "melody_note", "duration", "period", "division", "bar", "beat", "beatdur"]].
            merge(solo_metadata[["melid", "key", "key_center", "performer", "title"]], on="melid", how="left").
            merge(solo_beats[["melid", "chord", "chord_root", "chord_type", "chord_type_base", "chord_3rd", "chord_5th", "chord_7th", "bar", "beat"]], on=["melid",  "bar", "beat"], how="left").
            pipe(add_note_number, "key_center").
            pipe(add_note_number, "chord_root").
            pipe(add_note_number, "melody_note").
            pipe(get_interval_from_note_nums, "key_center_num", "melody_note_num", "key_center_melody_interval").
            pipe(get_interval_from_note_nums, "key_center_num", "chord_root_num", "key_chord_root_interval").
            pipe(get_interval_from_note_nums, "chord_root_num", "melody_note_num", "chord_root_melody_interval")
    )

    return df