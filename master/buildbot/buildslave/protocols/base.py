# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from buildbot.util import service
from buildbot.util import subscription


class Listener(service.ReconfigurableServiceMixin, service.AsyncMultiService):
    pass


class Connection(object):
    proxies = {}

    def __init__(self, master, buildslave):
        self.master = master
        self.buildslave = buildslave
        name = buildslave.slavename
        self._disconnectSubs = subscription.SubscriptionPoint(
            "disconnections from %s" % name)

    # This method replace all Impl args by their Proxy protocol implementation
    def createArgsProxies(self, args):
        newargs = {}
        for k, v in args.iteritems():
            for implclass, proxyclass in self.proxies.items():
                if isinstance(v, implclass):
                    v = proxyclass(v)
            newargs[k] = v
        return newargs
    # disconnection handling

    def notifyOnDisconnect(self, cb):
        return self._disconnectSubs.subscribe(cb)

    def notifyDisconnected(self):
        self._disconnectSubs.deliver()

    def loseConnection(self):
        raise NotImplementedError

    # methods to send messages to the slave

    def remotePrint(self, message):
        raise NotImplementedError

    def remoteGetSlaveInfo(self):
        raise NotImplementedError

    def remoteSetBuilderList(self, builders):
        raise NotImplementedError

    def remoteStartCommand(self, remoteCommand, builderName, commandId, commandName, args):
        raise NotImplementedError

    def remoteShutdown(self):
        raise NotImplementedError

    def remoteStartBuild(self, builderName):
        raise NotImplementedError

    def remoteInterruptCommand(self, builderName, commandId, why):
        raise NotImplementedError


# RemoteCommand base implementation and base proxy
class RemoteCommandImpl(object):

    def remote_update(self, updates):
        raise NotImplementedError

    def remote_complete(self, failure=None):
        raise NotImplementedError


# FileWriter base implementation
class FileWriterImpl(object):

    def remote_write(self, data):
        raise NotImplementedError

    def remote_utime(self, accessed_modified):
        raise NotImplementedError

    def remote_unpack(self):
        raise NotImplementedError

    def remote_close(self):
        raise NotImplementedError


# FileReader base implementation
class FileReaderImpl(object):

    def remote_read(self, maxLength):
        raise NotImplementedError

    def remote_close(self):
        raise NotImplementedError
