import httpx

httpx.HTTPTransport
class FingerprintTransport(httpx.BaseTransport):
    """
    Spoofs TCPIP Fingerprints
    """

    def handle_request(self, request):
        print('YAYAYA')
        return super().handle_request(request)
