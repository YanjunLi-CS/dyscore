#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
pipeline.py: 
"""

from sklearn.pipeline import Pipeline
from dyscore_model.processing import preprocessors as preproc
from dyscore_model.config import model_config
from dyscore_model.models.xgb_model import XGB_MODEL


def build_pipeline(weight_fs):
    dyscore_pipe = Pipeline(
        [
            ('data_process', preproc.ProcessFeat(model_config.FEAT_USED)),
            ('xgb_model', XGB_MODEL(weight_fs)),
        ]
    )
    return dyscore_pipe
