# -*- coding: utf-8 -*-
import os
import pytest

from theconf import Config
from theconf import ConfigArgumentParser

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'datas',
)

@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'arguments.yaml')
)
def test_arguments_simple(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0]])

    assert args.foo == 'test'
    assert args.bar == 1234
    assert Config.get_instance()['foo'] == 'test'
    assert Config.get_instance()['bar'] == 1234

    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value'])

    assert args.foo == 'value'
    assert args.bar == 1234
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 1234

    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value', '--bar', '4321'])

    assert args.foo == 'value'
    assert args.bar == 4321
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 4321

    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    parser.add_argument('--baz', type=float, default=0.1)
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value', '--bar', '4321'])

    assert args.foo == 'value'
    assert args.bar == 4321
    assert args.baz == 0.1
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 4321
    assert Config.get_instance()['baz'] == 0.1

    Config.clear()


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'arguments.yaml')
)
def test_arguments_boolean(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0], '--var', 'true'])
    
    assert args.var == True
    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0], '--var', 'false'])

    assert args.var == False
    Config.clear()


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'arguments.yaml')
)
def test_arguments_invalid(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(filename=filenames[0])
    with pytest.raises(SystemExit) as e:
        _ = parser.parse_args(args=['-c', filenames[0], '--baz', 'test'])
    # pytest: error: unrecognized arguments: --baz test

    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    with pytest.raises(SystemExit) as e:
        _ = parser.parse_args(args=['-c', filenames[0], '--bar', 'test'])
    # pytest: error: argument --bar: invalid int value: 'test'

    Config.clear()

    parser = ConfigArgumentParser(filename=filenames[0])
    with pytest.raises(Exception) as e:
        parser.add_argument('--foo', type=int, default=1)
    assert str(e.value) in ['argument --foo: conflicting option string: --foo', 'argument --foo: conflicting option string(s): --foo']

    Config.clear()


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'arguments_complex.yaml')
)
def test_arguments_complex(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=['-c', filenames[0]])
    _ = args

    Config.clear()

    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(filename=filenames[0])
    args = parser.parse_args(args=[])  # -c 옵션이 없어도 filename이 명시적으로 있는 경우 parse 가능해야 함
    _ = args

    Config.clear()

    assert True


@pytest.mark.filterwarnings("ignore:MarkInfo")
@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'configs', 'arguments.yaml')
)
def test_arguments_simple_lazy(datafiles):
    filenames = [str(f) for f in datafiles.listdir()]
    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[0]])

    assert args.foo == 'test'
    assert args.bar == 1234
    assert Config.get_instance()['foo'] == 'test'
    assert Config.get_instance()['bar'] == 1234

    Config.clear()

    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value'])

    assert args.foo == 'value'
    assert args.bar == 1234
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 1234

    Config.clear()

    parser = ConfigArgumentParser(lazy=True)
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value', '--bar', '4321'])

    assert args.foo == 'value'
    assert args.bar == 4321
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 4321

    Config.clear()

    parser = ConfigArgumentParser(lazy=True)
    parser.add_argument('--baz', type=float, default=0.1)
    args = parser.parse_args(args=['-c', filenames[0], '--foo', 'value', '--bar', '4321'])

    assert args.foo == 'value'
    assert args.bar == 4321
    assert args.baz == 0.1
    assert Config.get_instance()['foo'] == 'value'
    assert Config.get_instance()['bar'] == 4321
    assert Config.get_instance()['baz'] == 0.1

    Config.clear()


