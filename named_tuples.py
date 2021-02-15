import os
from collections import namedtuple

Email = namedtuple('Email',
                   ['id', 'timestamp', 'sender_name', 'sender_email', 'receiver_name', 'receiver_email',
                    'subject', 'content', 'has_attachments', 'is_threaded', 'is_forwarded', 'reply'])
