
"""
    Module for the text preprocessing microservice.
"""

from typing import Optional, List
import logging
import json
import requests
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from etcd_registry import EtcdRegistry
import wave
import numpy as np
import librosa
import torch
import spacy
from spacy.lang.en import English
from functools import reduce


class TranscriptionError(Exception):
    """Raised when there is an error during transcription."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> str:
        return f"TranscriptionError: {self.message}"


class TextPreprocessingMicroservice:
    """
    Microservice that transcribes audio to text using the DeepSpeech 2 model, tokenizes the text into sentences,
    removes stop words, and applies stemming and lemmatization to the remaining words.
    """

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    def __init__(self, etcd_host: str, etcd_port: str, etcd_ttl: int):
        """
        Initializes the TextPreprocessing object.

        Args:
            etcd_host: str, hostname of etcd server
            etcd_port: str, port number of etcd server
            etcd_ttl: int, time-to-live for etcd key
        """
        self.etcd_registry = EtcdRegistry(etcd_host, etcd_port, etcd_ttl)

        # Get configuration from config_microservice
        config_url = f"http://{self.etcd_registry.get_service_url('config_microservice')}/config"
        headers = {"Content-Type": "application/json"}
        response = requests.get(config_url, headers=headers)
        response.raise_for_status()
        self.config = response.json()

        # Set configuration values
        self.audio_input = self.config['audio_input']
        self.silence_thresh = self.config['silence_thresh']
        self.silence_len = self.config['silence_len']
        self.question_detection_service = self.config.get('question_detection_service')
        self.sr = self.config["sr"]

        # Get logging microservice url from etcd_registry
        try:
            response = self.etcd_registry.get("/microservices/logging")
            self.logging_microservice_url = response.value.decode()
        except Exception as e:
            logging.error(f"Error occurred while getting logging_microservice_url from etcd_registry: {e}")
            self.logging_microservice_url = None

        # Load tokenizer and model from local file path
        model_path = self.config['model_path']
        tokenizer_path = self.config['tokenizer_path']
        self.tokenizer = Wav2Vec2Tokenizer.from_pretrained(tokenizer_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_path)

    def get_audio_segments(self, audio_file: str) -> List[np.ndarray]:
        """
        Splits the input audio file into segments based on silence.

        Args:
           audio_file: A string representing the path of the input audio file.

        Returns:
           A list of numpy arrays, each representing a segment of the input audio file.

        Raises:
           ValueError: If the input audio file is not valid.
        """
       # Load audio file
        try:
            audio, sr = librosa.load(audio_file, sr=self.sample_rate)
        except Exception as e:
            raise ValueError(f"Error occurred while reading audio file: {e}")

        # Split audio into segments based on silence
        segments = []
        chunks = librosa.effects.split(audio, top_db=self.silence_thresh, frame_length=self.frame_length,
                                       hop_length=self.hop_length)
        for chunk in chunks:
            segment = audio[chunk[0]:chunk[1]]
            if len(segment) >= self.min_segment_length:
                segments.append(segment)

        return segments
    def transcribe_audio(self, audio_file: str) -> str:
        """
        Transcribes the audio file to text using the DeepSpeech 2 model.

         Args:
             audio_file: str, path to the audio file to be transcribed.

         Returns:
             str: The transcribed text.

         Raises:
             ValueError: If audio_file is not a valid file path.
             TranscriptionError: If there is an error during transcription.
         """
        try:
            with wave.open(audio_file, "rb") as audio:
                audio_data = audio.readframes(-1)
                audio_rate = audio.getframerate()
                audio_width = audio.getsampwidth()
        except FileNotFoundError:
            raise ValueError(f"File {audio_file} not found.")
        except Exception as e:
            raise TranscriptionError(f"Error occurred while reading audio file: {e}")

        # Load the tokenizer and model
        tokenizer = Wav2Vec2Tokenizer.from_pretrained(self.tokenizer_path)
        model = Wav2Vec2ForCTC.from_pretrained(self.model_path)

         # Tokenize and encode the audio
        input_values = tokenizer(audio_data, return_tensors="pt").input_values

        # Transcribe the audio using the DeepSpeech 2 model
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = tokenizer.decode(predicted_ids[0])

        return transcription

    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenizes input text into sentences using Spacy.

        Args:
            text: A string of text to be tokenized.

        Returns:
            A list of strings, each representing a sentence in the input text.
        """
        # Parse text into Spacy Doc object
        doc = self.nlp(text)

        # Return list of sentence strings
        return [sent.text.strip() for sent in doc.sents]

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Removes stop words from a list of tokens.

        Args:
            tokens: List of tokens.

        Returns:
            List of tokens with stop words removed.
        """
        filtered_tokens = [token for token in tokens if not self.nlp.vocab[token].is_stop]
        return filtered_tokens

    def stemming_and_lemmatization(self, tokens: List[str]) -> List[str]:
        """
        Applies stemming and lemmatization to the input list of tokens.

        Args: tokens: A list of tokens.

        Returns: A list of stemmed and lemmatized tokens.
        """

        # Initialize spacy nlp object with English model
        nlp = spacy.load('en_core_web_sm')

        # Lemmatize and stem tokens
        processed_tokens = [token.lemma_.lower() for token in nlp(" ".join(tokens)) if not token.is_stop]

        return processed_tokens


    def preprocess_text(self, text):

        """
        Preprocesses the input text by transcribing any audio, tokenizing sentences, removing stopwords, and applying
        stemming and lemmatization to the remaining words.

        Args:
        text: A string representing the input text.

        Returns: A string representing the preprocessed text.

        Raises: TranscriptionError: If the input text contains an audio file that cannot be transcribed.
                ValueError: If the input text is not a valid string.
        """

        pipeline = [
            self.tokenize_text,
            self.remove_stopwords,
            self.apply_stemming_and_lemmatization
        ]

        return reduce(lambda x, f: f(x), pipeline, text)


    def setup(self):

        '''
            Sets up the text preprocessing microservice by registering with the etcd registry, loading configuration parameters, setting up the tokenizer and model, configuring logging to the logging microservice, and setting up the question detection microservice.
            This method should be called from the `run` method before the microservice starts listening for incoming requests.

            Returns: None.
        '''
        # Register microservice with etcd registry
        self.etcd_registry.register_service("text_preprocessing", "localhost", 8000)

        # Load configuration parameters from config microservice
        self.config = self.etcd_registry.get_config("text_preprocessing")

        # Load tokenizer and model
        self.tokenizer = Wav2Vec2Tokenizer.from_pretrained(self.config.tokenizer_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.config.model_path)

        # Set up logging to logging microservice
        log_host = self.etcd_registry.get_service_host("logging")
        log_port = self.etcd_registry.get_service_port("logging")
        log_url = f"http://{log_host}:{log_port}/log"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.handlers.HTTPHandler(log_url, method="POST"))

    def run(self):

        '''
            Runs the text_preprocessing microservice.
            This method is responsible for starting the microservice and handling incoming requests. It listens for requests
            on the specified port and route, and processes each request by transcribing the audio to text, tokenizing the text
            into sentences, removing stop words, and applying stemming and lemmatization to the remaining words. The resulting
            preprocessed text is then passed to the question_detection_microservice. All configuration information for the
            service is obtained from the config_microservice using Hydra.

            Returns: None.
        '''


        self.setup()

        # Run microservice
        while True:
            # Wait for request
            request = self.etcd_registry.get_request("text_preprocessing")

            # Process request
            audio_file = request["audio_file"]
            audio = AudioSegment.from_file(audio_file)

            segments = self.get_audio_segments(audio)
            transcriptions = [self.transcribe_audio(segment) for segment in segments]
            sentences = [self.tokenize_text(transcription) for transcription in transcriptions]
            sentences = list(chain.from_iterable(sentences))  # Flatten list of sentences
            sentences = [self.remove_stopwords(sentence) for sentence in sentences]
            sentences = [self.apply_stemming_and_lemmatization(sentence) for sentence in sentences]
            processed_text = self.preprocess_text(" ".join(sentences))

        # Send output to question detection microservice
        payload = {"text": processed_text}
        response = requests.post(qd_url, json=payload)

        # Send log to logging microservice
        log_payload = {
            "microservice": "text_preprocessing",
            "request": request,
            "response": response.json(),
            "processed_text": processed_text
        }
        logger.info(json.dumps(log_payload))

        # Store result in etcd registry
        self.etcd_registry.store_result(request["id"], processed_text)
