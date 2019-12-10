# -*- coding: utf-8 -*-
# pylint: disable=arguments-differ, abstract-method
from __future__ import absolute_import
import logging

import mlflow
import torch


LOGGER = logging.getLogger(__name__)


class AverageMeter(torch.nn.Module):
    def __init__(self, *keys, use_mlflow=False):
        super(AverageMeter, self).__init__()
        self.step = 0
        self.use_mlflow = use_mlflow
        self.keys = keys
        self.reset()

    def reset(self, step=None, use_mlflow=False, mlflow_prefix=None):
        self.step = step if step is not None else self.step + 1

        if self.use_mlflow or use_mlflow:
            mlflow.log_metrics(self.get(prefix=mlflow_prefix), step=self.step)

        for key in self.keys:
            device = self._buffers[key].device if key in self._buffers else torch.device('cpu')
            self.register_buffer(key, torch.zeros(1, dtype=torch.float, device=device))
            self.register_buffer(key + '_count', torch.zeros(1, dtype=torch.int32, device=device))

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
