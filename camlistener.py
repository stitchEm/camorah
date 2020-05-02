import wsock

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import socket



CAMERA_SERVICE_NAME = "_vscamera._tcp.local."
CAMERA_CONTROL_ENDPOINT = "control"


class CamListener:


    def __init__(self):
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, CAMERA_SERVICE_NAME,
                                      handlers=[self._on_service_state_change])
	
    def url_join(self, scheme, hostname, port, *path):
        scheme = "{}://".format(scheme) if scheme is not None else ""
        netloc = "{}:{}".format(hostname, port) if port is not None else hostname
        path = "/{}".format("/".join(path)) if len(path) > 0 else ""
        return "{}{}{}".format(scheme, netloc, path)

    def _on_service_state_change(self, zeroconf, service_type, name, state_change):
        if  state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                print("Camera discovered at " + socket.inet_ntoa(info.address) + ":" + str(info.port))
                self.ws_url = self.url_join("ws", socket.inet_ntoa(info.address), str(info.port), CAMERA_CONTROL_ENDPOINT)
                print("Camera control at " + self.ws_url)

                ws = wsock.WSocket()
                ws.connect(self.ws_url, socket.inet_ntoa(info.address), info.port)
