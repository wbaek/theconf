# -*- coding: utf-8 -*-
import os
import pytest

from theconf.config import Config
from theconf import ConfigArgumentParser


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'datas',
)


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'basic.yaml'),
    os.path.join(FIXTURE_DIR, 'configs', 'basic2.yaml')
)
def test_config(datafiles):
    filenames = [str(f) for f in datafiles.listdir(sort=True)]
    print(filenames)
    config = Config(filenames[0], skip_timestamp=True, skip_git_info=True)

    assert config['_version'] == 1

    assert config['foo']['bar'] == 1
    assert config['foo']['baz'] == 2
    assert 'qux' not in config['foo']
    Config.clear()

    config = Config(filenames[1], skip_timestamp=True, skip_git_info=True)

    assert config['_version'] == 1

    assert config['foo']['baz'] == 3
    assert config['foo']['qux'] == 4
    assert 'bar' not in config['foo']
    Config.clear()

    config = Config(filenames, skip_timestamp=True, skip_git_info=True)

    assert config['_version'] == 1

    assert config['foo']['bar'] == 1
    assert config['foo']['baz'] == 3
    assert config['foo']['qux'] == 4
    Config.clear()



@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'basic.yaml'),
    os.path.join(FIXTURE_DIR, 'configs', 'basic2.yaml')
)
def test_arguments(datafiles):
    filenames = [str(f) for f in datafiles.listdir(sort=True)]
    print(filenames)

    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[0]])

    assert args.foo_bar == 1
    assert args.foo_baz == 2
    assert Config.get_instance()['foo']['bar'] == 1
    assert Config.get_instance()['foo']['baz'] == 2
    assert 'qux' not in Config.get_instance()['foo']
    Config.clear()

    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[1]])

    assert args.foo_baz == 3
    assert args.foo_qux == 4
    assert Config.get_instance()['foo']['baz'] == 3
    assert Config.get_instance()['foo']['qux'] == 4
    assert 'bar' not in Config.get_instance()['foo']
    Config.clear()

    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[0], filenames[1]])

    assert args.foo_bar == 1
    assert args.foo_baz == 3
    assert args.foo_qux == 4
    assert Config.get_instance()['foo']['bar'] == 1
    assert Config.get_instance()['foo']['baz'] == 3
    assert Config.get_instance()['foo']['qux'] == 4
    Config.clear()
