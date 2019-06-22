# -*- coding: utf-8 -*-
import os
import random

import six
import fire
import mmh3
import tqdm

from util import iterate_data_files


def groupby(from_dtm, to_dtm, tmp_dir, out_path, num_chunks=10):
    from_dtm, to_dtm = map(str, [from_dtm, to_dtm])
    fouts = {idx: open(os.path.join(tmp_dir, str(idx)), 'w')
             for idx in range(num_chunks)}
    files = sorted([path for path, _ in iterate_data_files(from_dtm, to_dtm)])
    for path in tqdm.tqdm(files, mininterval=1):
        for line in open(path):
            user = line.strip().split()[0]
            chunk_index = mmh3.hash(user, 17) % num_chunks
            fouts[chunk_index].write(line)

    map(lambda x: x.close(), fouts.values())
    with open(out_path, 'w') as fout:
        for chunk_idx in fouts.keys():
            _groupby = {}
            chunk_path = os.path.join(tmp_dir, str(chunk_idx))
            for line in open(chunk_path):
                tkns = line.strip().split()
                userid, seen = tkns[0], tkns[1:]
                _groupby.setdefault(userid, []).extend(seen)
            os.remove(chunk_path)
            for userid, seen in six.iteritems(_groupby):
                fout.write('%s %s\n' % (userid, ' '.join(seen)))


def sample_users(data_path, out_path, num_users):
    users = [data.strip().split()[0] for data in open(data_path)]
    random.shuffle(users)
    users = users[:num_users]
    with open(out_path, 'w') as fout:
        fout.write('\n'.join(users))


if __name__ == '__main__':
    fire.Fire({'groupby': groupby,
               'sample_users': sample_users})
