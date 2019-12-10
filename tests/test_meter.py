# -*- coding: utf-8 -*-
import os
import sys
import pytest

import torch

from theconf.meter import AverageMeter

def test_average_meta_to_device():
    if torch.cuda.is_available():
        meter = AverageMeter('key1', 'key2')
        assert meter._buffers['key1'].device == torch.device('cpu')
        assert meter._buffers['key2'].device == torch.device('cpu')

        meter = meter.to(device=torch.device('cuda', 0))
        assert meter._buffers['key1'].device == torch.device('cuda', 0)
        assert meter._buffers['key2'].device == torch.device('cuda', 0)


def test_average_meta_single():
    meter = AverageMeter('key1', 'key2')
    meter.update('key1', 2 * torch.ones(1))
    meter.update('key1', 3 * torch.ones(1))

    meter.update('key2', 5 * torch.ones(1))

    assert meter['key1'] == 2.5
    assert meter['key2'] == 5


def test_average_meta_count():
    meter = AverageMeter('key1', 'key2')
    meter.update('key1', 2 * torch.ones(1), n=1)
    meter.update('key1', 4 * torch.ones(1), n=3)

    meter.update('key2', 5 * torch.ones(1), n=5)

    assert meter['key1'] == 3.5
    assert meter['key2'] == 5


def test_average_meta_dict():
    meter = AverageMeter('key1', 'key2')
    meter.updates({
        'key1': 2 * torch.ones(1),
        'key2': 5 * torch.ones(1),
    })
    meter.updates({
        'key1': 3 * torch.ones(1),
    })

    assert meter['key1'] == 2.5
    assert meter['key2'] == 5


def test_average_meta_str():
    meter = AverageMeter('key1', 'key2')
    meter.updates({
        'key1': 2 * torch.ones(1),
        'key2': 5 * torch.ones(1),
    })
    meter.updates({
        'key1': 3 * torch.ones(1),
    })

    assert str(meter) == 'key1:2.500, key2:5.000'


def test_average_meta_not_exist_key():
    meter = AverageMeter('key1', 'key2')
    assert meter['not_exists'] == 0.0

