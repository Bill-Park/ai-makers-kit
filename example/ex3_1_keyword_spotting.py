import audioop  
from ctypes import * 
import ktkws # KWS  
import MicrophoneStream as MS  
KWS_KEYWORDS = ['기가지니', '지니야', '친구야', '자기야']  
  
RATE = 16000  
CHUNK = 512  

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def detect_wake_up_word(keyword = '기가지니'): 
  if not keyword in KWS_KEYWORDS:
    return False
        
  response_code = ktkws.init("../data/kwsmodel.pack")  
  print ('response_code on init = %d' % (response_code))  
  response_code = ktkws.start()  
  print ('response_code on start = %d' % (response_code))  
  print ('\n호출어를 불러보세요~\n')  
  ktkws.set_keyword(KWS_KEYWORDS.index(keyword))
  
  with MS.MicrophoneStream(RATE, CHUNK) as stream:  
    audio_generator = stream.generator()  
  
    for content in audio_generator:  
      response_code = ktkws.detect(content)  
  
      if (response_code == 1):  
        MS.play_file("../data/sample_sound.wav")
        print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')  
        ktkws.stop()
        return True


if __name__ == "__main__":
  detect_wake_up_word()
