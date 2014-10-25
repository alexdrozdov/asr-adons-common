 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
import traceback
import localdb
import time
import select
import thread
import asyncore


class SndUdpRouter(object):
    def __init__(self, sock, manager, data_id):
        self.sock = sock
        self.data_id = data_id
        self.man = manager
        self.man.register_handler(data_id, self.ticket_handler)
        self.remote_hosts = []
    def add_remote_host(self, addr_port):
        self.remote_hosts.append(addr_port)
    def ticket_handler(self, ticket):
        ticket = ticket.export_standalone_ticket()
        pickled_ticket = pickle.dumps(ticket)
        for h in self.remote_hosts:
            self.sock.sendto(pickled_ticket, h)
class SndTcpRouter(object):
    def __init__(self, manager, addr):
        self.man = manager
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
    def add_data_id(self, data_id):
        self.man.register_handler(data_id, self.ticket_handler)
    def ticket_handler(self, ticket):
        ticket = ticket.export_standalone_ticket()
        pickled_ticket = pickle.dumps(ticket)
        self.sock.send(pickled_ticket)
class SndFabric(object):
    def __init__(self, manager):
        self.man = manager
        remote_hosts = None
        try:
            remote_hosts = localdb.db.read_value("/db/persistent/sendmsg/localhost/remote_hosts")
        except:
            return
        self.udp_routers = self.__generate_udp_routers(remote_hosts)
        self.tcp_routers = self.__generate_tcp_routers(remote_hosts)
    def __build_sndmsg_list(self, remote_hosts, channel):
        msglist = []
        for rh in remote_hosts:
            if not rh.get_enabled():
                continue
            if rh.get_channel().lower() != channel.lower():
                continue
            for m in rh.messages_to_send:
                if m in msglist:
                    continue
                msglist.append(m)
        return msglist
    def __generate_udp_routers(self, remote_hosts):
        routers = []
        msg_list = self.__build_sndmsg_list(remote_hosts, 'udp') #Full message list for all hosts receiving udp
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for m in msg_list:
            router = SndUdpRouter(self.sock, self.man, m)
            hosts = [(rhci.get_address(), int(rhci.get_channel_params())) for rhci in remote_hosts if m in rhci.messages_to_send and rhci.get_channel().lower()=='udp' ]
            for h in hosts:
                router.add_remote_host(h)
            routers.append(router)
        return routers
    def __generate_tcp_routers(self, remote_hosts):
        routers = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for h in [h for h in remote_hosts if h.get_channel().lower()=='tcp']:
            router = SndTcpRouter(self.man, (h.get_address(), int(h.get_channel_params())))
            for m in h.messages_to_send:
                router.add_data_id(m)
            routers.append(router)
        return routers

class UdpReceiver(asyncore.dispatcher):
    def __init__(self, manager, port):
        asyncore.dispatcher.__init__(self)
        self.man = manager
        
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('', port))
    def recvfrom(self, buffer_size):
        try:
            data,addr = self.socket.recvfrom(buffer_size)
            if not data:
                self.handle_close()
                return ('','')
            else:
                return (data,addr)
        except socket.error, why:
            # winsock sometimes raises ENOTCONN
            if why.args[0] in _DISCONNECTED:
                self.handle_close()
                return ''
            else:
                raise
    def handle_read(self):
        data,addr = self.recvfrom(65000)
        try:
            remote_ticket = pickle.loads(data)
            ticket = self.man.ticket(remote_ticket.get_data_name(),
                                            remote_ticket.get_data(), description = remote_ticket.description)
            self.man.push_ticket(ticket)
        except:
            print traceback.format_exc()

class TcpReceiver(asyncore.dispatcher):
    def __init__(self, manager, sock):
        asyncore.dispatcher.__init__(self, sock=sock)
        self.man = manager
    def handle_read(self):
        data = self.recv(65535)
        try:
            remote_ticket = pickle.loads(data)
            ticket = self.man.ticket(remote_ticket.get_data_name(),
                                            remote_ticket.get_data(), description = remote_ticket.description)
            self.man.push_ticket(ticket)
        except:
            print traceback.format_exc()

class TcpAcceptor(asyncore.dispatcher):
    def __init__(self, manager, port):
        asyncore.dispatcher.__init__(self)
        self.man = manager
        self.receivers = []
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
    def handle_accept(self):
        pair = self.accept()
        if pair == None:
            return
        sock, addr = pair
        self.receivers.append(TcpReceiver(self.man, sock))
class RcvFabric:
    def __init__(self, manager):
        self.man = manager
        rcv_ports = []
        try:
            rcv_ports = localdb.db.read_value("/db/persistent/sendmsg/localhost/rcv_ports")
        except:
            return
        for r in rcv_ports:
            if r.get_channel().lower()=="udp":
                ur = UdpReceiver(self.man, int(r.get_channel_params(),0))
            elif r.get_channel().lower()=="tcp":
                ur = TcpAcceptor(self.man, int(r.get_channel_params(),0))
        self.rcv_thread = thread.start_new_thread(self.__poll_thread, ())
    def __poll_thread(self):
        self.is_running = True
        asyncore.loop()
        self.is_running = False

def init_module(manager, gui):
    r = RcvFabric(manager)
    s = SndFabric(manager)
    return [r, s]
