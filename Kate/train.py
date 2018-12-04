import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
from beat_aligned_feats import get_bttimbre

try:
    msd_code_path = '/Users/sw_k_jung/Google Drive/Cloud/CSE546/Project/helpers'
    sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))
    import hdf5_getters as GETTERS
except ImportError:
    print('cannot find file hdf5_getters.py')
    print('you must put MSongsDB/PythonSrc in your path or import it otherwise')
    raise

def getSamples(basedir):
    X, Y = [],[]
    feature_labels = ['segments_pitch',
                 'segments_timbre',
                 'segments_loudness_max',
                 'tempo']
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*.h5'))
        print(root, cnt)
        # apply function to all files
        for f in files :
#             try:
            h5 = GETTERS.open_h5_file_read(f)
            year = GETTERS.get_year(h5)
            if year == 0:
                continue
            bttimbre = get_bttimbre(h5)
            if bttimbre is None or year == 0:
                continue
            h5.close()
            X.append(bttimbre)
            Y.append(year)
            cnt+=1

            if cnt  > 10000:
                break
    return X, Y, feature_labels
if __name__ == '__main__':
    msd_subset_path = '/Users/sw_k_jung/Google Drive/Cloud/CSE546/Project/'
    msd_subset_data_path = '/Users/sw_k_jung/Google Drive/Cloud/CSE546/data_train'
    msd_subset_addf_path = os.path.join(msd_subset_path, 'helpers')
    msd_code_path = '/Users/sw_k_jung/Google Drive/Cloud/CSE546/Project/helpers'
    sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))

    X, Y, labels = getSamples(msd_subset_data_path)
    print(len(X), len(Y))