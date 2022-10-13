from dataclasses import dataclass


from dataclass_config import load


@dataclass
class Y:
    a: str
    b: int


@dataclass
class X:
    y: Y
    c: str
    a: int = 11
    b: int = 12


if __name__ == "__main__":
    print(load(X, path="cfg.yaml", prefix="SVC"))
