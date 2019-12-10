# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
import logging
import yaml
import git
import mlflow


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

    def __init__(self, filename=None, skip_timestamp=False, skip_git_info=False):
        if Config._instance is not None:
            raise Exception('This class is a singleton!')

        if filename is not None:
            LOGGER.info('load config at: %s', filename)
            self.filename = filename

            with open(filename, 'r') as f:
                self.conf = yaml.safe_load(f)
        else:
            self.conf = {}

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

    def mlflow_log_pararms(self, key=None):
        mlflow.log_params(self.flatten(key))
        return self

    def __str__(self):
        return 'filename:%s\nconf:%s' % (self.filename, self.conf)

    def __contains__(self, item):
        return item in self.conf

    def __getitem__(self, key, default_value=''):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value
