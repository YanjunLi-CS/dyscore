#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
config.py: 
"""
import argparse
import logging
LOG_LEVELS = list(logging._levelToName.values())


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_num', '-n', default=1, help='model ID')
    parser.add_argument('--log-level', default="INFO", choices=LOG_LEVELS)
    parser.add_argument('--weight_save', '-w', default="weight.pkl", help='path of weight file')
    parser.add_argument('--data_dir', default="./", help='directory of training set ')

    # ==========================
    parser.add_argument('--manualSeed', type=int, default=None,
                        help='The random seed for variable initialization and python random.')

    # ==========================
    parser.add_argument('--input_dim', type=int, default=14, help='Input dimension.')
    parser.add_argument('--output_dim', type=int, default=1, help='Output dimension.')
    parser.add_argument('--feat_remove', nargs='+', default=None, help='features to remove')
    # Note: 0 Score, 1 Stable, 2 LogP, 3 HB, 4 MT, 5 HSPC, 6 VDW, 7 BUMP, 8 HM, 9 RT, 10 Match, 11 Heavy, 12 Vina, 13 RF3, 14 NN, 15 DSX, 16 DSXA, 17 Score2, 18 Xscore, 19 HB+HSPC （adding）.
    #
    # final features: 1 4 6 8 9 10 12 13 14 15 16 17 18 19 (In total 14 features)
    # feat_remove and feat_keep should not be specified concurrently, if it is, then feat_remove would be ignored
    parser.add_argument('--feat_keep', nargs='+',
                        default=[1,4,6,8,9,10,12,13,14,15,16,17,18,19],
                        help='features to keep. '
                             'dyScore: [1,4,6,8,9,10,12,13,14,15,16,17,18,19]')
    parser.add_argument('--add_feat', type=int,nargs='+', default=[20, 21, 22, 23, 24, 25, 26, 27],
                        help='Whether add chemical structure info.'
                             '[20, 21, 22, 23, 24, 25, 26, 27] for DyScore-MF')

    # ==========================
    args = parser.parse_args()
    return args


def get_logger(log_level):
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(funcName)s(%(lineno)d): %(message)s',
                                  "%H:%M:%S")
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    stream = logging.StreamHandler()
    stream.setLevel(log_level.upper())
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger


args = get_arguments()
logger = get_logger(args.log_level)
