import pickle
from sklearn.pipeline import Pipeline

from src.modules.ts_models.preprocess import EventsFeatureImputer, DateFeatureAdder


class FrozenModel:
    def __init__(self, frozen_model_path):
        self.model_path = frozen_model_path
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

        self.pipeline = Pipeline([
            ('holidays', EventsFeatureImputer()),
            ('date_feature_gen', DateFeatureAdder()),
        ])

    def fit(self, X, y):
        X_transf = self.pipeline.transform(X)
        self.model.fit(X_transf, y)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)

    def predict(self, X):
        X_transf = self.pipeline.transform(X)
        return self.model.predict(X_transf)