import audioop
from ctypes import *
import MicrophoneStream as MS
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import MicrophoneStream as MS
import user_auth as UA
import os

HOST = 'gate.gigagenie.ai'
PORT = 4080

RATE = 16000
CHUNK = 512

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def generate_request():
  with MS.MicrophoneStream(RATE, CHUNK) as stream:
    audio_generator = stream.generator()

    for content in audio_generator:
      message = gigagenieRPC_pb2.reqVoice()
      message.audioContent = content
      yield message

def get_grpc_stub():
  channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
  stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

  return stub

def get_voice_from_text(text, output_file_name = 'tts.wav'):
  stub = get_grpc_stub()

  message = gigagenieRPC_pb2.reqText()
  message.lang = 1
  message.mode = 0
  message.text = text

  with open(output_file_name, 'wb') as output:
    for response in stub.getText2VoiceStream(message):
      result_code = response.resOptions.resultCd
      print ("\n\n음성합성 응답 상태코드:", result_code)

      if result_code == 200 or result_code == 0:
        output.write(response.audioContent)
      else:
        return False

  return True

def get_voice_and_speech(text):
  result_code = get_voice_from_text(text)
  if result_code:
    MS.play_file('tts.wav')
    print('음성이 출력되었습니다.')
  else:
    print('에러가 발생하였습니다.')

if __name__ == '__main__':
  get_voice_and_speech('안녕하세요, 기가지니입니다.')
