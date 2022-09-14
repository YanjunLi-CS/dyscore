#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
postprocessors.py: 
"""

import numpy as np
import pandas as pd
from dyscore_model.config import model_config


def merge_pred(X: dict) -> pd.DataFrame:
    samples = X["samples"]
    pred_lst = X["pred_lst"]
    final_pred = np.mean(pred_lst, axis=0, keepdims=False).reshape(-1, 1)

    feat_names = [model_config.FEAT_MAP[feat_id] for feat_id in model_config.FEAT_USED]
    df = pd.DataFrame(np.hstack((samples["receptors"], final_pred, samples["feats"])),
                      columns=["sampleID", "prediction"] + feat_names)
    return df
