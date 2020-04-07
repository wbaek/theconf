# -*- coding: utf-8 -*-
# pylint: disable=arguments-differ, abstract-method
from __future__ import absolute_import
import os
import logging

import mlflow as module_mlflow
import torch
from torch.utils.tensorboard import SummaryWriter


LOGGER = logging.getLogger(__name__)


class AverageMeter(torch.nn.Module):
    def __init__(self, *keys, tensorboard_path=None, prefixs=['train', 'valid']):
        super(AverageMeter, self).__init__()
        self.step = 0
        self.keys = keys
        self.reset()

        self.tensorboard_path = tensorboard_path
        if tensorboard_path:
            self.writers = {prefix: SummaryWriter(os.path.join(tensorboard_path, prefix)) for prefix in prefixs}
        else:
            self.writers = {}

    def reset(self, step=None):
        self.step = step if step is not None else self.step + 1

        for key in self.keys:
            device = self._buffers[key].device if key in self._buffers else torch.device('cpu')
            self.register_buffer(key, torch.zeros(1, dtype=torch.float, device=device))
            self.register_buffer(key + '_count', torch.zeros(1, dtype=torch.int32, device=device))

    def log(self, prefix, step=None, keep_best_keys=[], tensorboard=True, mlflow=False):
        step = step if step is not None else self.step

        for key in keep_best_keys:
            if key not in self._buffers:
                continue
            best_key = key + '_best'
            device = self._buffers[key].device if key in self._buffers else torch.device('cpu')
            last_value = self._buffers[best_key] if best_key in self._buffers else torch.zeros(1, dtype=torch.float, device=device)
            last_count = self._buffers[best_key + '_count'] if best_key in self._buffers else torch.zeros(1, dtype=torch.float, device=device)

            value = max(last_value, self._buffers[key])
            count = max(last_count, self._buffers[key + '_count'])

            self.register_buffer(best_key, value)
            self.register_buffer(best_key + '_count', count)

        if self.tensorboard_path and tensorboard:
            for key, value in self.get(with_best=True).items():
                self.writers[prefix].add_scalar('metrics/%s' % key, value, global_step=step)

        if mlflow:
            module_mlflow.log_metrics(self.get(prefix=prefix), step=step)

    def close(self, mlflow=False):
        for prefix, writer in self.writers.items():
            writer.flush()
            writer.close()
        if mlflow:
            module_mlflow.end_run()

    def update(self, key, value, n=1):
        if isinstance(value, torch.Tensor):
            value = value.detach()

        self._buffers[key] += value * n
        self._buffers[key + '_count'] += n
        return self

    def updates(self, dictionary, n=1):
        for key, value in dictionary.items():
            self.update(key, value, n)
        return self

    def get(self, prefix=None, with_best=False):
        keys = [key for key in self._buffers.keys() if '_count' not in key]
        if not with_best:
            keys = [key for key in keys if '_best' not in key]
        if prefix is not None:
            return {prefix + '_' + key: self.__getitem__(key) for key in keys}
        return {key: self.__getitem__(key) for key in keys}

    def __getitem__(self, key):
        if key not in self._buffers:
            return 0.0
        if self._buffers[key + '_count'] == 0:
            return 0.0
        return self._buffers[key].item() / self._buffers[key + '_count'].item()

    def __str__(self, with_best=False):
        return ', '.join(['%s:%.4f' % (str(key), value) for key, value in self.get(with_best=with_best).items()])
