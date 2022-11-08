# DCLoader

Load a data class from diffrent sources.
Including: Environment Variables, YAML files, and, ....

main.py
``` python
from dataclasses import dataclass

from dcloader import EnvLoader, Loader, YAMLLoader


@dataclass
class Leaf:
    node: str


@dataclass
class Root:
    leaf: Leaf
    node: int


loader = Loader([EnvLoader(prefix="CONFIG"), YAMLLoader("config.yaml")])
cfg = loader.load(Root)
print(cfg)
```

config.yaml
``` yaml
leaf:
  node: value
```

``` sh
$ export CONFIG_NODE=12
$ python main.py
```
