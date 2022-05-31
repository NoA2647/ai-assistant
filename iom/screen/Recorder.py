import tkinter as tk
import threading
import pyaudio
import wave


class Recorder:
    frame = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100

    def __init__(self, master, path):
        self.path = path
        self.stream = None
        self.p = None
        self.frames = []
        self.t = threading.Thread(target=self.record)
        self.master = master
        self.isRecording = False
        self.button1 = tk.Button(self.master, text='rec', command=self.startRecording)
        self.button2 = tk.Button(self.master, text='stop', command=self.stopRecording)

        self.button1.pack()
        self.button2.pack()

    def startRecording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.rate,
                                  frames_per_buffer=self.frame, input=True)
        self.isRecording = True

        print('Recording ...')
        self.t.start()

    def stopRecording(self):
        if self.isRecording:
            self.isRecording = False
            print('recording complete')
            wf = wave.open(self.path, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            if self.t.is_alive():
                self.t.join()
            self.master.destroy()

    def record(self):
        while self.isRecording:
            data = self.stream.read(self.frame)
            self.frames.append(data)
