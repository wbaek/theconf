# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import argparse

from .config import Config

LOGGER = logging.getLogger(__name__)


class ConfigArgumentParser(argparse.ArgumentParser):
    def __init__(self, filename=None, **kwargs):
        super(ConfigArgumentParser, self).__init__(add_help=False, **kwargs)
        self.add_argument('-c', '--config', required=(not filename), help='set config filepath')

        parsed, _ = self.parse_known_args(args=None if not filename else ['-c', filename])
        Config(parsed.config)

        self.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
        for key, value in Config.get_instance().conf.items():
            self._add_argument(key, value)

    def _add_argument(self, key, value, prefix=None):
        if key.startswith('_'):
            return
        key = key if prefix is None else prefix + '-' + key
        if key in self._option_string_actions:
            LOGGER.error('%s already exist arguments', key)
        elif isinstance(value, dict):
            for k, v in value.items():
                self._add_argument(k, v, key)
        elif isinstance(value, list):
            if value:
                self.add_argument('--' + key, type=type(value[0]), nargs='*', default=value, help='set ' + type(value[0]).__name__ + ' list (default:' + str(value) + ')')
            else:
                self.add_argument('--' + key, nargs='*', default=value, help='set list (default:' + str(value) + ')')
        else:
            self.add_argument('--' + key, type=type(value), default=value, help='set ' + type(value).__name__ + ' value (default:' + str(value) + ')')

    def _set_argument_from_conf(self, parsed_args, key, value, prefix=None):
        key = key if prefix is None else '_'.join([prefix, key])
        used = ['conf']
        if isinstance(value, dict):
            rv = {}
            for k, v in value.items():
                rv[k], local_used = self._set_argument_from_conf(parsed_args, k, v, key)
                used += local_used
        else:
            used.append(key)
            rv = getattr(parsed_args, key)
        return rv, used

    def _set_argument_from_args(self, keys, value, rv=None):
        rv = {} if rv is None else rv
        if len(keys) == 1:
            rv[keys[0]] = value
        else:
            rv[keys[0]] = self._set_argument_from_args(keys[1:], value, rv.get(keys[0], {}))
        return rv

    def parse_args(self, args=None, namespace=None):
        parsed_args = super(ConfigArgumentParser, self).parse_args(args, namespace)

        used = []
        for key, value in Config.get_instance().conf.items():
            if key.startswith('_'):
                continue
            Config.get_instance()[key], local_used = self._set_argument_from_conf(parsed_args, key, value)
            used += local_used

        for key, value in parsed_args.__dict__.items():
            if key in used:
                continue
            splited_keys = key.split('_')
            Config.get_instance().conf = self._set_argument_from_args(splited_keys, value, Config.get_instance().conf)

        return parsed_args
