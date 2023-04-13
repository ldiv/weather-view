import httpx


class SimpleHTTPClient:
    def __init__(self):
        self._session = httpx.Client()

    def get(self, url, **kwargs):
        resp = self._session.get(url, **kwargs)
        self._validate_response(resp)
        return resp

    def post(self, url, data, **kwargs):
        resp = self._session.post(url, data=data, **kwargs)
        self._validate_response(resp)
        return resp

    def put(self, url, **kwargs):
        raise NotImplementedError

    def delete(self, url, **kwargs):
        raise NotImplementedError

    def _validate_response(self, response):
        if response.status_code not in (200,):
            raise InvalidResponse


class InvalidResponse(httpx.HTTPStatusError):
    ...
