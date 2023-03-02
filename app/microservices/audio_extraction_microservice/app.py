import os
import subprocess
from typing import Optional
from etcd_registry import EtcdRegistry
import requests
from hydra import compose, initialize

with initialize(config_path="../../../config"):
    cfg = compose("mednotes")

class AudioExtractor:
    def __init__(self, etcd_host: str, etcd_port: str, etcd_ttl: int, audio_input: str = cfg.audio_input, save_video: Optional[bool] = None):
        """
        Initialize AudioExtractor object

        :param etcd_host: str, hostname of etcd server
        :param etcd_port: str, port number of etcd server
        :param etcd_ttl: int, time-to-live for etcd key
        :param audio_input: str, path to directory to save audio files to
        :param save_video: bool, whether to save the original video file after extracting audio
        """
        self.audio_input = audio_input
        self.save_video = save_video or os.getenv('SAVE_VIDEO') or False
        self.etcd_registry = EtcdRegistry(etcd_host, etcd_port, etcd_ttl)
        self.text_preprocessing_service = self.etcd_registry.get_service(cfg.microservices.text_preprocessing.name)

    def download_file(self, url: str) -> str:
        """
        Downloads file from given URL and returns the file path

        :param url: str, URL to download file from
        :return: str, path to downloaded file
        """
        if 'youtube.com' in url or 'you.tube.com' in url:
            print(f'Downloading audio from YouTube video at {url}...')
            command = f'youtube-dl -x --audio-format mp3 {url}'
        else:
            print(f'Downloading audio from file at {url}...')
            command = f'wget {url}'

        # Generate a unique file name
        file_name = f'{os.path.splitext(os.path.basename(url))[0]}_{os.getpid()}.mp3'
        file_path = os.path.join(self.audio_input, file_name)

        # Download file
        subprocess.run(f'{command} -O {file_path}', shell=True, check=True)

        return file_path

    def extract_audio(self, file_path: str):
        """
        Extracts audio from given video file path and saves to self.audio_input directory

        :param file_path: str, path to video file to extract audio from
        """
        if not os.path.isfile(file_path):
            raise ValueError(f'Invalid file path: {file_path}')

        print(f'Extracting audio from {file_path}...')

        # Generate a unique file name
        file_name = f'{os.path.splitext(os.path.basename(file_path))[0]}_{os.getpid()}.mp3'
        audio_file_path = os.path.join(self.audio_input, file_name)

        # Extract audio and save to audio_file_path
        command = f'ffmpeg -i {file_path} -vn -acodec libmp3lame -ar 44100 -ac 2 {audio_file_path}'
        subprocess.run(command, shell=True, check=True)

        if not self.save_video:
            # Delete video file
            os.remove(file_path)

        # Send extracted audio file path to text preprocessing microservice
        if self.text_preprocessing_service:
            audio_file_name = os.path.basename(audio_file_path)
            audio_file_url = f"http://{os.environ['HOSTNAME']}:{cfg.ports.audio_server_port}/audio/{audio_file_name}"
            data = {"audio_file_url": audio_file_url}
            headers = {"Content-Type": "application

