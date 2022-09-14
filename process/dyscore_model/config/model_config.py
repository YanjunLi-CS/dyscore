#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
model_config.py: 
"""

# Model
#  Start from Score (0), 1: Stable, 19: hb + hspc'
FEAT_MAP = {
 1: "Stable",
 2: "LogP",
 3: "HB",
 4: "MT",
 5: "HSPC",
 6: "VDW",
 7: "BUMP",
 8: "HM",
 9: "RT",
 10: "Match",
 11: "Heavy",
 12: "Vina",
 13: "RF3",
 14: "NN",
 15: "DSX",
 16: "DSXA",
 17: "Score2",
 18: "Xscore",
 19: "HB+HSPC"
}

FEAT_USED = [1, 4, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19]
# Note: 0 Score, 1 Stable, 2 LogP, 3 HB, 4 MT, 5 HSPC, 6 VDW, 7 BUMP, 8 HM, 9 RT, 10 Match, 11 Heavy,
# 12 Vina, 13 RF3, 14 NN, 15 DSX, 16 DSXA, 17 Score2, 18 Xscore, 19 HB+HSPC （Add their values.
# final features: 1 4 6 8 9 10 12 13 14 15 16 17 18 19 (In total 14 features)
assert all(feat_id in FEAT_MAP for feat_id in FEAT_USED), "Features used do not exist in the FeatMap"
assert sorted(FEAT_USED) == FEAT_USED, \
    "Feature used id do not follow the ascending order, " \
    "will cause problems for column names generated in final csv file."

INPUT_DIM = len(FEAT_USED)

XGBOOST_CONFIG = {
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

DEFAULT_WEIGHT_NAMES = {'weight1.pkl', 'weight2.pkl', 'weight3.pkl'}


