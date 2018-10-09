# -*- coding: utf-8 -*-

import sys
import argparse
from email.parser import Parser

from aiosmtpd.controller import Controller
from logbook import Logger, StreamHandler

log = Logger(__name__)
StreamHandler(sys.stdout).push_application()


class InboxServerHandler:
    def __init__(self, handler):
        self._handler = handler

    async def handle_DATA(self, server, session, envelope):
        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos
        data = envelope.content.decode('utf8', errors='replace')
        log.info('Collating message from {0}'.format(mailfrom))
        subject = Parser().parsestr(data)['subject']
        log.debug(dict(to=rcpttos, sender=mailfrom, subject=subject, body=data))
        if self._handler:
            self._handler(to=rcpttos, sender=mailfrom, subject=subject, body=data)

        return '250 Message accepted for delivery'


class Inbox(object):
    """A simple SMTP Inbox."""

    def __init__(self, port=None, address=None):
        self.port = port
        self.address = address
        self.collator = None

    def collate(self, collator):
        """Function decorator. Used to specify inbox handler."""
        self.collator = collator
        return collator

    def serve(self, port=None, address=None):
        """Serves the SMTP server on the given port and address."""
        port = port or self.port
        address = address or self.address

        log.info('Starting SMTP server at {0}:{1}'.format(address, port))
        controller = Controller(InboxServerHandler(self.collator), hostname=address, port=port)

        try:
            controller.start()
            controller._thread.join()
        except KeyboardInterrupt:
            log.info('Cleaning up')
        finally:
            controller.stop()

    def dispatch(self):
        """Command-line dispatch."""
        parser = argparse.ArgumentParser(description='Run an Inbox server.')

        parser.add_argument('addr', metavar='addr', type=str, help='addr to bind to')
        parser.add_argument('port', metavar='port', type=int, help='port to bind to')

        args = parser.parse_args()

        self.serve(port=args.port, address=args.addr)
