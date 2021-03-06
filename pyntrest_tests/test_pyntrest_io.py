"""Test suite for module pyntrest_io"""

from os import path
from tempfile import mkdtemp
from pyntrest import pyntrest_io, pyntrest_config
from shutil import rmtree
import unittest

class IoTestSuite(unittest.TestCase):

    base_path = path.abspath(path.dirname(__file__))

    def create_temp_file_with_content ( self, content, filename ):
        temp_dir = mkdtemp()
        self.addCleanup(rmtree, temp_dir, True)
        ofile = open (path.join(temp_dir, filename), 'w')
        for line in content:
            ofile.write(str(line) + '\n')
        ofile.close()
        return temp_dir

    def test_cleanup_url_path (self):

        self.assertRaises(TypeError, pyntrest_io.cleanup_url_path)
        self.assertEqual('/', pyntrest_io.cleanup_url_path(None))
        self.assertEqual('/', pyntrest_io.cleanup_url_path(''))
        self.assertEqual('/', pyntrest_io.cleanup_url_path('//'))
        self.assertEqual('/path/', pyntrest_io.cleanup_url_path('//path///'))
        self.assertEqual('/path/', pyntrest_io.cleanup_url_path('//path///index.html'))
        self.assertEqual('/path/path2/', pyntrest_io.cleanup_url_path('//path///path2/index.html'))

    def test_convert_url_path_to_local_filesystem_path (self):
        self.assertRaises(TypeError, pyntrest_io.convert_url_path_to_local_filesystem_path)
        self.assertRaises(TypeError, pyntrest_io.convert_url_path_to_local_filesystem_path, None)
        self.assertEqual(path.join(''), pyntrest_io.convert_url_path_to_local_filesystem_path('', ''))
        self.assertEqual(path.join('test'), pyntrest_io.convert_url_path_to_local_filesystem_path('', 'test'))
        self.assertEqual(path.join('test', 'test2', 'test3'), pyntrest_io.convert_url_path_to_local_filesystem_path('', '//test/test2//test3'))
        cwd = path.abspath(path.dirname(__file__))
        self.assertEqual(path.join(cwd, 'test', 'test2'), pyntrest_io.convert_url_path_to_local_filesystem_path(cwd, '//test/test2/'))
        self.assertEqual(path.join(cwd), pyntrest_io.convert_url_path_to_local_filesystem_path(cwd, ''))
        self.assertEqual(path.join(cwd), pyntrest_io.convert_url_path_to_local_filesystem_path(cwd, '//'))

    def test_get_absolute_breadcrumb_filesystem_paths (self):
        self.assertRaises(TypeError, pyntrest_io.get_absolute_breadcrumb_filesystem_paths)
        self.assertEqual(1, len(pyntrest_io.get_absolute_breadcrumb_filesystem_paths('')))
        self.assertEqual([''], pyntrest_io.get_absolute_breadcrumb_filesystem_paths(''))
        self.assertEqual(['', 'test'], pyntrest_io.get_absolute_breadcrumb_filesystem_paths('//test/'))
        self.assertEqual(['', 'test', 'test2'], pyntrest_io.get_absolute_breadcrumb_filesystem_paths('//test/test2/index.html'))

    def test_read_optional_album_metadata (self):
        ini_filename = '__info__.ini'
        self.assertRaises(TypeError, pyntrest_io.read_optional_album_metadata)
        self.assertRaises(TypeError, pyntrest_io.read_optional_album_metadata, 'asdasd_:asd')
        self.assertRaises(TypeError, pyntrest_io.read_optional_album_metadata, 'asdasd_:asd', '')
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata('', ini_filename)
        self.assertEqual(path.basename(path.abspath('')), a)
        self.assertEqual('', b)
        self.assertEqual(None, c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content = []
        dirname = self.create_temp_file_with_content(content, ini_filename )
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertEqual(path.basename(dirname), a)
        self.assertEqual('', b)
        self.assertEqual(None, c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('[AlbumInfo]')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertEqual(path.basename(dirname), a)
        self.assertEqual('', b)
        self.assertEqual(None, c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('Title=Pyntrest')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertEqual('Pyntrest', a)
        self.assertEqual('', b)
        self.assertEqual(None, c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('Description=Automated web photo albums for convenience lovers')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertEqual('Pyntrest', a)
        self.assertEqual('Automated web photo albums for convenience lovers', b)
        self.assertEqual(None, c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('CoverImage=im-001.jpg')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertEqual('Pyntrest', a)
        self.assertEqual('Automated web photo albums for convenience lovers', b)
        self.assertEqual('im-001.jpg', c)
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('ReverseImages=asdasd')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertFalse(d)
        self.assertFalse(e)
        self.assertFalse(f)
        del content[-1]
        content.append('ReverseImages=True')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertTrue(d)
        self.assertFalse(e)
        self.assertFalse(f)
        content.append('HideCover=asdasd')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertFalse(e)
        self.assertFalse(f)
        del content[-1]
        content.append('HideCover=True')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertTrue(e)
        self.assertFalse(f)
        content.append('ModifiedAlbumsOnTop=asdasd')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertFalse(f)
        del content[-1]
        content.append('ModifiedAlbumsOnTop=True')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        a, b, c, d, e, f, _ = pyntrest_io.read_optional_album_metadata(dirname, ini_filename )
        self.assertTrue(f)

    def test_read_optional_image_metadata (self):
        ini_filename = '__info__.ini'
        self.assertRaises(TypeError, pyntrest_io.read_optional_image_metadata)
        self.assertRaises(TypeError, pyntrest_io.read_optional_image_metadata, 'asdasd_:asd')
        self.assertRaises(TypeError, pyntrest_io.read_optional_image_metadata, 'asdasd_:asd', '')
        image_infos = pyntrest_io.read_optional_image_metadata('', ini_filename)
        self.assertEqual({}, image_infos)

        content = []
        dirname = self.create_temp_file_with_content(content, ini_filename )
        image_infos = pyntrest_io.read_optional_image_metadata(dirname, ini_filename )
        self.assertEqual({}, image_infos)

        content.append('[AlbumInfo]')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        image_infos = pyntrest_io.read_optional_image_metadata(dirname, ini_filename )
        self.assertEqual({}, image_infos)

        content.append('[ImageInfo]')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        image_infos = pyntrest_io.read_optional_image_metadata(dirname, ini_filename )
        self.assertEqual({}, image_infos)
        try:
            image_infos['sdoasdma'];
            self.fail()
        except KeyError:
            pass # Expected

        content.append('im-001.jpg=test-message')
        content.append('im-001.youtube.ini=test-message-2')
        content.append('im-002.jpg=       test-message-3    ')
        dirname = self.create_temp_file_with_content(content, ini_filename)
        image_infos = pyntrest_io.read_optional_image_metadata(dirname, ini_filename )
        self.assertNotEqual({}, image_infos)
        try:
            image_infos['sdoasdma'];
            self.fail()
        except KeyError:
            pass # Expected
        self.assertEqual('test-message', image_infos['im-001.jpg']);
        self.assertEqual('test-message', image_infos['IM-001.JPG'.lower()]);
        self.assertEqual('test-message-2', image_infos['im-001.youtube.ini']);
        self.assertEqual('test-message-3', image_infos['im-002.jpg']);

    def test_read_youtube_ini_file (self):
        ini_file = 'my-test.ini'
        self.assertRaises(TypeError, pyntrest_io.read_youtube_ini_file)
        self.assertRaises(TypeError, pyntrest_io.read_youtube_ini_file, 'asdasd_:asd')
        content = []
        dirname = self.create_temp_file_with_content(content, ini_file)
        filepath = path.join(dirname, ini_file)
        self.assertEqual('', pyntrest_io.read_youtube_ini_file(filepath))
        content.append('[VideoInfo]')
        dirname = self.create_temp_file_with_content(content, ini_file)
        filepath = path.join(dirname, ini_file)
        self.assertEqual('', pyntrest_io.read_youtube_ini_file(filepath))
        content.append('YoutubeId=rPmGtZAUxNs')
        dirname = self.create_temp_file_with_content(content, ini_file)
        filepath = path.join(dirname, ini_file)
        self.assertEqual('rPmGtZAUxNs', pyntrest_io.read_youtube_ini_file(filepath))

    def test_get_html_content(self):

        self.assertRaises(TypeError, pyntrest_io.get_html_content)
        self.assertRaises(TypeError, pyntrest_io.get_html_content, '')
        self.assertRaises(TypeError, pyntrest_io.get_html_content, 'nirvana.txt')

if __name__ == '__main__':
    unittest.main()
