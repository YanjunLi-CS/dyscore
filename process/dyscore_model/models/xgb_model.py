#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
xgb_model.py: 
"""

import xgboost as xgb
import pickle
from sklearn import metrics
from sklearn.base import BaseEstimator
import gc
import bz2
import time
import gzip
import multiprocessing as mp
from multiprocessing import Pool, Manager
from functools import partial
from dyscore_model import logger
from dyscore_model.utils import timer
from dyscore_model.config.model_config import XGBOOST_CONFIG


class XGB_MODEL(object):
    def __init__(self, weight_fs):
        self.params = XGBOOST_CONFIG
        self.weight_fs = weight_fs

    def fit(self, x_train, y_train, x_val, y_val, **kwargs):
        return self

    def predict(self, x):
        with timer('Duration of all models prediction'):
            m = Manager()
            shared_weight_fs = m.list(self.weight_fs)

            p = Pool(processes=1)
            rst_lst = p.map(partial(single_model_predict, x), shared_weight_fs)
            p.close()
            p.join()

            return {"samples": x, "pred_lst": rst_lst}

    def save(self, save_f):
        return self

    def load(self, weight_f):
        with timer('Duration of the model loading'):
            logger.info('Load model from {}'.format(weight_f))
            with open(weight_f, 'rb') as f:
                bst = pickle.load(f)

            return bst


def single_model_predict(x, weight_f):
    dpred = xgb.DMatrix(data=x['feats'])

    with timer('Duration of the model loading'):
        bst = load(weight_f)

    logger.info('Loading finishes, start to predict.')

    with timer('Duration of the model predicting'):
        rst = bst.predict(dpred, ntree_limit=bst.best_ntree_limit)

        del bst
        gc.collect()
    return rst


def load(weight_f):
    logger.info('Load model from {}'.format(weight_f))
    with open(weight_f, 'rb') as f:
        bst = pickle.load(f)

    return bst

