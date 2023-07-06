import os
import re

from slack_bolt import Ack, Respond
from logging import Logger

from slack_sdk import WebClient

from db import get_poll, open_poll, close_poll, reopen_poll

POLL_OPEN_EXAMPLE_CALL="/poll open my_poll [Delete Limit,Delete Quota,Delete all]"
POLL_CLOSE_EXAMPLE_CALL="/poll close my_poll"
POLL_REOPEN_EXAMPLE_CALL="/poll reopen my_poll"
POLL_GET_EXAMPLE_CALL="/poll get my_poll"

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def poll_command_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        logger.info(f' command => {command}')

        verb_pattern = '(open|close|reopen|get)\s+(.*)'
        verb_match = re.search(verb_pattern, command['text']) 

        if verb_match:
            verb = verb_match.group(1)
            subject = verb_match.group(2)
            logger.debug(f' verb => {verb} subject => {subject}')
            
            match verb.lower():
                case 'open':
                    (poll_name, option_1, option_2, option_3) = extract_args_open(subject, logger)
                    respond(f'Opening poll {poll_name}')
                    open_poll(poll_name, option_1, option_2, option_3)
                    client.chat_postMessage(
                        channel=command['channel_name'],
                        text=f'Poll {poll_name} opened for voting:\n1. {option_1}\n2. {option_2}\n3. {option_3}',
                    )
                case 'close':
                    poll_name = extract_args_close(subject, logger)
                    respond(f'Closing poll {poll_name}')
                    poll = get_poll(poll_name)
                    if poll is not None:
                        close_poll(poll_name)
                        counts = poll['option_1_count'],poll['option_2_count'],poll['option_3_count']
                        winner = counts.index(max(counts))
                        client.chat_postMessage(
                            channel=command['channel_name'],
                            text=f'Poll {poll_name} closed, the winner is option {winner + 1}',
                        )
                    else:
                        respond(f'No such a poll named {poll_name}')
                case 'reopen':
                    poll_name = extract_args_reopen(subject, logger)
                    respond(f'Reopening poll {poll_name}')
                    reopen_poll(poll_name)
                    client.chat_postMessage(
                        channel=command['channel_name'],
                        text=f'Poll {poll_name} reopened',
                    )
                case 'get':
                    poll_name = extract_args_get(subject, logger)
                    respond(f'Getting poll {poll_name}')
                    poll = get_poll(poll_name)
                    if poll is not None:
                        respond(f"Poll {poll['poll_name']} is {poll['status']}:\n1. {poll['option_1']}\n2. {poll['option_2']}\n3. {poll['option_3']}")
                    else:
                        respond(f'No such a poll named {poll_name}')
                case _:
                    client.chat_postMessage(
                        channel=command['channel_name'],
                        text=f'Poll command not found!',
                    )

            # if verb.lower() == 'open':
            #     (poll_name, option_1, option_2, option_3) = extract_args_open(subject, logger)
            #     client.chat_postMessage(
            #         channel=command['channel_name'],
            #         text=f'Opening poll {poll_name} with options:\n1. {option_1}\n2. {option_2}\n3. {option_3}',
            #     )
            #     open_poll(poll_name, option_1, option_2, option_3)
            # else:
            #     if verb.lower() == 'close':
            #         poll_name = extract_args_close(subject, logger)
            #         client.chat_postMessage(
            #             channel=command['channel_name'],
            #             text=f'Closing poll {poll_name}',
            #         )
            #         close_poll(poll_name)
            #         poll = get_poll(poll_name)
            #         counts = poll['option_1_count'],poll['option_2_count'],poll['option_3_count']
            #         winner = counts.index(max(counts))
            #         client.chat_postMessage(
            #             channel=command['channel_name'],
            #             text=f'Poll {poll_name} closed, the winner is option {winner + 1}',
            #         )
                    
            #     else:
            #         raise Exception("Arguments malformed for '/poll open' try this instead: {POLL_OPEN_EXAMPLE_CALL}")
        else:
            logger.error("Poll command not found!")
            respond(f"Malformed command: /poll {command['text']}")

        # respond(f"Responding to the poll command! Your command was: {command['text']}")
    except Exception as e:
        logger.error(e)
        respond(f"Error command: /poll {command['text']} failed with this error: {e}")

def extract_args_open(subject: str, logger: Logger):
    pattern = '(\w+)\s+\[(.+),(.+),(.+)\]'
    match = re.search(pattern, subject) 

    if match:
        poll_name = match.group(1).lstrip().rstrip()
        option_1 = match.group(2).lstrip().rstrip()
        option_2 = match.group(3).lstrip().rstrip()
        option_3 = match.group(4).lstrip().rstrip()
        logger.debug(f'poll_name => {poll_name} option_1 => {option_1} option_2 => {option_2} option_3 => {option_3}')
    else:
        raise Exception(f"Arguments malformed for '/poll open' try this instead: {POLL_OPEN_EXAMPLE_CALL}")
    
    return (poll_name, option_1, option_2, option_3)

def extract_args_close(subject: str, logger: Logger):
    pattern = '(\w+)'
    match = re.search(pattern, subject) 

    if match:
        poll_name = match.group(1).lstrip().rstrip()
        logger.debug(f'poll_name => {poll_name}')
    else:
        raise Exception(f"Arguments malformed for '/poll close' try this instead: {POLL_CLOSE_EXAMPLE_CALL}")
    
    return poll_name

def extract_args_reopen(subject: str, logger: Logger):
    pattern = '(\w+)'
    match = re.search(pattern, subject) 

    if match:
        poll_name = match.group(1).lstrip().rstrip()
        logger.debug(f'poll_name => {poll_name}')
    else:
        raise Exception(f"Arguments malformed for '/poll reopen' try this instead: {POLL_REOPEN_EXAMPLE_CALL}")
    
    return poll_name

def extract_args_get(subject: str, logger: Logger):
    pattern = '(\w+)'
    match = re.search(pattern, subject) 

    if match:
        poll_name = match.group(1).lstrip().rstrip()
        logger.debug(f'poll_name => {poll_name}')
    else:
        raise Exception(f"Arguments malformed for '/poll get' try this instead: {POLL_GET_EXAMPLE_CALL}")
    
    return poll_name