import sqlite3 as sq

ENHARMONIC_NOTES_FILEPATH = "data/enharmonicNotes.csv"
SCALE_DEGREES_FILEPATH = "data/scaleDegrees.csv"
MIDI_NOTE_TABLE_FILEPATH = "data/midiNoteTable.csv"
CHORD_TYPES_FILEPATH = "data/chord_types.csv"
CHORD_TONES_FILEPATH = "data/chord_tones.csv"

conn = sq.connect("data/wjazzd.db")