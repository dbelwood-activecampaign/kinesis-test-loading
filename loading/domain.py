from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from json import dumps
from typing import Any, Dict, Mapping, NewType, Union


AccountId = NewType('AccountId', int)


class EventType(Enum):
    event_a = 'A'
    event_b = 'B'
    event_c = 'C'


@dataclass
class Record:
    partition_key: str
    data: bytes
    explicit_hash_key: Union[str, None] = None
    sequence_number: Union[str, None] = None


class StreamSendable(ABC):
    @abstractmethod
    def partition_key(self) -> str:
        pass

    @abstractmethod
    def data(self) -> bytes:
        pass

    def to_record(self) -> Record:
        return Record(self.partition_key(), self.data())


class StreamSendableDataClass(StreamSendable):
    def data(self: 'StreamSendableDataClass') -> bytes:
        return bytes(dumps(self.to_dict()), 'utf8')

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VisitInfo:
    email: str


@dataclass
class Event(StreamSendableDataClass):
    track_id: AccountId
    event_key: str
    event: EventType
    event_data: Mapping[str, str]
    visit: VisitInfo

    def partition_key(self: 'Event') -> str:
        return str(self.track_id)


@dataclass
class Visit(StreamSendableDataClass):
    act_id: AccountId
    e: str
    u: str
    r: str

    def partition_key(self: 'Visit') -> str:
        return str(self.act_id)


@dataclass
class Conversion(StreamSendableDataClass):
    act: AccountId
    e: str
    u: str
    c: int
    v: Any

    def partition_key(self: 'Conversion') -> str:
        return str(self.act)


@dataclass
class Config:
    aws_access_key: str
    aws_secret_key: str
    aws_region: str


@dataclass
class PutRecordResponse:
    shard_id: str
    sequence_number: str
    # encryption_type: str
