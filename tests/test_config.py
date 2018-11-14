# -*- coding: utf-8 -*-
import os
import pytest

from theconf.config import Config

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'datas',
)


def test_singletone():
    conf1 = Config.get_instance()
    conf2 = Config.get_instance()
    assert conf1 == conf2
    Config.clear()

@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'basic.yaml')
)
def test_singletone2(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    _ = Config(filenames[0])
    with pytest.raises(Exception) as _:
        _ = Config(filenames[0])
    Config.clear()

@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'basic.yaml')
)
def test_update_and_dump(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    config = Config(filenames[0], skip_git_info=True)

    assert config['foo']['bar'] == 1
    assert config['foo']['baz'] == 2

    config['foo']['bar'] = {'test': 10}
    config['foo']['baz'] = 3
    assert config['foo']['bar']['test'] == 10
    assert config['foo']['baz'] == 3

    yaml_string = config.dump()
    assert yaml_string == 'foo:\n  bar:\n    test: 10\n  baz: 3\n'

    config.dump(filenames[0])

    Config.clear()

    config = Config(filenames[0])
    assert config['foo']['bar']['test'] == 10
    assert config['foo']['baz'] == 3
    Config.clear()
