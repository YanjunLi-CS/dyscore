#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
dataload_ml.py: 
"""

import os
import os.path as osp
import numpy as np
import pandas as pd
from collections import defaultdict

feat_dict = {
    0: 'Stable',
    1: 'MT',
    2: 'VDW',
    3: 'HM',
    4: 'RT',
    5: 'Match',
    6: 'Vina',
    7: 'RF3',
    8: 'NN',
    9: 'DSX',
    10: 'DSXA',
    11: 'Score2',
    12: 'Xscore',
    13: 'HB-HSPC'
}


class DataSet(object):
    def __init__(self, ds_path, mode, args, logger):
        self.mode = mode
        self.logger = logger

        self.pos_f = osp.join(ds_path, mode + '_pos.csv')
        self.neg_f = osp.join(ds_path, mode + '_neg.csv')

        self.pos_df = pd.read_csv(self.pos_f)
        self.neg_df = pd.read_csv(self.neg_f)

        self.merge_df = pd.concat([self.pos_df, self.neg_df], ignore_index=True)

        assert self.merge_df.columns[1] == 'Active', f'{merged_csv} 2nd column is not Active.'
        self.numerical = self.merge_df.iloc[:, 1:].to_numpy()   # col starts from "label"

        self.args = args
        self.sample_names = self.merge_df.iloc[:, 0]
        self.labels = self.numerical[:, 0]

        if self.args['feat_keep'] is None:
            if self.args['feat_remove'] is not None:
                self.feats = np.delete(self.numerical[:, 1:], self.args['feat_remove'], 1)
            else:
                self.feats = self.numerical[:, 1:]
        else:
            self.feats = self.numerical[:, 1:20]    # self.feats starts from "Score", ends by "Xscore"
            
            # HB+HSPC as 14th feature
            hb_hspc = np.reshape(self.numerical[:, 4] + self.numerical[:, 6], (-1, 1))
            self.feats = np.concatenate([self.feats, hb_hspc], axis=1)
            self.indices = list(set([int(num) for num in self.args['feat_keep']]))
            self.feats = self.feats[:, self.indices]

        if self.args['add_feat']:
            add_feat_idx = self.args['add_feat']
            if 27 in add_feat_idx:
                # convert binary feature to bit vector
                hex_feat = self.numerical[:, 27]
                hex_max_len = len(hex_feat[0])
                binary_max_len = 4 * hex_max_len
                binary_feat = [format(int(str(hex_str), 16), f'0{binary_max_len}b') for hex_str in hex_feat]
                vector_binary_feat = [[int(c) for c in binary_str] for binary_str in binary_feat]
                vector_binary_feat_np = np.array(vector_binary_feat)
                add_fest_idx2 = [idx for idx in add_feat_idx if idx != 27]  # Exclude the hex features
                self.feats = np.concatenate([self.feats, self.numerical[:, add_fest_idx2], vector_binary_feat_np], axis=1)
            else:
                self.feats = np.concatenate([self.feats, self.numerical[:, add_feat_idx]], axis=1)
            self.logger.info(f"Add additional features, Feats dim: {self.feats.shape}")

        self.receptor_idx_d = self._obtain_receptor_idx()

    def fetch(self):
        samples = {'feats': self.feats, 'labels': self.labels,
                   'sample_name': self.sample_names, "receptor_idx_d": self.receptor_idx_d}
        self.logger.info(f"Feats dim: {self.feats.shape}")
        return samples

    def __len__(self):
        return len(self.merge_df)

    def _obtain_receptor_idx(self):
        receptor_names = [sample_name.rpartition("_")[0] for sample_name in self.sample_names]
        unique_receptor_names = set(receptor_names)
        receptor_idx_d = defaultdict(list)

        for i, receptor_name in enumerate(receptor_names):
            receptor_idx_d[receptor_name].append(i)
        self.logger.info("{}: total receptors: {}".format(self.mode, len(unique_receptor_names)))
        return receptor_idx_d

    def _adjust_title_field(self, org_title, receptor_name):
        title = org_title.replace('_', '-')
        return f'{receptor_name}_{title}'


