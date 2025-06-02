import os
from glob import glob

import joblib
import pandas as pd
from scipy.stats import norm
import numpy as np
from arch import arch_model
class BuildModel:
    """Class for cleaning, training and making predictions based on garch model
    Attributes
    -----------
    repo : SQLRepository
        The repository where the training data will be stored.
    model_directory : str
       Path for directory where trained models will be stored.
    Methods
    -------
    wrangle_data
        Generate returns from data in database.
    fit
        Fit model to training data.
    predict
        Generate volatilty forecast from trained model.
    dump
        Save trained model to file.
    load
        Load trained model from file.
    """
    def __init__(self, table_name, repo):
        self.table_name=table_name
        self.repo=repo
    def wrangle_data(self):
        df=self.repo.read_table(table_name = self.table_name)
        df['return']=df['Close'].pct_change()*100 
        return df["return"].dropna()
    def fit_data(self,data,p,q):
        model=arch_model(
            data,
            p=p,
            q=q,
            rescale=False
        ).fit(disp=0)
        return model
    