# pylint: disable=line-too-long
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from .. import __main__

JSON_SAMPLE = [
    {
        'albumId': 1,
        'id': 1,
        'title': 'accusamus beatae ad facilis cum similique qui sunt',
        'url': 'https://via.placeholder.com/600/92c952',
        'thumbnailUrl': 'https://via.placeholder.com/150/92c952'
    },
    {
        'albumId': 1,
        'id': 2,
        'title': 'reprehenderit est deserunt velit ipsam',
        'url': 'https://via.placeholder.com/600/771796',
        'thumbnailUrl': 'https://via.placeholder.com/150/771796'
    },
]


class TestMain(IsolatedAsyncioTestCase):

    @patch('__main__.__builtins__.print')
    async def test_no_args_exits_1(self, mock_print):
        test_args = ['progname']
        with patch('__main__.sys.argv', test_args):
            with self.assertRaises(SystemExit) as sys_exit:
                await __main__.main()
                self.assertEqual(1, sys_exit.exception.code)
                mock_print.assert_called_once()

    @patch('__main__.__builtins__.print')
    async def test_no_albums_exits_1(self, mock_print):
        test_args = ['progname', '-a']
        with patch('__main__.sys.argv', test_args):
            with self.assertRaises(SystemExit) as sys_exit:
                await __main__.main()
                self.assertEqual(1, sys_exit.exception.code)
                mock_print.assert_called_once()

    @patch('__main__.__builtins__.print')
    async def test_bad_commas_exits_2(self, mock_print):
        test_args = (
            ['progname', '-a', '1,,'],
            ['progname', '-a', '1', '-i', '1,,']
        )
        for args in test_args:
            with self.subTest(args=args):
                with patch('__main__.sys.argv', args):
                    with self.assertRaises(SystemExit) as sys_exit:
                        await __main__.main()
                        self.assertEqual(2, sys_exit.exception.code)
                        mock_print.assert_called_once()

    @patch('__main__.__builtins__.print')
    async def test_path_doesnt_exist_exits_3(self, mock_print):
        test_args = ['progname', '-a', '1', '-o', 'foobarbaz']
        with patch('__main__.sys.argv', test_args):
            with self.assertRaises(SystemExit) as sys_exit:
                await __main__.main()
                self.assertEqual(3, sys_exit.exception.code)
                mock_print.assert_called_once_with('output path does not exist')

    @patch('__main__.__builtins__.print')
    async def test_path_is_not_dir_exits_4(self, mock_print):
        test_args = ['progname', '-a', '1', '-o', 'test_main.py']
        with patch('__main__.sys.argv', test_args):
            with self.assertRaises(SystemExit) as sys_exit:
                await __main__.main()
                self.assertEqual(4, sys_exit.exception.code)
                mock_print.assert_called_once_with('output path is not a directory')

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_success_no_dl(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)
        mock_download_image.assert_not_called()

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_regex_match(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1', '-r', 'facilis']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 1)
        mock_download_image.assert_not_called()

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_regex_no_match(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1', '-r', 'foobarbaz']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 0)
        mock_download_image.assert_not_called()

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_image_id_match(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1', '-i', '1']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 1)
        mock_download_image.assert_not_called()

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_image_id_no_match(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1', '-i', '42']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 0)
        mock_download_image.assert_not_called()

    @patch('app.__main__.download_image')
    @patch('app.__main__.get_album_json')
    @patch('__main__.__builtins__.print')
    async def test_image_download(self, mock_print, mock_get_json, mock_download_image):
        mock_get_json.return_value = JSON_SAMPLE
        test_args = ['progname', '-a', '1', '-s']
        with patch('__main__.sys.argv', test_args):
            await __main__.main()
        mock_get_json.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_download_image.call_count, 2)
