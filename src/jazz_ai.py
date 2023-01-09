from src.feature_matrix import create_feature_matrix
import pandas as pd
from src.generate_solo import generate_solo

class JazzAI:
    def __init__(self, clf_function, melody_note_lags=range(1,5), chord_root_lags=range(-1,-2,-1), chord_type_lags=range(-1,-2,-1)) -> None:
        self.clf = clf_function()
        self.melody_note_lags = melody_note_lags
        self.chord_root_lags = chord_root_lags
        self.chord_type_lags = chord_type_lags

        self.training_data = None
        self.feature_matrix = None
        self.X = None
        self.y = None

    def fit(self, training_data):
        self.training_data = training_data

        self.feature_matrix = create_feature_matrix(training_data, melody_note_lags=range(1,5), chord_root_lags=range(-1,-2,-1), chord_type_lags=range(-1,-2,-1))
        self.y = self.feature_matrix['chord_root_melody_note_interval']
        self.X = self.feature_matrix.drop(['chord_root_melody_note_interval'], axis=1)
        self.X = pd.get_dummies(self.X)

        self.clf.fit(self.X, self.y)

        pred_probs = self.clf.predict_proba(self.X)
        pred = self.clf.predict(self.X)

        self.eval_df = pd.concat([pd.DataFrame({'actual': self.y.reset_index(drop=True), 'pred': pred}), pd.DataFrame(pred_probs, columns=self.clf.classes_)], axis=1)
        self.eval_df.index = self.y.index
        
        return self.eval_df

    def predict(self, new_data):
        return self.clf.predict(new_data)

    def generate_solo(self, init_notes, struct_df):
        # init_notes = ["5", "4", "1", "b3"]  TODO: assert length matches provided lags
        # struct_df = joined.query('melid==1')[['chord_3rd', 'chord_5th', 'chord_7th', 'chord_root_num']]  # TODO assert cols

        generated_notes = struct_df.copy()

        init_notes_struct = pd.DataFrame(init_notes[::-1]).T
        init_notes_struct.columns = [f"chord_root_melody_lag_{i}_interval" for i in self.melody_note_lags]

        struct_df = create_feature_matrix(struct_df, melody_note_col=None, chord_root_lags=self.chord_root_lags, chord_type_lags=self.chord_type_lags, group_by_col=None)

        all_notes = generate_solo(self.clf, init_notes_struct, struct_df)

        # generated_notes['generated_notes'][:min(self.melody_note_lags + self.chord_root_lags + self.chord_type_lags)] = all_notes
        generated_notes['generated_notes'] = list(all_notes) + [pd.NA]*(-1*min(min(self.melody_note_lags), min(self.chord_root_lags), min(self.chord_type_lags)))

        generated_notes = pd.concat([pd.DataFrame(index=range(0, len(init_notes)), columns=generated_notes.columns), generated_notes])
        generated_notes.loc[0:(len(init_notes)-1), 'generated_notes'] = init_notes

        return generated_notes 