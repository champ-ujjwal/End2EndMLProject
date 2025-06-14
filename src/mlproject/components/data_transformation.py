import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.mlproject.utils import save_object

from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import os


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')  # artifacts -> pkl file save hoga

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is responsible for data transformation.
        It returns a ColumnTransformer object that applies different transformations
        to different columns of the dataset.
        """
        try:    
            # we can do like this, just need to define X, but here we are doing hardcoding
            # num_features = X.select_dtypes(exclude="object").columns
            # cat_features = X.select_dtypes(include="object").columns
            numerical_features =["writing_score", "reading_score"]
            categorical_features = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]
            # filling missing values for numerical features with median
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            # filling missing values for categorical features with most frequent value
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehotencoder', OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))  # OneHotEncoder creates sparse matrix
            ])

            logging.info(f"Categorical features: {categorical_features}")
            logging.info(f"Numerical features: {numerical_features}")
            
            # combinig both numerical and categorical pipelines
            preprocessor = ColumnTransformer(
                [
                     ("num_pipeline", num_pipeline, numerical_features),
                     ("cat_pipeline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor




        except Exception as e:
            raise CustomException(e, sys)
            
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_features = ["writing_score", "reading_score"]
            
            # divide the data into input and target features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            #  divide the data into input and target features for test data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  
            target_feature_test_df = test_df[target_column_name]
            
            logging.info("Applying preprocessing object on training and testing dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("Saved preprocessing object")
            # save the preprocessor object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )





        except Exception as e:
            raise CustomException(e, sys)