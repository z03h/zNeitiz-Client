# zNeitiz

Wrapper for [zNeitiz API](https://zneitiz.onrender.com/)[source](https://github.com/z03h/zNeitiz-public).

Install with `pip install zneitiz` or from GitHub with `pip install zneitiz@git+https://github.com/z03h/zNeitiz-Clienty@master`.

Don't expect great things, pretty quick and dirty.
The API is also low effort so don't expect much from it.

Minimum python version is probaby `3.9`.

Sample images [in the wiki](../../wiki).

## Examples

```python

import asyncio
import aiohttp

from zneitiz import NeitizClient, NeitizException, NeitizRatelimitException

image_url = '...'


async def main():

    print(zneitiz.__version__)

    # Use an already existing aiohttp.ClientSession.
    cs = aiohttp.ClientSession()
    znclient = NeitizClient(session=cs)
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
            data = file.read()
            f.write(data)


    # All image urls can be replace with file-like objects
    # such as BytesIO or opened files
    with open('path/to/image.png', 'rb') as image:
        data = image.read()
        new_data = await znclient.explode(io.BytesIO(data))

        image.seek(0)
        other_data = await znclient.explode(image)

    # NeitizClient should be closed if you do not pass in a session
    await znclient.close()


    # Use context manager to handle cleanup.
    # Can opt to pass `None` for session if you do not want to create a session
    async with NeitizClient(session=None) as znclient:
        # You can access `Route.url`, `Route.headers`, and `Route.json` for
        # manual requests or use with other libraries.
        route = znclient.sand(image_url)
        url: str = route.url
        headers: dict[str, str] = route.headers
        json_body: dict[str, any] = route.json

        import requests
        r = requests.post(url=url, headers=headers, json=json_body)


    # can use an async context manager with Route to handle the request manually
    async with NeitizClient() as znclient:
        async with znclient.sand(image_url) as response:
            headers = response.headers
            if response.ok:
                data = await response.read()
            else:
                print(response.status, response.message)



asyncio.run(main())
```
