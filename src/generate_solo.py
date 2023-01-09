import numpy as np
import pandas as pd
from src.music_theory import calculate_note_from_interval

def one_step_predict(struct_instance, notes_instance, clf):

    one_step_instance = pd.concat([struct_instance.reset_index(drop=True), notes_instance.reset_index(drop=True)], axis=1)
    one_step_instance = pd.get_dummies(one_step_instance)

    diff = set(clf.feature_names_in_).difference(set(one_step_instance.columns))

    one_step_instance[list(diff)] = 0
    one_step_instance = one_step_instance[clf.feature_names_in_]

    pred_probs = clf.predict_proba(one_step_instance)[0]

    p = np.power(pred_probs, 1)
    p = p / sum(p)
    choice = np.random.choice(clf.classes_, p=p)

    return choice

def generate_solo(clf, init_notes, struct_df):
    notes_instance = init_notes.copy()
    all_notes = notes_instance.to_numpy()
    for i in range(len(struct_df)):
        struct_instance = struct_df.iloc[i:i+1]

        pred_note_instance = one_step_predict(struct_instance, notes_instance, clf)

        all_notes = np.append(all_notes, pred_note_instance)

        notes_instance.iloc[:, 1:4] = notes_instance.iloc[:, 0:3]

        notes_instance.iloc[:, 0] = pred_note_instance

    # struct_df['generated_notes'] = all_notes[4:]
    # generated_notes = calculate_note_from_interval(struct_df, 'chord_root', 'generated_notes', 'generated_note_names')

    return all_notes[4:]