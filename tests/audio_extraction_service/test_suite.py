import unittest
from unittest.mock import patch, MagicMock
from audio_extraction_microservice import AudioExtractor

class TestAudioExtractor(unittest.TestCase):

    @patch('audio_extraction_microservice.requests.get')
    def test_download_file(self, mock_get):
        url = "http://example.com/test.mp3"
        mock_response = MagicMock()
        mock_response.content = b"test"
        mock_get.return_value = mock_response

        ae = AudioExtractor(url)
        ae.download_file()

        mock_get.assert_called_with(url, stream=True)
        ae.file_path = "/home/bbrelin/src/repos/mednotes/data/audio_input/test.mp3"
        with open(ae.file_path, "rb") as f:
            contents = f.read()
        self.assertEqual(contents, b"test")

    def test_extract_audio(self):
        input_file_path = "/home/bbrelin/src/repos/mednotes/data/audio_input/test.mp4"
        output_file_path = "/home/bbrelin/src/repos/mednotes/data/audio_input/test.mp3"

        ae = AudioExtractor("")
        ae.extract_audio(input_file_path, output_file_path)

        with open(output_file_path, "rb") as f:
            contents = f.read()
        self.assertNotEqual(contents, b"")
        self.assertTrue(len(contents) > 0)

if __name__ == '__main__':
    unittest.main()

