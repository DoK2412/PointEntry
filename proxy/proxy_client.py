import os
import httpx
import ssl


from dotenv import load_dotenv

load_dotenv()

timeout = httpx.Timeout(60.0)

ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1


class RegisterService(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=os.getenv("REGISTR_SERVISE"),
            verify=False,
            timeout=timeout,
            **kwargs,
        )

