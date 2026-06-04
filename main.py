import sys

from Network_Security.Components.data_ingestion import DataIngestion
from Network_Security.Components.data_validation import DataValidation
from Network_Security.Components.data_transformation import DataTransformation
from Network_Security.Components.model_trainer import ModelTrainer

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging

from Network_Security.Entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)


if __name__ == "__main__":

    try:

        # =====================================
        # Training Pipeline Configuration
        # =====================================
        training_pipeline_config = TrainingPipelineConfig()

        # =====================================
        # Data Ingestion
        # =====================================
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )

        data_ingestion = DataIngestion(
            data_ingestion_config=data_ingestion_config
        )

        logging.info("Starting Data Ingestion")

        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        print(data_ingestion_artifact)

        logging.info(
            f"Data Ingestion Artifact: {data_ingestion_artifact}"
        )

        # =====================================
        # Data Validation
        # =====================================
        data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config
        )

        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config
        )

        logging.info("Starting Data Validation")

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        print(data_validation_artifact)

        logging.info(
            f"Data Validation Artifact: {data_validation_artifact}"
        )

        # =====================================
        # Data Transformation
        # =====================================
        data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config
        )

        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
        )

        logging.info("Starting Data Transformation")

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        print(data_transformation_artifact)

        logging.info(
            f"Data Transformation Artifact: {data_transformation_artifact}"
        )

        # =====================================
        # Model Training
        # =====================================
        model_trainer_config = ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config
        )

        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact
        )

        logging.info("Starting Model Training")

        model_trainer_artifact = (
            model_trainer.initiate_model_trainer()
        )

        print(model_trainer_artifact)

        logging.info(
            f"Model Trainer Artifact: {model_trainer_artifact}"
        )

        logging.info(
            "Training Pipeline completed successfully."
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)