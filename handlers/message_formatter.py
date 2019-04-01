'''Publish message to SNS'''

import json
import logging
import os

from typing import Tuple

import boto3

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', '')
SNS_CLIENT = boto3.client('sns')


def _get_message_data_from_event(event: dict) -> Tuple[dict, str]:
    '''Return message data from event.'''
    message = json.loads(event.get('Records')[0].get('Sns').get('Message'))
    subject = event.get('Records')[0].get('Sns').get('Subject')

    return (message, subject)


def _publish_sns_message(msg: dict, subject: str, topic_arn: str = SNS_TOPIC_ARN) -> dict:
    '''Publish message to SNS topic'''
    msg_str = json.dumps(msg)
    r = SNS_CLIENT.publish(
        TargetArn=topic_arn,
        Subject=subject,
        Message=msg_str
    )
    return r


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event: {}'.format(json.dumps(event)))

    msg, subject = _get_message_data_from_event(event)
    resp = _publish_sns_message(msg, subject)

    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp

