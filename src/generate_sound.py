from gensound import Triangle, Silence, WhiteNoise
import pandas as pd

# TODO: don't use for loops for this.
def generate_bassline_sounds(solo_bass_notes, bass_note_duration=0.1):
    bassline = {
        "duration": [],
        "note": []
    }

    current_time = 0
    for row in solo_bass_notes.iterrows():
        
        row = row[1]
        next_note_time = row['onset'] - current_time

        if next_note_time > 0:
            bassline['note'].append('r')
            bassline["duration"].append(next_note_time)

        bassline['note'].append(row['bass_note'] + str(int(row['octave'])))
        bassline["duration"].append(bass_note_duration)

        current_time = row['onset'] + bass_note_duration

    B = Silence(1e3)

    for i in range(len(bassline['duration'])):
        B = B | Triangle(bassline['note'][i], duration=bassline['duration'][i]*1e3)

    return B

def generate_snare_sounds(solo_bass_notes, snare_duration=0.1, snare_beats=[2, 4]):
    snare = {
        # "onset": [],
        "note": [],
        "duration": []
    }

    current_time = 0
    for row in solo_bass_notes.iterrows():
        
        row = row[1]
        next_note_time = row['onset'] - current_time

        if next_note_time > 0:
            snare['note'].append('r')
            # melody["onset"].append(current_time)
            snare["duration"].append(next_note_time)

        if row['beat'] in snare_beats:
            snare['note'].append("X")
        else:
            snare['note'].append("r")

        snare["duration"].append(snare_duration)

        current_time = row['onset'] + snare_duration

    D = Silence(1e3)

    for i in range(len(snare['duration'])):
        if snare['note'][i] == "X":
            D = D | WhiteNoise(duration=snare['duration'][i]*1e3)
        else:
            D = D | Silence(duration=snare['duration'][i]*1e3)

    return D

def generate_melody_sounds(solo_melody_notes, melody_note_col_name='melody_note'):
    melody = {
        "duration": [],
        "note": []
    }

    current_time = 0
    for row in solo_melody_notes.iterrows():   

        row = row[1]
        next_note_time = row['onset'] - current_time

        if next_note_time > 0:
            melody['note'].append('r')
            melody["duration"].append(next_note_time)


        melody['note'].append(str(row[melody_note_col_name]) + str(row['octave']))
        melody["duration"].append(row['duration'])

        current_time = row['onset'] + row['duration']
    S = Silence(1e3)

    for i in range(len(melody['duration'])):
        S = S | Triangle(melody['note'][i], duration=melody['duration'][i]*1e3)

    return S

def generate_solo_sounds(solo_bass_notes, solo_melody_notes, melody_note_col_name='melody_note', bass_note_duration=0.1, snare_duration=0.1, snare_beats=[2, 4]):
    B = generate_bassline_sounds(solo_bass_notes, bass_note_duration=bass_note_duration)
    D = generate_snare_sounds(solo_bass_notes, snare_duration=snare_duration, snare_beats=snare_beats)
    S = generate_melody_sounds(solo_melody_notes, melody_note_col_name=melody_note_col_name)

    W = S + B + D
    return W
