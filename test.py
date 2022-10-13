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


if __name__ == "__main__":
    print(load(Root, path="config.yaml", prefix="CONFIG"))
