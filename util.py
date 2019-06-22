# -*- coding: utf-8 -*-
import os
import config as conf


def iterate_data_files(from_dtm, to_dtm):
    from_dtm, to_dtm = map(str, [from_dtm, to_dtm])
    read_root = os.path.join(conf.data_root, 'read')
    for fname in os.listdir(read_root):
        if len(fname) != len('2018100100_2018100103'):
            continue
        if from_dtm != 'None' and from_dtm > fname:
            continue
        if to_dtm != 'None' and fname > to_dtm:
            continue
        path = os.path.join(read_root, fname)
        yield path, fname
