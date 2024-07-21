from langchain_openai import ChatOpenAI


# memory config
MEMORY_LIMIT = 10

# brain config
LLM = ChatOpenAI(model="gpt-4o-mini")
NAME = 'Soda'
EMOTIONS = {'Fear': 0.0, 'Sadness': 0.0, 'Joy': 0.0, 'Disgust': 0.0, 'Anger': 0.0}

# stt config
STT_ON = False
STT_LANGUAGE = 'ko' # 'en

# tts config
TTS_ON = False
TTS_LANGUAGE = 'ko-KR' # 'en-US'
TTS_VOICE = 'ko-KR-SunHiNeural' # 'en-US-AshleyNeural'
TTS_RATE = '+10.00%'
TTS_PITCH = '+15.00%'