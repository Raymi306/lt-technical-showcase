TARGET = 'https://jsonplaceholder.typicode.com/photos'
CHUNK_SIZE = 4096


async def get_album_json(session, album_id):
    params = {
        'albumId': album_id
    }
    async with session.get(TARGET, params=params) as resp:
        return await resp.json()


async def download_image(session, url, path):
    async with session.get(url) as resp:
        with open(path, 'wb') as f:
            async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                f.write(chunk)
