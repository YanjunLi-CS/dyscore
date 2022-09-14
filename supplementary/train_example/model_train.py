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


def main():
    script_dir = osp.realpath(__file__)
    os.chdir(osp.dirname(script_dir))
    logger.info(os.getcwd())
    logger.info('Process Id: {}'.format(os.getpid()))

    #  ========================================================================
    # Basic config

    args_dict = vars(args)

    if args.manualSeed is None:
        args.manualSeed = random.randint(1, 10000)
    logger.info('Random Seed: {}'.format(args.manualSeed))
    random.seed(args.manualSeed)

    #  ========================================================================
    # Data related
    ds_path = args.data_dir
    train_ds = DataSet(ds_path=ds_path, mode='train', args=args_dict, logger=logger)
    train_samples = train_ds.fetch()

    # Validation has no augmentation
    valid_ds = DataSet(ds_path=ds_path, mode='valid', args=args_dict, logger=logger)
    valid_samples = valid_ds.fetch()
    
    # test has no augmentation
    test_ds = DataSet(ds_path=ds_path, mode='test', args=args_dict, logger=logger)
    test_samples = test_ds.fetch()


    #  ========================================================================
    # Model related
    model = Model(logger)

    with timer('=> Model fitting'):
        model.fit(train_samples['feats'], train_samples['labels'], valid_samples['feats'],
                  valid_samples['labels'], receptor_idx_d=valid_samples["receptor_idx_d"])

    with timer('=> Model saving'):
        saved_model_f = args.weight_save
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

    logger.info("Trained model is saved to "+args.weight_save)
    logger.info("Prediction results for test set:")
    print("sampleID,prediction")
    for i in range(len(analyzed_dict['sample_name'])):
        print(analyzed_dict["sample_name"][i]+","+str(analyzed_dict['y_pred'][i]))


if __name__ == '__main__':
    main()

