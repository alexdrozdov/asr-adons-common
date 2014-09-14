 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pickle
import traceback
import localdb
import time
import select
import thread

class SndRouter(object):
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
class SndDaemon(object):
    def __init__(self, manager):
        self.man = manager
        remote_hosts = None
        try:
            remote_hosts = localdb.db.read_value("/db/persistent/sendmsg/localhost/remote_hosts")
        except:
            return
        self.routers = self.__generate_msg_routers(remote_hosts)
    def __build_sndmsg_list(self, remote_hosts):
        msglist = []
        for rh in remote_hosts:
            for m in rh.messages_to_send:
                if m in msglist:
                    continue
                msglist.append(m)
        return msglist
    def __generate_msg_routers(self, remote_hosts):
        self.routers = []
        msg_list = self.__build_sndmsg_list(remote_hosts)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for m in msg_list:
            router = SndRouter(self.sock, self.man, m)
            hosts = [(rhci.get_address(), int(rhci.get_channel_params())) for rhci in remote_hosts if m in rhci.messages_to_send ]
            for h in hosts:
                router.add_remote_host(h)

class UdpReceiver:
    def __init__(self, manager, port):
        self.man = manager
        self.port = port
        self.fd = None
        self.open_port()
    def open_port(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        self.sock.setblocking(False)
        self.fd = self.sock.fileno()
    def get_fd(self):
        return self.fd
    def get_socket(self):
        return self.sock
    def read_socket(self):
        data, addr = self.sock.recvfrom(65000)
        try:
            remote_ticket = pickle.loads(data)
            ticket = self.man.ticket(remote_ticket.get_data_name(),
                                            remote_ticket.get_data(), description = remote_ticket.description)
            self.man.push_ticket(ticket)
        except:
            print traceback.format_exc()
        #self.man.push_ticket(self.man.ticket(self.data_id, data, self.ticket_name))
class UdpPoller:
    def __init__(self):
        self.p = select.poll()
        self.fd_to_receiver = {}
        self.enabled = False
        self.is_running = False
    def add_udp_receiver(self, udp_receiver):
        self.p.register(udp_receiver.get_socket(), select.POLLIN | select.POLLHUP)
        self.fd_to_receiver[udp_receiver.get_fd()] = udp_receiver
    def __poll(self, timeout):
        events = self.p.poll(timeout)
        for fd, flag in events:
            ur = self.fd_to_receiver[fd]
            ur.read_socket()
    def __poll_thread(self):
        self.is_running = True
        try:
            while self.enabled:
                self.__poll(1000)
        except:
            print traceback.format_exc()
        self.is_running = False
    def start_async_operation(self):
        self.enabled = True
        self.is_running = False
        self.rcv_thread = thread.start_new_thread(self.__poll_thread, ())
    def stop_async_operation(self):
        self.enabled = False
        while self.is_running:
            time.sleep(1)
    def clear(self):
        self.stop_async_operation()
        for fd in self.fd_to_receiver.keys():
            self.p.unregister(fd)


class RcvDaemon:
    def __init__(self, manager):
        self.man = manager
        rcv_ports = None
        self.udp_poller = UdpPoller()
        try:
            rcv_ports = localdb.db.read_value("/db/persistent/sendmsg/localhost/rcv_ports")
        except:
            return
        for r in rcv_ports:
            ur = UdpReceiver(self.man, int(r.get_channel_params(),0))
            self.udp_poller.add_udp_receiver(ur)
        self.udp_poller.start_async_operation()

def init_module(manager, gui):
    s = SndDaemon(manager)
    r = RcvDaemon(manager)
    return [r, s]
