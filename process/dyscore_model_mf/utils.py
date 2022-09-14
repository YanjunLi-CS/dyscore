#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
utils.py: 
"""
import os
import os.path as osp
import numpy as np
import os
from pathlib import Path
from shutil import rmtree
import re
import json
from collections import OrderedDict
import pandas as pd
from contextlib import contextmanager
import time
from sklearn import metrics
#from rdkit.ML.Scoring.Scoring import CalcBEDROC
import logging
from config import logger


def rm_dump_dir(model_name, pattern):
    for x in ['summaries', 'weight']:
        base_dir = osp.join(x, model_name)
        for p in Path(base_dir).glob(pattern + '*'):
            rmtree(p)


def create_dir(root_dir, x):
    target_dir = osp.join(root_dir, x)
    if not osp.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir


def create_weight_dir(root_weight_dir, metrics_lst):
    weight_dir_dict = {}
    for metric in metrics_lst:
        weight_dir_dict[metric] = create_dir(root_weight_dir, metric + '/')
    return weight_dir_dict


def write_config(dest_dir, f_name, *args):
    if not osp.exists(dest_dir):
        os.makedirs(dest_dir)

    item_list = os.listdir(dest_dir)
    num_config_files = 0
    for x in item_list:
        if re.search(r'{}_config_\d\.json'.format(f_name), x):
            num_config_files += 1

    new_config_name = osp.join(dest_dir, '{}_config_{}.json'.format(f_name, num_config_files))
    logger.info("num_config_files={}, new_config_name={}".format(num_config_files, new_config_name))
    data_dict_list = []
    for data_dict in args:
        print_dict_byline(data_dict)    # stdout the config dict
        order_dict = OrderedDict(sorted(data_dict.items(), key=lambda t: t[0]))
        data_dict_list.append(order_dict)
    with open(new_config_name, 'w') as fp:
        json.dump(data_dict_list, fp, indent=2)


def print_dict_byline(target_dict):
    for k, v in target_dict.items():
        logger.info('{}:'.format(k).ljust(15) + '{}'.format(v))
    logger.info('===============================')


@contextmanager
def timer(message):
    """Context manager for timing snippets of code."""
    tick = time.time()
    yield
    tock = time.time()

    diff = tock - tick
    if diff >= 3600:
        duration = "{:.2f}h".format(diff / 3600)
    elif diff >= 60:
        duration = "{:.2f}m".format(round(diff / 60))
    else:
        duration = "{:.2f}s".format(diff)
    logger.info("{}: {}".format(message, duration))


def cal_ef(sorted_y_true, sorted_y_pred, ratio_lst, **kwargs):
    """
    EF(x%) = (#actives at x% / #compounds at x%) * (#total compounds / #total actives)
    :param sorted_y_true: Descent order
    :param sorted_y_pred:
    :param ratio:
    :return:
    """
    receptor_type = kwargs['receptor_type'] if kwargs else None
    ef_lst = []
    total_compounds = len(sorted_y_true)
    total_actives = np.count_nonzero(sorted_y_true)
    assert (total_actives != 0), '{}'.format(receptor_type)
    upper_ef = total_compounds / total_actives
    logger.debug('EF upper boundary: {}'.format(upper_ef))

    for ratio in ratio_lst:
        if ratio < 1.0:
            # It is for ratio percentage
            compounds = int(ratio * total_compounds)
            actives = np.count_nonzero(sorted_y_true[:compounds])
        else:
            # It is for #top-N:
            compounds = ratio
            actives = np.count_nonzero(sorted_y_true[:ratio])

        ef = (actives / compounds) * (total_compounds / total_actives)
        ef_lst.extend([ef])
    ef_lst = list(np.around(np.array(ef_lst), decimals=3))
    return ef_lst


def cal_bedroc(sorted_y_true, sorted_y_pred, ratio_lst, **kwargs):
    """

    :param sorted_y_true: Descent order
    :param sorted_y_pred:
    :param ratio:
    :return:
    """
    bedroc_lst = []
    for ratio in ratio_lst:
        sorted_scores_label = list(zip(sorted_y_true, sorted_y_pred))
        bedroc = CalcBEDROC(sorted_scores_label, col=0, alpha=ratio)
        bedroc_lst.extend([bedroc])
    bedroc_lst = list(np.around(np.array(bedroc_lst), decimals=3))
    return bedroc_lst


class AlyModelML(object):
    def __init__(self, data_d, receptor_idx_d, **kwargs):
        self.y_true = data_d['y_true']
        self.y_pred = data_d['y_pred']
        self.scope = data_d['scope']
        self.sample_name = data_d['sample_name']
        self.receptor_idx_d = receptor_idx_d
        self.receptor_lst = list(receptor_idx_d.keys())
        logger.info('Analyzed results contain {} receptors, including: {}'.format(len(self.receptor_lst), self.receptor_lst))

        if ~((self.y_pred != 0) & (self.y_pred != 1)).any():
            # For the cases where the provided y_pred is binary value
            raise Exception("The generated y_pred is binary values, which requires additional analysis.")

        self.out_path = kwargs.get('out_path', None)
        if self.out_path:
            self._split_receptor_sorted()
            os.makedirs(self.out_path, exist_ok=True)

    def _split_receptor_sorted(self):
        """
        Sort the data based on the prediction, and split per target
        :return:
        """
        self.sorted_idx = np.argsort(self.y_pred)[::-1]  # In descending order
        self.sorted_y_pred, self.sorted_y_true, self.sorted_sample_name \
            = self.y_pred[self.sorted_idx], self.y_true[self.sorted_idx], self.sample_name[self.sorted_idx]

        self.full_pred_df = pd.DataFrame(
            data={'receptor': self.sorted_sample_name, 'y_true': self.sorted_y_true, 'y_pred': self.sorted_y_pred})
        self.full_pred_df_nosort = pd.DataFrame(
            data={'sampleID': self.sample_name,  'prediction': self.y_pred})
        self.per_receptor_pred_df = dict()

        # Split the prediction based on the receptor
        receptor_path = osp.join(self.out_path, '{}_receptors'.format(self.scope))
        if not osp.exists(receptor_path):
            os.makedirs(receptor_path)

        # Save the full prediction, sorted across receptors.
        self.full_pred_df.to_csv(osp.join(self.out_path, '{}_preds.csv'.format(self.scope)), index=False)
        self.full_pred_df_nosort.to_csv(osp.join(self.out_path, '{}_preds_nosort.csv'.format(self.scope)), index=False)

        # Save the prediction per receptor, sorted per receptor.
        for receptor in self.receptor_lst:
            pred_receptor_df = self.full_pred_df[self.full_pred_df['receptor'].str.contains(receptor)]
            self.per_receptor_pred_df[receptor] = pred_receptor_df
            csv_f_receptor = osp.join(receptor_path, '{}_preds.csv'.format(receptor))
            pred_receptor_df.to_csv(csv_f_receptor, index=False)

    def aly_auc(self):
        """
        Calculate the AUC for per target and average.
        :return:
        """
        accumulated_auc = 0.0
        auc_d = OrderedDict()

        for receptor_name, idx_lst in self.receptor_idx_d.items():
            receptor_y_true = self.y_true[idx_lst].astype(int)
            receptor_y_pred = self.y_pred[idx_lst]
            per_target_auc = metrics.roc_auc_score(receptor_y_true, receptor_y_pred)
            auc_d[receptor_name] = per_target_auc
            accumulated_auc += per_target_auc
        avg_auc = accumulated_auc / len(self.receptor_idx_d)

        auc_df = pd.DataFrame.from_dict(auc_d, orient='index', columns=['auc'])
        auc_df.reset_index(inplace=True)
        auc_df.rename({'index': 'receptor'}, axis='columns', inplace=True)
        auc_df.sort_values(by='auc', ascending=False, inplace=True)
        avg_row = pd.DataFrame({'receptor': 'Average', 'auc': avg_auc}, index=[0])
        auc_df = pd.concat([avg_row, auc_df], ignore_index=True)
        logger.info('AUC for {}\n{}'.format(self.scope, auc_df))

        if self.out_path:
            auc_csv = osp.join(self.out_path, self.scope + '_' + 'auc.csv')
            auc_df.to_csv(auc_csv, index=False)

    def aly_ef(self):
        ratio_lst = [3, 5, 10, 0.01, 0.02, 0.05, 0.1, 0.2]
        ef_df_col_name = ['receptor'] + ['ef-' + str(i) for i in ratio_lst]
        logger.info('EF data frame col names:{}'.format(ef_df_col_name))

        ef_df_lst = []
        for receptor in self.receptor_lst:
            receptor_pred_df = self.per_receptor_pred_df[receptor]

            # Cal ef for each receptor
            receptor_ef_lst = cal_ef(receptor_pred_df['y_true'].values, receptor_pred_df['y_pred'].values,
                                     ratio_lst, receptor_type=receptor)
            ef_df_lst.append(pd.DataFrame(data=[[receptor] + receptor_ef_lst], columns=ef_df_col_name))

        ef_df = pd.concat(ef_df_lst, ignore_index=True)
        ef_df = ef_df.sort_values(by=['ef-{}'.format(ratio_lst[0])], ascending=False)

        avg_ef_lst = list(np.around(ef_df.mean(axis=0).values, decimals=3))  # Cal average
        avg_df = pd.DataFrame(data=[['Average'] + avg_ef_lst], columns=ef_df_col_name)

        ef_df = pd.concat([avg_df, ef_df], ignore_index=True)
        ef_csv = osp.join(self.out_path, self.scope + '_' + 'ef.csv')
        ef_df.to_csv(ef_csv, index=False)

    def aly_bedroc(self):
        ratio_lst = [321.9, 160.9, 80.5, 53.6, 32.2, 20.0, 16.1]
        bedroc_df_col_name = ['receptor'] + ['alpha-' + str(i) for i in ratio_lst]

        bedroc_df_lst = []
        for receptor in self.receptor_lst:
            receptor_pred_df = self.per_receptor_pred_df[receptor]

            # Cal ef for each receptor
            receptor_bedroc_lst = cal_bedroc(receptor_pred_df['y_true'].values, receptor_pred_df['y_pred'].values,
                                             ratio_lst, receptor_type=receptor)
            bedroc_df_lst.append(pd.DataFrame(data=[[receptor] + receptor_bedroc_lst], columns=bedroc_df_col_name))

        bedrcd_df = pd.concat(bedroc_df_lst, ignore_index=True)
        bedrcd_df = bedrcd_df.sort_values(by=['alpha-{}'.format(ratio_lst[-1])], ascending=False)

        avg_bedrcd_df_lst = list(np.around(bedrcd_df.mean(axis=0).values, decimals=3))  # Cal average
        avg_df = pd.DataFrame(data=[['Average'] + avg_bedrcd_df_lst], columns=bedroc_df_col_name)

        bedrcd_df = pd.concat([avg_df, bedrcd_df], ignore_index=True)
        bedrcd_csv = osp.join(self.out_path, self.scope + '_' + 'bedroc.csv')
        bedrcd_df.to_csv(bedrcd_csv, index=False)


if __name__ == '__main__':
    pass
