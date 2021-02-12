import os
from collections import namedtuple

Email = namedtuple('Email',
                   ['id', 'timestamp', 'sender', 'subject',
                    'content', 'has_attachemnts', 'is_threaded', 'is_forwarded'])
