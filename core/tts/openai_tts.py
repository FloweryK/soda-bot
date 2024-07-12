from openai import OpenAI


class OpenaiTTS:
    def __init__(self, model, voice, speech_file_path="speech.wav"):
        self.client = OpenAI()
        self.model = model
        self.voice = voice
        self.speech_file_path = speech_file_path
    
    def synthesize(self, text):
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
        )
        response.stream_to_file(self.speech_file_path)