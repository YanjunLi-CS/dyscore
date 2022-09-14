#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
dyScore.py:
"""

import xgboost as xgb
import pickle
from sklearn import metrics


feat_dict = {
    0: 'Stable',
    1: 'MT',
    2: 'VDW',
    3: 'HM',
    4: 'RT',
    5: 'Match',
    6: 'Vina',
    7: 'RF3',
    8: 'NN',
    9: 'DSX',
    10: 'DSXA',
    11: 'Score2',
    12: 'Xscore',
    13: 'HB-HSPC'
}

CONFIG = {
    'eta': 0.05,
    'max_depth': 30,
    'subsample': 0.85,
    'scale_pos_weight': 60,
    'objective': 'binary:logistic',
    'seed': 111,
    'num_boost_round': 1000,   # 10000
    'early_stopping_rounds': 20,

    # random forest in xgboost
    'num_parallel_tree':30,
    'colsample_bynode':0.3
}


class Model(object):
    def __init__(self, logger):
        self.params = CONFIG
        self.logger = logger

    def eval_metric(self, preds, dtrain):
        labels = dtrain.get_label()
        accumulated_auc = 0.0

        for receptor_name, idx_lst in self.valid_receptor_idx_d.items():
            y_true = labels[idx_lst]
            y_pred = preds[idx_lst]
            per_target_auc = metrics.roc_auc_score(y_true, y_pred)
            accumulated_auc += per_target_auc
        avg_auc = accumulated_auc / len(self.valid_receptor_idx_d)
        return "AUC", avg_auc

    def fit(self, x_train, y_train, x_val, y_val, **kwargs):
        self.logger.info('Start to fitting xgb model.')
        dtrain = xgb.DMatrix(data=x_train, label=y_train)
        dval = xgb.DMatrix(data=x_val, label=y_val)

        evallist = [(dval, 'eval')]
        self.valid_receptor_idx_d = kwargs.get("receptor_idx_d", "None")

        assert self.valid_receptor_idx_d is not None,  \
            "The valid receptor idx is not given to calculate the per target AUC (early stop metric)."

        self.bst = xgb.train(self.params, dtrain=dtrain, num_boost_round=self.params['num_boost_round'],
                             evals=evallist, early_stopping_rounds=self.params['early_stopping_rounds'],
                             feval=self.eval_metric, maximize=True)
        self.logger.info('best AUC: {}'.format(self.bst.best_score))

    def predict(self, x):
        dpred = xgb.DMatrix(data=x)
        return self.bst.predict(dpred, ntree_limit=self.bst.best_ntree_limit)

    def save(self, save_f):
        self.logger.info('Save model to {}'.format(save_f))
        pickle.dump(self.bst, open(save_f, 'wb'), protocol=4)  # set protocol=4 to serialize file over 4gb(this is mainly for rf in xgb)

    def load(self, save_f):
        self.logger.info('Load model from {}'.format(save_f))
        self.bst = pickle.load(open(save_f, 'rb'))


if __name__ == '__main__':
    pass
