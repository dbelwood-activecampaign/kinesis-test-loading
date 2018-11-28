from loading.domain import PutRecordResponse, StreamSendable
from loading.stream_client import StreamClient


class Sender:
    def __init__(self, stream_client: StreamClient):
        self.stream_client = stream_client

    def send_data(self, data: StreamSendable) -> PutRecordResponse:
        return self.stream_client.put_record(data.to_record())
