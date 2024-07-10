import os
import azure.cognitiveservices.speech as speechsdk


class TTS:
    VOICE_NAME = "en-US-AshleyNeural"
    PITCH = "+20.00%"

    def __init__(self):
        # configs
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get('AZURE_SPEECH_KEY'), 
            region=os.environ.get('AZURE_SPEECH_REGION')
        )
        audio_config = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True,
            # filename=filename
        )

        # synthesizer
        self.synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )

    def synthesize(self, text):
        ssml_string = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{self.VOICE_NAME}">
                <prosody pitch="{self.PITCH}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """

        # get results
        response = self.synthesizer.speak_ssml_async(ssml_string).get()

        # response handling
        if response.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            pass
        elif response.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = response.cancellation_details
            print(f"Speech synthesis canceled:", cancellation_details.reason)

            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details:", cancellation_details.error_details)
                    print("Did you set the speech resource key and region values?")