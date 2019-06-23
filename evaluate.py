# -*- coding: utf-8 -*-
import math

import six
import fire


def _ndcg(recs, gt):
    Q, S = 0.0, 0.0
    for u, seen in six.iteritems(gt):
        seen = list(set(seen))
        rec = recs.get(u, [])
        if not rec or len(seen) == 0:
            continue

        dcg = 0.0
        idcg = sum([1.0 / math.log(i + 2, 2) for i in range(min(len(seen), len(rec)))])
        for i, r in enumerate(rec):
            if r not in seen:
                continue
            rank = i + 1
            dcg += 1.0 / math.log(rank + 1, 2)
        ndcg = dcg / idcg
        S += ndcg
        Q += 1
    return S / Q


def _map(recs, gt, topn):
    n, ap = 0.0, 0.0
    for u, seen in six.iteritems(gt):
        seen = list(set(seen))
        rec = recs.get(u, [])
        if not rec or len(seen) == 0:
            continue

        _ap, correct = 0.0, 0.0
        for i, r in enumerate(rec):
            if r in seen:
                correct += 1
                _ap += (correct / (i + 1.0))
        _ap /= min(len(seen), len(rec))
        ap += _ap
        n += 1.0
    return ap / n


def _entropy_diversity(recs, topn):
    sz = float(len(recs)) * topn
    freq = {}
    for u, rec in six.iteritems(recs):
        for r in rec:
            freq[r] = freq.get(r, 0) + 1
    ent = -sum([v / sz * math.log(v / sz) for v in six.itervalues(freq)])
    return ent


def evaluate(recs_path, dev_path, topn=100):
    recs = {}
    target_users = set()
    for line in open(recs_path):
        tkns = line.strip().split()
        userid, rec = tkns[0], tkns[1:]
        target_users.add(userid)
        recs[userid] = rec

    gt = {}
    for line in open(dev_path):
        tkns = line.strip().split()
        if tkns[0] not in target_users:
            continue
        userid, seen = tkns[0], tkns[1:]
        gt[userid] = seen

    print('MAP@%s: %s' % (topn, _map(recs, gt, topn)))
    print('NDCG@%s: %s' % (topn, _ndcg(recs, gt)))
    print('EntDiv@%s: %s' % (topn, _entropy_diversity(recs, topn)))


if __name__ == '__main__':
    fire.Fire({'run': evaluate})
