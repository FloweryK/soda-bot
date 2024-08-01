from langchain_community.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI


# memory config
SAVE_DIR = 'chat_history/'
SHORT_TERM_LIMIT = 10

# brain config
LLM = ChatOllama(model="mistral-nemo", temperature=1.0)
# LLM = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)
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