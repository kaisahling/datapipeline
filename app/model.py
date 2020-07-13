from abc import ABC, abstractmethod
import os
import injector
from joblib import load

PATH = os.path.dirname(os.path.abspath(__file__))


class ModelAbs(ABC, injector.Module):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self):
        pass


class DummyClassifier(ModelAbs):
    # Load the list of top cards
    def __init__(self):
        super().__init__()
        global PATH
        path_model = os.path.join(PATH, "models")

        path_clf = os.path.join(path_model, "dummy_clf.joblib")
        self.clf = load(path_clf)

    def apply(self, data):
        """
        This functions applies the model to the given data and return the classification
        :param data: DataFrame
        :return: int
        """
        X = data.to_numpy()
        result = self.clf.predict(X)
        return result[0]
