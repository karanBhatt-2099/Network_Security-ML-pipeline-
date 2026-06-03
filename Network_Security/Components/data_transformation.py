import sys
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Network_Security.Constants.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS
)

from Network_Security.Entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from Network_Security.Entity.config_entity import (
    DataTransformationConfig
)

from Network_Security.Exception.exception import (
    NetworkSecurityException
)

from Network_Security.Logging.logger import logging

from Network_Security.utils.main_utils.utils import (
    save_numpy_array_data,
    save_object
)


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Creates preprocessing pipeline.
        """
        try:
            logging.info(
                "Creating Data Transformation Pipeline"
            )

            imputer = KNNImputer(
                **DATA_TRANSFORMATION_IMPUTER_PARAMS
            )

            processor = Pipeline(
                [
                    ("imputer", imputer)
                ]
            )

            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(
        self
    ) -> DataTransformationArtifact:

        try:
            logging.info(
                "Reading validated train and test data"
            )

            train_df = self.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = self.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            logging.info(
                f"Train Shape: {train_df.shape}"
            )

            logging.info(
                f"Test Shape: {test_df.shape}"
            )

            # ==========================
            # Train Data
            # ==========================

            input_feature_train_df = train_df.drop(
                columns=[TARGET_COLUMN],
                axis=1
            )

            target_feature_train_df = train_df[
                TARGET_COLUMN
            ]

            target_feature_train_arr = (
                target_feature_train_df.replace(-1, 0)
            )

            # ==========================
            # Test Data
            # ==========================

            input_feature_test_df = test_df.drop(
                columns=[TARGET_COLUMN],
                axis=1
            )

            target_feature_test_df = test_df[
                TARGET_COLUMN
            ]

            target_feature_test_arr = (
                target_feature_test_df.replace(-1, 0)
            )

            # ==========================
            # Preprocessing
            # ==========================

            preprocessing_obj = (
                self.get_data_transformer_object()
            )

            preprocessing_obj.fit(
                input_feature_train_df
            )

            transformed_train_features = (
                preprocessing_obj.transform(
                    input_feature_train_df
                )
            )

            transformed_test_features = (
                preprocessing_obj.transform(
                    input_feature_test_df
                )
            )

            # ==========================
            # Create Final Arrays
            # ==========================

            train_arr = np.c_[
                transformed_train_features,
                np.array(target_feature_train_arr)
            ]

            test_arr = np.c_[
                transformed_test_features,
                np.array(target_feature_test_arr)
            ]

            # ==========================
            # Save Train/Test Arrays
            # ==========================

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_arr
            )

            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_arr
            )

            # ==========================
            # Save Preprocessor Object
            # ==========================

            save_object(
                file_path=self.data_transformation_config.preprocessor_object_file_path,
                obj=preprocessing_obj
            )

            # ==========================
            # Create Artifact
            # ==========================

            data_transformation_artifact = (
                DataTransformationArtifact(
                    transformed_train_file_path=
                    self.data_transformation_config.transformed_train_file_path,

                    transformed_test_file_path=
                    self.data_transformation_config.transformed_test_file_path,

                    transformed_object_file_path=
                    self.data_transformation_config.preprocessor_object_file_path
                )
            )

            logging.info(
                f"Data Transformation completed successfully"
            )

            logging.info(
                f"Data Transformation Artifact: {data_transformation_artifact}"
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e