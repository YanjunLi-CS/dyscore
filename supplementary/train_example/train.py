#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
train.py: 
"""
import os
import os.path as osp
import importlib
import random
from config import args, logger
from utils import timer
from dataload_ml import DataSet
from dyScore import Model
DATA_ROOT_PATH = '../experimental_data'
WEIGHT_ROOT_PATH = '../weight'
OUT_ROOT_PATH = '../tmp/out'


def main():
    script_dir = osp.realpath(__file__)
    os.chdir(osp.dirname(script_dir))
    logger.info(os.getcwd())
    logger.info('Process Id: {}'.format(os.getpid()))

    #  ========================================================================
    # Basic config
    weight_path = osp.join(WEIGHT_ROOT_PATH, str(args.model_num))
    if args.model_num != 0 and osp.exists(weight_path):
        raise ValueError('Weight folder has existed. => {}'.format(weight_path))

    args_dict = vars(args)

    if args.manualSeed is None:
        args.manualSeed = random.randint(1, 10000)
    logger.info('Random Seed: {}'.format(args.manualSeed))
    random.seed(args.manualSeed)

    #  ========================================================================
    # Data related
    ds_path = DATA_ROOT_PATH
    train_ds = DataSet(ds_path=ds_path, mode='train', args=args_dict, logger=logger)
    train_samples = train_ds.fetch()

    # Validation has no augmentation
    valid_ds = DataSet(ds_path=ds_path, mode='valid', args=args_dict, logger=logger)
    valid_samples = valid_ds.fetch()

    # Validation has no augmentation
    test_ds = DataSet(ds_path=ds_path, mode='test', args=args_dict, logger=logger)
    test_samples = test_ds.fetch()

    #  ========================================================================
    # Output related
    out_path = osp.join(OUT_ROOT_PATH, str(args.model_num))
    if not osp.exists(out_path):
        os.makedirs(out_path)

    #  ========================================================================
    # Model related
    model = Model(logger)

    with timer('=> Model fitting'):
        model.fit(train_samples['feats'], train_samples['labels'], valid_samples['feats'],
                  valid_samples['labels'], receptor_idx_d=valid_samples["receptor_idx_d"])

    with timer('=> Model saving'):
        saved_model_f = osp.join(weight_path, 'weight.pkl')
        model.save(saved_model_f)

    with timer('=> Model prediction'):
        valid_y_pred = model.predict(valid_samples['feats'])
        logger.info(valid_y_pred)

    for ds_name, samples in zip(['valid', 'test'], [valid_samples, test_samples]):
        with timer('=> Model evaluation for {}'.format(ds_name)):
            analyzed_dict = dict()
            analyzed_dict['scope'] = ds_name
            analyzed_dict['y_true'] = samples['labels']
            analyzed_dict['y_pred'] = model.predict(samples['feats'])
            analyzed_dict['sample_name'] = samples['sample_name']


if __name__ == '__main__':
    main()

