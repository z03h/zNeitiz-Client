# zNeitiz

Client for [zNeitiz API](https://zneitiz.herokuapp.com/).

Don't expect great things, pretty quick and dirty.
The API is also on heroku so don't expect anything there either.

Sample images [here](../../wiki).

## Examples

```python

import asyncio

import aiohttp

from zneitiz import NeitizClient, NeitizException

token = '...'
image_url = '...'


async def main():

    # Use an already existing aiohttp.ClientSession.
    cs = aiohttp.ClientSession()
    znclient = NeitizClient(token, session=cs)
    # returns a tuple of (io.BytesIO, str), the image and file extension.
    file, file_extension = await znclient.sand(image_url)
    with open(f'file.{file_extension}', 'wb') as f:
        f.write(file.read())
    znclient.close()  # NeitizClient will not cleanup sessions you pass in yourself

    # Use context manager to close any automatically created sessions if one isn't provided.
    async with NeitizClient(token) as znclient:
        ...

    # Passing `session=None` makes methods returns a Route instead of a coroutine.
    # You can access `Route.url`, `Route.headers`, and `Route.json` for
    # use with other libraries such as requests.
    znclient = NeitizClient(token, session=None)
    route = znclient.sand(image_url)
    url: str = route.url
    headers: dict[str, str] = route.headers
    json_body: dict[str, any] = route.json
    async with cs.get(url, headers=headers, json=json_body) as response:
        ...
    # use NeitizClient.request with the Route to manually handle the aiohttp.ClientResponse
    async with znclient.request(route) as response:
        headers = response.headers
        if respnose.ok:
            data = await response.read()
        else:
            print(response.status, response.message)

    # Can also be done by passing `raw=True` to an endpoint method.
    async with NeitizClient(token) as znclient:
        try:
            route = znclient.sand(image_url, raw=True)
            async with znclient.request(route) as response:
                if respnose.ok:
                    data = await response.read()
                else:
                    print(response.status, response.message)
        except NeitizRatelimitException as e:
            # client will raise NeitizExcpetion to prevent 429 errors
            print('seconds til ratelimit reset', e.ratelimit_reset)
        except NeitizHTTPException as e:
            # can get the status and message of failed requests
            print(e.status, e.message)


asyncio.run(main())
```
