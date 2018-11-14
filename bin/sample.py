# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from theconf import Config as C
from theconf import ConfigArgumentParser

if __name__ == '__main__':
    parser = ConfigArgumentParser(conflict_handler='resolve')
    parser.add_argument('--added', type=str, default='NOT_EXIST_CONFIG', help='ADDED_FROM_ARGPARSER')
    parser.add_argument('--dump', type=str, default=None, help='config dump filepath')
    parsed_args = parser.parse_args()
    print(parsed_args)
    print(C.get().dump())

    if parsed_args.dump:
        C.get().dump(parsed_args.dump)
        print('dumped at', parsed_args.dump)
