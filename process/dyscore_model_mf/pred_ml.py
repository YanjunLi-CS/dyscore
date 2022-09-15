#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pred_ml.py: 
"""

import importlib
import random
from config import args
from utils import *
from loader.dataloader_ml import DataSet


def main():

    logger.info(os.getcwd())
    logger.info('Process Id: {}'.format(os.getpid()))

    #  ========================================================================
    # Basic config
    MODULE = importlib.import_module('models.' + args.model_name)


    weight_path = args.weight_dir
    if not osp.exists(weight_path):
        raise ValueError('Weight file {} does not exist.'.format(weight_path))

    args_dict = vars(args)

    if args.manualSeed is None:
        args.manualSeed = random.randint(1, 10000)
    logger.info('Random Seed: {}'.format(args.manualSeed))
    random.seed(args.manualSeed)

    #  ========================================================================
    # Data related
    ds_name = args.input_file
    test_ds = DataSet(ds_path=ds_name, mode="pred", args=args_dict, logger=logger)
    test_samples = test_ds.fetch()

    #  ========================================================================
    # Output related
    out_path = args.output_file

    #  ========================================================================
    # Model related
    model = MODULE.Model(logger)

    prediction=[[],[],[]]
    record=[["sampleID","prediction"]]
    #three model
    for i in range(1,4):
        #  ========================================================================
        # Restore the previous weight
        restore_weight_path=weight_path+"/weight"+str(i)+".pkl"
        logger.info(f'==> restoring weights from {}'.format(restore_weight_path))
        logger.info(restore_weight_path)
        model.load(restore_weight_path)

        #  ========================================================================
        # Evaluation process
        with timer('=> Model prediction for {}'.format(ds_name)):
            analyzed_dict = dict()
            #analyzed_dict['scope'] = ds_name
#            analyzed_dict['y_pred'] = model.predict(test_samples['feats'])
            prediction[i-1]= model.predict(test_samples['feats'])
#            print(test_samples['sample_name'])
            #print(analyzed_dict['y_pred'])
            #analyzed_dict['sample_name'] = test_samples['sample_name']

            # The pred_ds has label
            #analyzed_dict['y_true'] = test_samples['labels']
            # # The pred_ds does not label
            # analyzed_dict['y_true'] = np.zeros_like(analyzed_dict['y_pred'])

#            amm = AlyModelML(analyzed_dict, test_samples["receptor_idx_d"], out_path=out_path)
#            amm.aly_auc()
#            amm.aly_ef()
#            amm.aly_bedroc()
    for i in range(len(prediction[0])):
        record.append([test_samples['sample_name'][i],(prediction[0][i]+prediction[1][i]+prediction[2][i])/3.0])
    write_csv(out_path,record)
    #logger.info(f'==> Prediction record to {out_path}')


def write_csv(name,data):
    fp=open(name,"w")
    for line in data:
        newline=[]
        for each in line:
            newline.append(str(each))
        allstr=",".join(newline)
        fp.write("%s\n" % allstr)
    fp.close()


if __name__ == '__main__':
    main()
