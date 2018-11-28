from boto3 import Session

from loading.domain import Config, PutRecordResponse, Record


class StreamClient:
    def __init__(self, config: Config, stream_name: str):
        session = Session(
            aws_access_key_id=config.aws_access_key,
            aws_secret_access_key=config.aws_secret_key,
            region_name=config.aws_region
        )
        self.kinesis = session.client('kinesis')
        self.stream_name = stream_name

    def put_record(self, record: Record) -> PutRecordResponse:
        response = self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=record.data,
            PartitionKey=record.partition_key
        )
        return PutRecordResponse(
            response['ShardId'],
            response['SequenceNumber']
            # ,
            # response['EncryptionType']
        )
