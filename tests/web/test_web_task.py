#!/usr/bin/env python

import os

from circuits.web import Controller
from circuits import Event, Component

from .helpers import urlopen


class Hello(Event):
    """Hello Event"""

class Root(Controller):

    def index(self):
        return self.push(Hello(os.getpid()))

class Task(Component):

    def hello(self, pid):
        return "Hello %d i'm %d" % (pid, os.getpid())

def test(webapp):
    from circuits import Debugger
    Debugger().register(webapp)
    t = Task()
    t.start(link=webapp, process=True)
    print('calling url open')
    f = urlopen(webapp.server.base)
    print('reading response')
    s = f.read()
    assert s == b"Hello %d i'm %d" % (os.getpid(), t._task.pid)
    t.stop()
