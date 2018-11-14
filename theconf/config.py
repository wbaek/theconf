# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import subprocess
import logging
import yaml


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
            remote = subprocess.check_output(
                'git remote -v | grep origin | grep fetch',
                shell=True,
                stderr=subprocess.PIPE
            ).decode('utf-8').replace('origin\t', '').replace(' (fetch)\n', '')
            if remote:
                branch_raw = subprocess.check_output(
                    'git branch -v | grep "*"',
                    shell=True
                ).decode('utf-8')[2:].split(' ')
                if branch_raw:
                    branch, hash_, comment = branch_raw[0], branch_raw[1], ' '.join(branch_raw[2:])
                    status = [line.strip() for line in subprocess.check_output('git status -s', shell=True).decode('utf-8').split('\n') if line.strip()]
                    self.conf['git'] = {'remote': remote, 'branch': branch, 'hash': hash_, 'comment': comment, 'status': status}
        except Exception:
            pass
        return self

    def dump(self, filename=None):
        dump_string = yaml.dump(self.conf, default_flow_style=False)
        if filename is not None:
            with open(filename, 'w') as f:
                f.write(dump_string)
        return dump_string

    def __init__(self, filename=None, skip_git_info=False):
        if Config._instance is not None:
            raise Exception('This class is a singleton!')

        if filename is not None:
            LOGGER.info('load config at: %s', filename)
            self.filename = filename

            with open(filename, 'r') as f:
                self.conf = IncludeLoader.load(f, IncludeLoader)
        else:
            self.conf = {}

        if not skip_git_info:
            self.update_git_info()
        Config._instance = self

    def __str__(self):
        return 'filename:%s\nconf:%s' % (self.filename, self.conf)

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

# https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another
# https://stackoverflow.com/questions/44910886/pyyaml-include-file-and-yaml-aliases-anchors-references
class IncludeLoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(IncludeLoader, self).__init__(stream)
        IncludeLoader.add_constructor('!include', IncludeLoader.include)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node)) # support for relative path
        with open(filename, 'r') as f:
            return IncludeLoader.load(f, IncludeLoader, self)

    def compose_document(self):
        LOGGER.info('compose_document')
        self.get_event()
        node = self.compose_node(None, None)
        LOGGER.info('compose_document node: %s', node)

        self.get_event()
        LOGGER.info('compose_document anchors: %s', self.anchors)

        # self.anchors = {}
        return node

    @staticmethod
    def load(stream, loader, master=None):
        loader_ = loader(stream)
        if master is not None:
            loader_.anchors = master.anchors
            LOGGER.info('load anchors: %s', master.anchors)
        try:
            return loader_.get_single_data()
        finally:
            loader_.dispose()
