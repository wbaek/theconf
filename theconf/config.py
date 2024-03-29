# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import logging
from collections import namedtuple
import keyword
import yaml
import git


LOGGER = logging.getLogger(__name__)


class Config():
    _instance = None

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config()
        return Config._instance

    @staticmethod
    def get():
        return Config.get_instance()

    @staticmethod
    def clear():
        Config._instance = None

    def update_git_info(self):
        try:
            repo = git.Repo('./')
            remotes = [u for u in repo.remotes.origin.urls]
            if remotes:
                remote = remotes[0]
                branch = repo.active_branch.name
                commit = next(repo.iter_commits())
                hash_ = commit.hexsha
                comment = commit.message

                self.conf['_git'] = {
                    'remote': remote,
                    'branch': branch,
                    'commit': {
                        'hash': hash_,
                        'comment': comment
                    },
                    'status': {
                        'diff': [
                            {'type': diff.change_type, 'path': diff.b_path}
                            for diff in repo.index.diff(None)
                        ],
                        'untracked': repo.untracked_files
                    }
                }
        except Exception as e:
            LOGGER.debug('[update_git_info] %s:%s', type(e), str(e))
        return self

    def dump(self, filename=None):
        self.conf['_version'] += 1
        dump_string = yaml.dump(self.conf, default_flow_style=False)
        if filename is not None:
            with open(filename, 'w') as f:
                f.write(dump_string)
        return dump_string

    def __init__(self, filenames=[], skip_timestamp=True, skip_git_info=True):
        if Config._instance is not None:
            raise Exception('This class is a singleton!')

        self.conf = {}
        if filenames:
            filenames = filenames if isinstance(filenames, list) else [filenames]
            LOGGER.info('load config at: %s', ','.join(filenames))
            self.filenames = filenames

            for filename in filenames:
                with open(filename, 'r') as f:
                    # self.conf = yaml.safe_load(f)
                    update_dict(self.conf, yaml.safe_load(f))

        if '_version' not in self.conf:
            self.conf['_version'] = 1
        if not skip_timestamp:
            self.conf['_timestamp'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        if not skip_git_info:
            self.update_git_info()

        Config._instance = self
        self.get = self._instance_get

    def _instance_get(self, key, default_value=''):
        return self.conf.get(key, default_value)

    def _flatten(self, keys, values):
        flatten_list = []
        if isinstance(values, dict):
            for key, value in values.items():
                if key.startswith('_'):
                    continue
                v = self._flatten(keys + [key], value)
                flatten_list += v
        elif isinstance(values, list):
            for key, value in enumerate(values):
                v = self._flatten(keys + [str(key)], value)
                flatten_list += v
        else:
            v = [('-'.join(keys), values)]
            flatten_list += v
        return flatten_list

    def flatten(self, key=None):
        if key is not None:
            return dict(self._flatten([], self.conf[key]))
        return dict(self._flatten([], self.conf))

    def __str__(self):
        return 'filenames:%s\nconf:%s' % (','.join(self.filenames), self.conf)

    def __contains__(self, item):
        return item in self.conf

    def __getitem__(self, key, default_value=''):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

    def __getattr__(self, key):
        tuples = dict_to_namedtuple('conf', self.conf)
        return getattr(tuples, key)


def update_dict(dict1, dict2):
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value
        elif isinstance(value, dict):
            update_dict(dict1[key], value)
        else:
            dict1[key] = value


def dict_to_namedtuple(typename, data):
    keys = [k for k in data.keys() if not k.startswith('_') and k not in keyword.kwlist]
    return namedtuple(typename, keys)(
        *(dict_to_namedtuple(typename + '_' + k, v) if isinstance(v, dict) else v for k, v in data.items() if k in keys)
    )
