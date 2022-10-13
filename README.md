# Dataclass Loader

Load a data class from a ymal file and environment.

test.py
``` py
from dataclasses import dataclass


from dataclass_config import load


@dataclass
class B:
    a: str
    b: int
    c: int
    d: int = 24


@dataclass
class Root:
    a: str
    b: B
    c: int
    d: int = 4


cfg = load(Root, path="config.yaml", prefix="CONFIG")
print(cfg)
```

config.cfg
``` yaml
b:
  c: 23
c: 13
```

``` sh
$ export CONFIG_A=a
$ export CONFIG_B_A=b_a
$ export CONFIG_B_B=22
$ python test.py
```
