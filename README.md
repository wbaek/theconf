# theconf
[![CodeFactor](https://www.codefactor.io/repository/github/wbaek/theconf/badge)](https://www.codefactor.io/repository/github/wbaek/theconf)
[![CircleCI](https://circleci.com/gh/wbaek/theconf.svg?style=svg)](https://circleci.com/gh/wbaek/theconf)
[![Waffle.io - Columns and their card count](https://badge.waffle.io/wbaek/theconf.svg?columns=all)](https://waffle.io/wbaek/theconf)

Python Package for Managing Configurations

python module 전역에서 쉽게 활용 가능한 global config util및 config를 쉽고 안전하게(실수를 예방하며) 활용가능한 Config전용 ArgumentParser확장 모듈

* sample_config.yaml
```yaml
value: string
foo:
    bar: text
    baz: 123
data:
    string: text
    int: 1
    float: 0.1
    list: [1, 2, 3]
    dict:
        from: to
```

## Config

Config는 main문에서 yaml 파일로 객체를 생성하고 어디서나 `Config.get_instatnce()`로 객체를 가져다 쓸 수 있다. (singleton pattern)

```python
>>> from theconf import Config
>>> _ = Config('sample_config.yaml')
>>> Config.get_instance()['value']
'string'
>>> Config.get_instance()['foo']
{'bar': 'text', 'baz': 123}
>>> Config.get_instance()['data']['float']
0.1
>>> _ = Config('sample_config.yaml')
Exception: This class is a singleton!
```

### shorten

```python
>>> from theconf import Config as C
>>> _ = Config('sample_config.yaml')
>>> C.get()['value']
'string'
```

### git info

git 정보를 가져 올 수 있을때 config에 정보를 기본으로 가지고 있는다.

```python
{
    'git': {
        'remote': 'https://github.com/wbaek/theconf.git',
        'branch': 'master',
        'hash': 'db8d899',
        'comment': 'add basic theconf\n',
        'status': ['M theconf/argument_parser.py']
    }
}
```

## ConfigArgumentParser

Config에 있는 변수를 실행시점에 변경하거나 추가로 정의하고 싶을때 사용한다.
기존에 정의되어 있는 Config에 값을 overwrite하고 싶을때 --key value 형식으로 입력하면되고 기본적인 key의 존재여부 및 value의 type을 확인한다.
ArgumentParser를 상속받아 구현하여 기본적으로 ArgumentParser와 사용법이 동일하다.

* sample_config.py
```python
from theconf import Config, ConfigArgumentParser
parser = ConfigArgumentParser(conflict_handler='resolve')
parser.add_argument('--added', type=str, default='NOT_EXIST_CONFIG', help='ADDED_FROM_ARGPARSER')
parser.add_argument('--dump', type=str, default=None, help='config dump filepath')
parsed_args = parser.parse_args()
print(parsed_args)
print(Config.get_instance())

if parsed_args.dump:
    Config.get_instance().dump(parsed_args.dump)
```

```bash
$ python sample_config.py -h
usage: sample_config.py -c CONFIG
sample_config.py: error: the following arguments are required: -c/--config

$ python simple_config.py -c sample_config.yaml -h
usage: sample.py -c CONFIG [-h] [--value VALUE] [--foo-bar FOO_BAR]
                 [--foo-baz FOO_BAZ] [--data-string DATA_STRING]
                 [--data-int DATA_INT] [--data-float DATA_FLOAT]
                 [--data-list [DATA_LIST [DATA_LIST ...]]]
                 [--data-dict-from DATA_DICT_FROM] [--added ADDED]
                 [--dump DUMP]

optional arguments:
  -c CONFIG, --config CONFIG
                        set config filepath
  -h, --help            show this help message and exit
  --value VALUE         set str value (default:string)
  --foo-bar FOO_BAR     set str value (default:text)
  --foo-baz FOO_BAZ     set int value (default:123)
  --data-string DATA_STRING
                        set str value (default:text)
  --data-int DATA_INT   set int value (default:1)
  --data-float DATA_FLOAT
                        set float value (default:0.1)
  --data-list [DATA_LIST [DATA_LIST ...]]
                        set int list (default:[1, 2, 3])
  --data-dict-from DATA_DICT_FROM
                        set str value (default:to)
  --added ADDED         ADDED_FROM_ARGPARSER
  --dump DUMP           config dump filepath

$ python sample_config.py -c sample_config.yaml
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_from='to', data_float=0.1, data_int=1, data_list=[1, 2, 3], data_string='text', dump=None, foo_bar='text', foo_baz=123, value='string')
filename:sample_config.yaml
conf:{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 0.1, 'list': [1, 2, 3], 'dict': {'from': 'to'}}, 'config': 'sample_config.yaml', 'added': 'NOT_EXIST_CONFIG', 'dump': None}

$ python sample_config.py -c sample_config.yaml --data-float 10
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_from='to', data_float=10.0, data_int=1, data_list=[1, 2, 3], data_string='text', dump=None, foo_bar='text', foo_baz=123, value='string')
filename:sample_config.yaml
conf:{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 10.0, 'list': [1, 2, 3], 'dict': {'from': 'to'}}, 'config': 'sample_config.yaml', 'added': 'NOT_EXIST_CONFIG', 'dump': None}

$ python sample_config.py -c sample_config.yaml --data-float 10 --dump here.yaml
Namespace(added='NOT_EXIST_CONFIG', config='sample_config.yaml', data_dict_from='to', data_float=10.0, data_int=1, data_list=[1, 2, 3], data_string='text', dump='here.yaml', foo_bar='text', foo_baz=123, value='string')
filename:sample_config.yaml
conf:{'value': 'string', 'foo': {'bar': 'text', 'baz': 123}, 'data': {'string': 'text', 'int': 1, 'float': 10.0, 'list': [1, 2, 3], 'dict': {'from': 'to'}}, 'config': 'sample_config.yaml', 'added': 'NOT_EXIST_CONFIG', 'dump': 'here.yaml'}

$ cat here.yaml
added: NOT_EXIST_CONFIG
config: sample_config.yaml
data:
  dict: {from: to}
  float: 10.0
  int: 1
  list: [1, 2, 3]
  string: text
dump: here.yaml
foo: {bar: text, baz: 123}
value: string

$ python sample_config.py -c sample_config.yaml --not-exists
usage: sample_config.py -c CONFIG [-h] [--value VALUE] [--foo-bar FOO_BAR]
                        [--foo-baz FOO_BAZ] [--data-string DATA_STRING]
                        [--data-int DATA_INT] [--data-float DATA_FLOAT]
                        [--data-list [DATA_LIST [DATA_LIST ...]]]
                        [--data-dict-from DATA_DICT_FROM] [--added ADDED]
                        [--dump DUMP]
sample_config.py: error: unrecognized arguments: --not-exists
```
