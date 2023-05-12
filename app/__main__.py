import asyncio
from pathlib import Path
import re
import sys

import aiohttp

from .args import parser, cleanup_comma_seperated_args
from .requests import get_album_json, download_image


def _cleanup_commas(args, name):
    try:
        cleanup_comma_seperated_args(args)
    except ValueError:
        print(f'invalid `{name}` argument, must be an integer')
        sys.exit(2)


async def main():
    args = parser.parse_args()
    if len(args.albums) == 0:
        print(parser.format_usage())
        sys.exit(1)
    if args.albums is not None:
        _cleanup_commas(args.albums, 'albums')
    if args.images is not None:
        _cleanup_commas(args.images, 'images')
    args.images = set(args.images) if args.images else set()
    pattern = None
    if args.regex is not None:
        pattern = re.compile(args.regex)
    path = Path('.') if args.out is None else Path(args.out)
    if not path.exists():
        print('output path does not exist')
        sys.exit(3)
    if not path.is_dir():
        print('output path is not a directory')
        sys.exit(4)
    async with aiohttp.ClientSession() as session:
        download_targets = []
        album_data = await asyncio.gather(
            *(get_album_json(session, album_id) for album_id in args.albums)
        )
        for album in album_data:
            for image in album:
                if ((pattern is None or pattern.findall(image['title'])) and
                        (not args.images or image['id'] in args.images)):
                    if not args.quiet:
                        print(f"[{image['id']}] {image['title']}")
                    if args.save:
                        download_targets.append(
                            (image['url'], f"{image['albumId']}-{image['id']}")
                        )
        if args.save:
            await asyncio.gather(
                *(
                    download_image(session, url, path / filename)
                    for url, filename in download_targets
                )
            )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
