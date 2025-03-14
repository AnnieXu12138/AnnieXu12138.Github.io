import pyaudio
import threading
import time
import wave
import speech_recognition as sr
from crystalball import openai_send2

class AudioRecorder():
    AUDIO_RATE = 48000        
    AUDIO_CHANNEL = 1         
    AUDIO_CHUNK_SIZE = 1024   
    AUDIO_FORMAT = pyaudio.paInt16 
    AUDIO_FILE = "output.wav" 


    def __init__(self, dev_index:int=0):

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.is_ready_stop = False 
        self.dev_index = dev_index
        pass


    def start_recoding(self)->None:
        
        recording_thread = threading.Thread(target=self.start_recording_back_worker)
        recording_thread.start()
        pass


    def start_recording_back_worker(self, rate=AUDIO_RATE, channels=AUDIO_CHANNEL, chunk_size=AUDIO_CHUNK_SIZE)->None:
        
        
        self.stream = self.audio.open(format = AudioRecorder.AUDIO_FORMAT,
                                    channels = channels,
                                    rate = rate,
                                    input = True,
                                    input_device_index = self.dev_index,
                                    frames_per_buffer = chunk_size)
        
        print("Recording starts...")

    
        self.frames = []


        self.is_recording = True
        self.is_ready_stop = False


        while self.is_recording:
            data = self.stream.read(chunk_size)
            self.frames.append(data)

        self.is_ready_stop = True
        print("Stop recording...")
        pass


    def stop_recording(self, filename:str=AUDIO_FILE)->bool:
        if not self.is_recording:
            print("No recording is in progress and recording cannot be stopped.")
            return False

        
        self.is_recording = False
        while not self.is_ready_stop:
            time.sleep(0.01)
        
        
        self.stream.stop_stream()
        self.stream.close()

        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(AudioRecorder.AUDIO_CHANNEL)  
            wf.setsampwidth(self.audio.get_sample_size(AudioRecorder.AUDIO_FORMAT))  
            wf.setframerate(AudioRecorder.AUDIO_RATE)  
            wf.writeframes(b''.join(self.frames))  

        print(f"The recording is finished and the file has been saved as {filename}")
        return True


    def recognize_audio_by_google(self, filename:str=AUDIO_FILE)->str|None:
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(filename) as source:
                print("Recognizing the audio...")
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='en-US')
                print("Result ", text)
                return text
        except sr.UnknownValueError:
            print("Can't revognize the audio")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None
        except:
            print("Error")
            return None
        pass


    def terminate(self):
        self.audio.terminate()

if __name__ == "__main__":
    audio_recorder = AudioRecorder()

    audio_recorder.start_recoding()
    
    # 延时5秒接收录音（由于录音使用了线程方式，所以无法
    # 使用【except KeyboardInterrupt】捕获到Ctrl+C事件
    time.sleep(5)

    if (audio_recorder.stop_recording()):
        text = audio_recorder.recognize_audio_by_google()
        print(text)
        result = openai_send2(text)
        print(result)

        audio_recorder.terminate()
    else:
        print("Error！")
    
    