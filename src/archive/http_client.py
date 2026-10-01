"""Bounded local HTTP renderer for static exports and route regressions."""
from __future__ import annotations
import json
import socket
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
import uvicorn
from .util import ArchiveError

class LocalResponse:
    def __init__(self, response):
        self.status_code=response.code
        self.content=response.read()
        self.text=self.content.decode('utf-8',errors='replace')
    def json(self):return json.loads(self.content)

class LocalAppClient:
    """Real loopback requests; startup, requests and shutdown have bounds."""
    def __init__(self,app,timeout=5):
        self.timeout=timeout
        self.socket=socket.socket()
        self.socket.bind(('127.0.0.1',0));self.socket.listen(128)
        self.base='http://127.0.0.1:'+str(self.socket.getsockname()[1])
        self.server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',log_level='error',lifespan='off'))
        self.thread=threading.Thread(target=self.server.run,kwargs={'sockets':[self.socket]},daemon=True)
        self.thread.start();deadline=time.monotonic()+timeout
        while not self.server.started and self.thread.is_alive() and time.monotonic()<deadline:time.sleep(.01)
        if not self.server.started:
            self.close();raise ArchiveError('Local renderer did not start within its timeout')
    def get(self,path,params=None):
        if params:path+=('&' if '?' in path else '?')+urlencode(params)
        try:
            with urlopen(Request(self.base+quote(path,safe='/%?=&+#')),timeout=self.timeout) as response:return LocalResponse(response)
        except HTTPError as response:
            with response:return LocalResponse(response)
        except (TimeoutError,OSError) as error:raise ArchiveError('Local renderer HTTP request failed: '+str(error)) from error
    def close(self):
        self.server.should_exit=True;self.thread.join(timeout=3);self.socket.close()
        if self.thread.is_alive():raise ArchiveError('Local renderer did not stop within its timeout')
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
