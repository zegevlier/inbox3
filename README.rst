Inbox3: SMTP Server for Humans with asyncio
===========================================


Inspired by the `inbox.py <https://github.com/kennethreitz/inbox.py>`_ based on asyncore.

Inbox3 is an asyncio-based SMTP server.

Usage
-----

Give your app an inbox easily::

    from inbox3 import Inbox

    inbox = Inbox()


    @inbox.collate
    def handle(to, sender, subject, body):
        print('Message sender %s' % sender)
        print('Message to %s' % to)
        print('Message body: \n')
        print(body)
        print('End of message')


    # Bind directly.
    inbox.serve(address='0.0.0.0', port=4467)


You can also defer to the commandline::

    if __name__ == '__main__':
        inbox.dispatch()

::

    $ dasinbox.py 0.0.0.0 4467
    [2012-04-28 07:31] INFO: inbox3: Starting SMTP server at 0.0.0.0:4467


Installation
------------

    $ pip install git+https://github.com/2minchul/inbox3.git
