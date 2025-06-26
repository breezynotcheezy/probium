import json
from dataclasses import dataclass, asdict

class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def model_dump(self):
        out = {}
        for k, v in self.__dict__.items():
            if isinstance(v, BaseModel):
                out[k] = v.model_dump()
            elif isinstance(v, list):
                out[k] = [i.model_dump() if isinstance(i, BaseModel) else i for i in v]
            else:
                out[k] = v
        return out

    def model_dump_json(self):
        return json.dumps(self.model_dump())

    @classmethod
    def model_validate_json(cls, raw: str):
        return cls(**json.loads(raw))

    def model_copy(self, deep: bool = False):
        return self.__class__(**self.__dict__)

def Field(*, ge=None, le=None, default=None):
    return default

ConfigDict = dict
