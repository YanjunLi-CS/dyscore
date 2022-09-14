#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
preprocessors.py: 
"""

import numpy as np
import pandas as pd
from dyscore_model.utils import timer
from sklearn.base import BaseEstimator, TransformerMixin


class ProcessFeat(BaseEstimator, TransformerMixin):
    def __init__(self, feat_used):
        """
         # output_features:
         In files: 1:Stable, 4:MT, 6:VDW, 8:HM, 9:RT, 10:Match 12:Vina, 13:RF3 14:NN 15:DSX 16:DSXA 17:Score2 18:Xscore 19:HB+HSPC (In total 14 features)
         In numpy: 0:Stable, 1:MT, 2:VDW, 3:HM, 4:RT, 5:Match 6:Vina, 7:RF3, 8:NN, 9:DSX, 10:DSXA, 11:Score2, 12:Xscore, 13:HB+HSPC
        :param ds_path:
        :param mode:
        :param args:
        :param logger:
        """
        self.feat_used = feat_used

    def fit(self):
        return self

    def transform(self, X: pd.DataFrame) -> dict:
        with timer('Duration of feature process'):
            df = X.copy()
            assert df.columns[1] == 'Active', 'Input df 2nd column is not Active.'
            # Before to_numpy(), rm the non-numerical part, otherwise, it will be a numpy object.
            numerical = df.iloc[:, 1:].to_numpy()   # numerical col starts from "activate" (label)

            sample_names = df.iloc[:, 0].values.reshape(-1, 1)
            labels = numerical[:, 0]

            feats = numerical[:, 1:20]    # feats starts from "Score", ends by "Xscore"

            # HB+HSPC as 14th feature
            hb_hspc = np.reshape(numerical[:, 4] + numerical[:, 6], (-1, 1))
            feats = np.concatenate([feats, hb_hspc], axis=1)

            feats = feats[:, self.feat_used]

            samples = {'receptors': sample_names, 'feats': feats, 'labels': labels}
            return samples


