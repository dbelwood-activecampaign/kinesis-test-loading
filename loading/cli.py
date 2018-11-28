from datetime import datetime

import click

from loading.config import load_config
from loading.data_generation import generate_account_ids, generate_emails, \
    generate_event_fn
from loading.sender import Sender
from loading.stream_client import StreamClient


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config()


@cli.command()
@click.pass_context
@click.argument('event_count', default=1000)
@click.argument('accounts', default=10)
@click.argument('emails', default=100)
def send_events(ctx, event_count, accounts, emails):
    tic = datetime.utcnow()
    stream_client = StreamClient(ctx.obj['config'], 'track-events')
    account_ids = generate_account_ids(accounts)
    emails = generate_emails(emails)
    generate_fn = generate_event_fn(account_ids, emails)
    sender = Sender(stream_client)
    for _i in range(0, event_count - 1):
        event = generate_fn()
        response = sender.send_data(event)
    toc = datetime.utcnow()
    duration = (toc - tic).total_seconds()
    print(f'Posted {event_count} events in {duration} seconds')


if __name__ == '__main__':
    cli(obj={})
