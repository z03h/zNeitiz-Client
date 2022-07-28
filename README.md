# zNeitiz

Wrapper for [zNeitiz API](https://zneitiz.herokuapp.com/).

Don't expect great things, pretty quick and dirty.
The API is also on heroku so don't expect anything there either.

Minimum python version is probaby `3.9`.

Sample images [in the wiki](../../wiki).

## Examples

```python

import asyncio
import aiohttp

from zneitiz import NeitizClient, NeitizException, NeitizRatelimitException

token = '...'
image_url = '...'


async def main():

    print(zneitiz.__version__)

    # Use an already existing aiohttp.ClientSession.
    cs = aiohttp.ClientSession()
    znclient = NeitizClient(token, session=cs)
    # returns an awaitable `Route` that returns a `NeitizImage`.
    # `NeitizImage`s should be treated like an `io.BytesIO`
    # has `endpoint`, `content_type` and `extension` attributes
    # can access the Route used for the request with `route` attribute.
    try:
        route = znclient.sand(image_url)
        file = await route  # can also be shortened to await znclient.sand(image_url)
    except NeitizRatelimitException as e:
        # client will raise NeitizRatelimitException to prevent 429 errors
        print('ratelimit reset', e.ratelimit_reset)
    except NeitizHTTPException as e:
        # can get the status and message of other failed requests
        print(e.status, e.message)
    else:
        with open(f'{file.endpoint}.{file.extension}', 'wb') as f:
            f.write(file.read())

    # NeitizClient should be closed if you do not pass in a session
    znclient.close()

    # Use context manager to handle cleanup.
    # Can opt to pass `None` for session if you do not want to create a session
    async with NeitizClient(token, session=None) as znclient:
        # You can access `Route.url`, `Route.headers`, and `Route.json` for
        # manual requests or use with other libraries.
        route = znclient.sand(image_url)
        url: str = route.url
        headers: dict[str, str] = route.headers
        json_body: dict[str, any] = route.json

        import requests
        r = requests.get(url=url, headers=headers, json=json_body)

    async with NeitizClient(token) as znclient:
        # use an async context manager with Route to handle the request manually
        async with znclient.sand(image_url) as response:
            headers = response.headers
            if response.ok:
                data = await response.read()
            else:
                print(response.status, response.message)


asyncio.run(main())
```
