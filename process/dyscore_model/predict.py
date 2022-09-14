#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
predict.py: 
"""

import pandas as pd
import argparse
from dyscore_model.processing.data_loader import load_ds, get_weight_fs
from dyscore_model.processing import postprocessors as postproc
from dyscore_model.pipeline import build_pipeline
from dyscore_model.processing.validation import validate_args, validate_inputs
from dyscore_model import logger

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_f', required=True, help='The input filename with csv format.')
    parser.add_argument('-o', '--output_f', required=True, help='The output filename with full path.')
    parser.add_argument('-w', '--weight_path', required=True, help='The directory storing the model weights.')
    args = parser.parse_args()
    return args


def make_prediction(input_data: pd.DataFrame, weight_fs: list) -> dict:
    validated_data = validate_inputs(input_data=input_data)

    dyscore_pipe = build_pipeline(weight_fs)
    pred_result = dyscore_pipe.predict(validated_data)
    pred_df = postproc.merge_pred(pred_result)
    pred_df = pred_df[["sampleID", "prediction"]]
    return pred_df


def main():
    args = get_arguments()

    if not validate_args(args.input_f, args.output_f, args.weight_path):
        return 1

    data = load_ds(args.input_f)
    weight_fs = get_weight_fs(args.weight_path)
    rst = make_prediction(data, weight_fs)

    rst.to_csv(args.output_f, index=False)
    logger.info(f'The prediction is saved to {args.output_f}')
    return 0

if __name__ == '__main__':
    main()

