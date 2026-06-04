import os
import sys

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging

from Network_Security.Entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from Network_Security.Entity.config_entity import (
    ModelTrainerConfig
)

from Network_Security.utils.main_utils.utils import (
    load_numpy_array_data,
    save_object,
    load_object,
    evaluate_models
)

from Network_Security.utils.ml_utils.metric.classification_metric import (
    get_classification_score
)

from Network_Security.utils.ml_utils.model.estimator import (
    NetworkModel
)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = (
                data_transformation_artifact
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(
        self,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        models = {
            "Random Forest": RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(),
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "AdaBoost": AdaBoostClassifier()
        }

        params = {

            "Decision Tree": {
                "criterion": [
                    "gini",
                    "entropy",
                    "log_loss"
                ]
            },

            "Random Forest": {
                "n_estimators": [
                    8,
                    16,
                    32,
                    64,
                    128,
                    256
                ]
            },

            "Gradient Boosting": {
                "learning_rate": [
                    0.1,
                    0.01,
                    0.001
                ],
                "subsample": [
                    0.6,
                    0.7,
                    0.8,
                    0.9
                ],
                "n_estimators": [
                    8,
                    16,
                    32,
                    64,
                    128
                ]
            },

            "Logistic Regression": {},

            "AdaBoost": {
                "learning_rate": [
                    0.1,
                    0.01,
                    0.001
                ],
                "n_estimators": [
                    8,
                    16,
                    32,
                    64,
                    128
                ]
            }
        }

        model_report = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            param=params
        )

        best_model_score = max(model_report.values())

        best_model_name = list(
            model_report.keys()
        )[
            list(model_report.values()).index(
                best_model_score
            )
        ]

        best_model = models[best_model_name]

        logging.info(
            f"Best Model Found: {best_model_name}"
        )

        # Train metric
        y_train_pred = best_model.predict(X_train)

        train_metric = get_classification_score(
            y_true=y_train,
            y_pred=y_train_pred
        )

        # Test metric
        y_test_pred = best_model.predict(X_test)

        test_metric = get_classification_score(
            y_true=y_test,
            y_pred=y_test_pred
        )

        preprocessor = load_object(
            self.data_transformation_artifact.preprocessor_object_file_path
        )

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model
        )

        model_dir = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )

        os.makedirs(model_dir, exist_ok=True)

        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=network_model
        )

        model_trainer_artifact = (
            ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_metric,
                test_metric_artifact=test_metric
            )
        )

        logging.info(
            f"Model Trainer Artifact : {model_trainer_artifact}"
        )

        return model_trainer_artifact

    def initiate_model_trainer(
        self
    ) -> ModelTrainerArtifact:

        try:

            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]

            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            model_trainer_artifact = self.train_model(
                X_train,
                y_train,
                X_test,
                y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)