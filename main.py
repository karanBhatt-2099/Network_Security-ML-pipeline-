import sys

from Network_Security.Components.data_ingestion import (
    DataIngestion
)

from Network_Security.Components.data_validation import (
    DataValidation
)

from Network_Security.Exception.exception import (
    NetworkSecurityException
)

from Network_Security.Logging.logger import logging

from Network_Security.Entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig
)


if __name__ == "__main__":

    try:

        training_pipeline_config = (
            TrainingPipelineConfig()
        )

        data_ingestion_config = (
            DataIngestionConfig(
                training_pipeline_config
            )
        )

        data_validation_config = (
            DataValidationConfig(
                training_pipeline_config
            )
        )

        data_ingestion = DataIngestion(
            data_ingestion_config
        )

        logging.info(
            "Starting Data Ingestion"
        )

        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        print(data_ingestion_artifact)

        logging.info(
            f"Data Ingestion Artifact : {data_ingestion_artifact}"
        )

        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config
        )

        logging.info(
            "Starting Data Validation"
        )

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        print(data_validation_artifact)

        logging.info(
            f"Data Validation Artifact : {data_validation_artifact}"
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)