#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
data_loader.py: 
"""

import os
import os.path as osp
import pandas as pd


def load_ds(feat_csv):
    df = pd.read_csv(feat_csv)
    return df


def get_weight_fs(weight_path):
    fnames = os.listdir(weight_path)
    weight_fs = sorted([osp.join(weight_path, fname) for fname in fnames])
    return weight_fs
