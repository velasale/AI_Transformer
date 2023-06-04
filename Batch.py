# Code from SamLynnEvans

import torch
from torchtext import data, datasets
import numpy as np
from torch.autograd import Variable


def nopeak_mask(size, opt):
    np_mask = np.triu(np.ones((1, size, size)), k=1).astype('uint8')
    np_mask = Variable(torch.from_numpy(np_mask == 0).to(opt.device))
    return np_mask


def create_masks(src, trg, opt):
    src_mask = (src != opt.src_pad).unsqueeze(-2).to(opt.device)

    if trg is not None:
        trg_mask = (trg != opt.trg_pad).unsqueeze(-2).to(opt.device)
        size = trg.size(1)  # get seq_len for matrix
        np_mask = nopeak_mask(size, opt).to(opt.device)
        trg_mask = trg_mask & np_mask

    else:
        trg_mask = None

    return src_mask, trg_mask


# class MyIterator(data.Iterator):
#
#     def create_batches(self):
#         if self.train:
#             def pool(d, random_shuffler):
#                 for p in data.batch(d, self.batch_size * 100):
#                     p_batch = data.batch(
#                         sorted(p, key=self.sort_key),
#                         self.batch_size, self.batch_size_fn)
#                     for b in random_shuffler(list(p_batch)):
#                         yield b
#
#             self.batches = pool(self.data(), self.random_shuffler)
#
#         else:
#             self.batches = []
#             for b in data.batch(self.data(), self.batch_size,
#                                 self.batch_size_fn):
#                 self.batches.append(sorted(b, key=self.sort_key))


global max_src_in_batch, max_tgt_in_batch


def batch_size_fn(new, count, sofar):
    """
    Keep augmenting batch and calulate total number of tokens + padding
    :param new:
    :param count:
    :param sofar:
    :return:
    """
    global max_src_in_batch, max_tgt_in_batch

    if count == 1:
        max_src_in_batch = 0
        max_tgt_in_batch = 0
    max_src_in_batch = max(max_src_in_batch, len(new.src))
    max_tgt_in_batch = max(max_tgt_in_batch, len(new.trg) + 2)
    src_elements = count * max_src_in_batch
    tgt_elements = count * max_tgt_in_batch
    return(src_elements, tgt_elements)