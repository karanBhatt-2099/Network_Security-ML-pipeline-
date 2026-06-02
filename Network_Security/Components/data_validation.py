from Network_Security.Entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)

from Network_Security.Entity.config_entity import (
    DataValidationConfig
)

from Network_Security.Exception.exception import (
    NetworkSecurityException
)

from Network_Security.Logging.logger import logging

from Network_Security.Constants.training_pipeline import (
    SCHEMA_FILE_PATH
)

from scipy.stats import ks_2samp

import os
import sys
import pandas as pd

from Network_Security.utils.main_utils.utils import (
    read_yaml_file,
    write_yaml_file
)


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = (
                data_ingestion_artifact
            )

            self.data_validation_config = (
                data_validation_config
            )

            self._schema_config = read_yaml_file(
                SCHEMA_FILE_PATH
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(
        self,
        dataframe: pd.DataFrame
    ) -> bool:

        try:
            number_of_columns = len(
                self._schema_config["columns"]
            )

            logging.info(
                f"Required columns : {number_of_columns}"
            )

            logging.info(
                f"Available columns : {len(dataframe.columns)}"
            )

            return (
                len(dataframe.columns)
                == number_of_columns
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self,
        base_df,
        current_df,
        threshold=0.05
    ) -> bool:

        try:
            status = True
            report = {}

            for column in base_df.columns:

                d1 = base_df[column]
                d2 = current_df[column]

                test = ks_2samp(d1, d2)

                if test.pvalue >= threshold:
                    drift_found = False
                else:
                    drift_found = True
                    status = False

                report[column] = {
                    "p_value": float(test.pvalue),
                    "drift_status": drift_found
                }

            drift_report_file_path = (
                self.data_validation_config.drift_report_file_path
            )

            write_yaml_file(
                file_path=drift_report_file_path,
                content=report
            )

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(
        self
    ) -> DataValidationArtifact:

        try:
            train_file_path = (
                self.data_ingestion_artifact.trained_file_path
            )

            test_file_path = (
                self.data_ingestion_artifact.test_file_path
            )

            train_df = self.read_data(
                train_file_path
            )

            test_df = self.read_data(
                test_file_path
            )

            status = self.validate_number_of_columns(
                train_df
            )

            if not status:
                raise Exception(
                    "Train dataframe column validation failed"
                )

            status = self.validate_number_of_columns(
                test_df
            )

            if not status:
                raise Exception(
                    "Test dataframe column validation failed"
                )

            status = self.detect_dataset_drift(
                base_df=train_df,
                current_df=test_df
            )

            os.makedirs(
                os.path.dirname(
                    self.data_validation_config.valid_train_file_path
                ),
                exist_ok=True
            )

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )

            data_validation_artifact = (
                DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_validation_config.valid_train_file_path,
                    valid_test_file_path=self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)