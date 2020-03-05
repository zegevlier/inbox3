# -*- coding: utf-8 -*-

import sys
import argparse
import inspect
from email.parser import Parser

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP, Envelope, Session


class InboxServerHandler:
    def __init__(self, handler):
        self._handler = handler

    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope):
        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos
        data = envelope.content.decode('utf8', errors='replace')
        subject = Parser().parsestr(data)['subject']
        result = None
        if self._handler:
            if inspect.iscoroutinefunction(self._handler):
                result = await self._handler(to=rcpttos, sender=mailfrom, subject=subject, body=data)
            else:
                result = await server.loop.run_in_executor(None, self._handler, rcpttos, mailfrom, subject, data)

        return '250 Message accepted for delivery' if result is None else result


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

    def serve(self, port=None, address=None, log_level=logbook.INFO):
        """Serves the SMTP server on the given port and address."""

        port = port or self.port
        address = address or self.address

        controller = Controller(InboxServerHandler(self.collator), hostname=address, port=port)

        try:
            controller.start()
            controller._thread.join()
        except KeyboardInterrupt:
        finally:
            controller.stop()

    def dispatch(self):
        """Command-line dispatch."""
        parser = argparse.ArgumentParser(description='Run an Inbox server.')

        parser.add_argument('addr', metavar='addr', type=str, help='addr to bind to')
        parser.add_argument('port', metavar='port', type=int, help='port to bind to')

        args = parser.parse_args()

        self.serve(port=args.port, address=args.addr)
