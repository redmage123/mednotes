import os
import subprocess
import requests
import logging
from typing import Optional
from etcd import Client as EtcdClient

logger = logging.getLogger(__name__)

class AudioExtractionMicroservice:
    """
    Microservice to extract audio from a video file and send the path to the extracted audio file to the text
    preprocessing microservice for further processing.
    """

    def __init__(self, etcd_host: str, etcd_port: str, etcd_ttl: int, audio_input: str, save_video: Optional[bool] = None):
        """
        Constructor for the AudioExtractionMicroservice class.

        :param etcd_host: str, hostname of the etcd server
        :param etcd_port: str, port number of the etcd server
        :param etcd_ttl: int, time-to-live for etcd key
        :param audio_input: str, path to directory to save audio files to
        :param save_video: bool, whether to save the original video file after extracting audio
        """
        self.audio_input = audio_input
        self.save_video = save_video or os.getenv('SAVE_VIDEO') or False

        # Connect to etcd server
        self.etcd_client = EtcdClient(host=etcd_host, port=etcd_port)
        self.etcd_ttl = etcd_ttl
        self.register_microservice()

        # Initialize microservices URLs
        self.config_microservice_url = None
        self.logging_microservice_url = None
        self.text_preprocessing_service_url = None

        # Get microservices URLs from etcd
        self.get_microservice_urls()

    def register_microservice(self):
        """
        Registers the audio extraction microservice with the etcd server.
        """
        self.etcd_client.put(f"/microservices/audio_extraction_microservice/{os.getenv('HOSTNAME')}:{os.getenv('PORT')}", f"{os.getenv('HOSTNAME')}:{os.getenv('PORT')}", ttl=self.etcd_ttl)
        logger.info("Audio Extraction Microservice registered with Etcd server.")

    def get_microservice_urls(self):
        """
        Retrieves the URLs for the config, logging, and text preprocessing microservices from the etcd server.
        """
        try:
            response = self.etcd_client.get("/microservices/config")
            self.config_microservice_url = response.value.decode()
            logger.info(f"Retrieved config_microservice_url: {self.config_microservice_url}")
        except Exception as e:
            logger.error(f"Error occurred while retrieving config_microservice_url: {e}")

        try:
            response = self.etcd_client.get("/microservices/logging")
            self.logging_microservice_url = response.value.decode()
            logger.info(f"Retrieved logging_microservice_url: {self.logging_microservice_url}")
        except Exception as e:
            logger.error(f"Error occurred while retrieving logging_microservice_url: {e}")

        try:
            response = self.etcd_client.get("/microservices/text_preprocessing")
            self.text_preprocessing_service_url = response.value.decode()
            logger.info(f"Retrieved text_preprocessing_service_url: {self.text_preprocessing_service_url}")
        except Exception as e:
            logger.error(f"Error occurred while retrieving text_preprocessing_service_url: {e}")

    def download_file(self, url: str) -> str:
        """
        Downloads file from the given URL and returns the file path.

        :param url: str, URL to download file from
        :return: str, path to downloaded file
        """
        output_file_path = os.path.join(self.audio_input, 'audio_file')
subprocess.run(['wget', '-O', output_file_path, url])
return output_file_path

def extract_audio(self, url: str) -> str:
    """
    Download the video file from the given URL, extract the audio, and send the path to the extracted audio file to
    the text preprocessing microservice.

    :param url: str, URL to download video from
    :return: str, path to extracted audio file
    """
    file_path = self.download_file(url)
    output_file_path = os.path.join(self.audio_input, 'extracted_audio.wav')
    subprocess.run(['ffmpeg', '-i',
                    file_path,
                    '-vn',
                    '-ar', '44100',
                    '-ac', '2',
                    '-b:a', '192k',
                    output_file_path], check=True)

    # make REST call to text_preprocessing microservice
    if self.text_preprocessing_service_url is not None:
        try:
            response = requests.post(self.text_preprocessing_service_url, data={'audio_path': output_file_path})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to make REST call to text_preprocessing service: {e}")

    return output_file_path

