import pickle
from sklearn.pipeline import Pipeline

from src.modules.ts_models.preprocess import EventsFeatureImputer, DateFeatureAdder


class FrozenModel:
    def __init__(self, frozen_model_path):
        with open(frozen_model_path, 'rb') as f:
            model = pickle.load(f)

        self.pipeline = Pipeline([
            ('holidays', EventsFeatureImputer()),
            ('date_feature_gen', DateFeatureAdder()),
            ('model', model)
        ])

    def predict(self, X):
        return self.pipeline.predict(X)