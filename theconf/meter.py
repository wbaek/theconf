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

    def log(self, prefix, step=None, tensorboard=True, mlflow=False):
        step = step if step is not None else self.step

        if self.tensorboard_path and tensorboard:
            for key, value in self.get().items():
                self.writers[prefix].add_scalar('metrics/%s' % key, value, global_step=step)

        if mlflow:
            module_mlflow.log_metrics(self.get(prefix=prefix), step=step)

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

    def get(self, prefix=None):
        if prefix is not None:
            return {prefix + '_' + key: self.__getitem__(key) for key in self.keys}
        return {key: self.__getitem__(key) for key in self.keys}

    def __getitem__(self, key):
        if key not in self._buffers:
            return 0.0
        if self._buffers[key + '_count'] == 0:
            return 0.0
        return self._buffers[key].item() / self._buffers[key + '_count'].item()

    def __str__(self):
        return ', '.join(['%s:%.3f' % (str(key), self.__getitem__(key)) for key in self.keys])
