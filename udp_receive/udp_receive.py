 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
import thread
import localdb
import traceback
import time

class UdpReceiver:
    def __init__(self, manager, data_id, data_description, ticket_name, port):
        self.man = manager
        self.data_id = data_id
        self.data_description = data_description
        self.ticket_name = ticket_name
        self.port = port
        self.fd = None
        self.open_port()
        self.man.add_data_id(data_id, data_description)
    def open_port(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', int(self.port,0)))
        self.sock.setblocking(False)
        self.fd = self.sock.fileno()
    def get_fd(self):
        return self.fd
    def get_socket(self):
        return self.sock
    def read_socket(self):
        data, addr = self.sock.recvfrom(65000)
        self.man.push_ticket(self.man.ticket(self.data_id, data, self.ticket_name))
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
        

class UdpRcvConfig:
    def __init__(self, manager):
        self.man = manager
        self._load()
    def _load(self):
        try:
            self.udp_poller = UdpPoller()
            receivers = localdb.db.read_value("/db/persistent/udp_receive/receivers")
            for rcv_cfg in receivers:
                try:
                    ur = UdpReceiver(self.man, rcv_cfg["data_id"], rcv_cfg["data_description"], rcv_cfg["ticket_name"], rcv_cfg["port"])
                    self.udp_poller.add_udp_receiver(ur)
                except:
                    print traceback.format_exc()
            self.udp_poller.start_async_operation()
        except:
            print traceback.format_exc()
    def reload(self):
        self.udp_poller.clear()
        self._load()

def init_module(manager, gui):
    urc = UdpRcvConfig(manager)
    return [urc, ]

