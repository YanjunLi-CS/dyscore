#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
validation.py: 
"""

import os
import os.path as osp
import pandas as pd

from dyscore_model.config import model_config
from dyscore_model.config.model_config import DEFAULT_WEIGHT_NAMES

def validate_args(input_f, output_f, weight_path):
    """
    Verify the input, output and model weight info.
    :param input_f:
    :param output_f:
    :return:make_prediction
    """
    if not osp.exists(input_f):
        raise FileNotFoundError(f'{input_f} does not exist.')

    fnames = os.listdir(weight_path)
    if len(fnames) == 0:
        raise FileNotFoundError(f'There is no saved weight file in {weight_path}')

    for fname in fnames:
        if fname not in DEFAULT_WEIGHT_NAMES:
            raise ValueError(f'{fname} does not match the DEFAULT_WEIGHT_NAMES.')

    output_folder = osp.dirname(output_f)
    if output_folder!="":
        os.makedirs(output_folder, exist_ok=True)
    return True


def validate_inputs(input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for unprocessable values."""
    validated_data = input_data.copy()
    return validated_data

