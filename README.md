# zNeitiz
Client for [zNeitiz API](https://zneitiz.herokuapp.com/).

Don't expect great things, pretty quick and dirty setup.
The API is also on heroku so don't expect speed/good uptime.

## Examples
```python
import asyncio
import aiohttp
from zneitiz import NeitizClient, NeitizException

token = '...'
image_url = '...'


async def main():

    # Use an already existing aiohttp.ClientSession.
    async with aiohttp.ClientSession() as cs:
        znclient = NeitizClient(token, session=cs)
        # returns a tuple of (io.IOBase, str) for the image and file extension.
        file, file_extension = await znclient.sand(image_url)
        with open(f'file.{file_extension}', 'wb') as f:
            f.write(file.read())
        znclient.close()


    # Use context manager to automatically create an
    # aiohttp.ClientSession and close it.
    async with NeitizClient(token) as znclient:
        ...


    # Passing `None` session makes methods returns a Route instead of a coroutine.
    # You can access `Route.url`, `Route.headers`, `Route.json` for
    # use with other libraries such as requests.
    znclient = NeitizClient(token, session=None)
    route = znclient.sand(image_url)
    url: str = route.url
    headers: dict[str, str] = route.headers
    json_body: dict[str, any] = route.json


    # Can also be done by passing `raw=True` to an endpoint method.
    async with NeitizClient(token) as znclient:
        try:
            route = znclient.sand(image_url, raw=True)
        except NeitizException as e:
            # can get the status and message of failed requests
            print(e.status, e.message)
```
