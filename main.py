from pydub import AudioSegment

from Manager import Manager
from iom.IOM import IOM
from Profile import Profile
from Map import Map
import logging
from speechbrain.pretrained import VAD
import pyaudio
import wave


logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(lineno)d | %(message)s')


def wake_word(name, iom):
    frame = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    path = 'testVoice.wav'
    vad = VAD.from_hparams(source="speechbrain/vad-crdnn-libriparty", savedir="pretrained_models/vad-crdnn-libriparty")

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format, channels=channels, rate=rate,
                    frames_per_buffer=frame, input=True)

    while True:
        frames = []
        print("silencly")
        for i in range(100):
            data = stream.read(frame)
            frames.append(data)
        wf = wave.open(path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        speeches = vad.get_speech_segments(path)
        if len(speeches) != 0:
            print("detect vad")
            audio = AudioSegment.from_wav(path)
            for speech in speeches:
                if speech[1].numpy() - speech[0].numpy() < 0.5:
                    continue
                else:
                    segment = audio[int(speech[0].numpy() * 1000): int(speech[1].numpy() * 1000)]
                    segment.export('temp.wav', format='wav')
                    print("sending to google ...")
                    command = iom.getListener().listenFile("temp.wav")
                    if name in command:
                        return True
            print("finish")


def run_ai():
    mapper = Map()
    logging.info('Mapper init ...')
    iom = IOM(mapper)
    logging.info('IOM init ...')
    profile = Profile(mapper)
    profile.readProfile()
    logging.info('Profile init ...')
    manager = Manager(profile, iom, mapper)
    manager.updateMap()
    logging.info('manager init ...')
    manager.getUtils()
    logging.info('utils init ...')
    sleep=True
    while True:
        if sleep:
            print("sleeping zzZ")
            wake_word('امیر', iom)
            sleep = False
        print("wakeup ...")
        # command = "سریال یلدا را از شبکه ۳ پخش کن"
        # path = iom.getScreen().record()
        command = iom.getListener().listenSilence()
        if command != "":
            sleep=True
        logging.debug(f"command: {command}")
        manager.query(command)
        # sys.exit()


run_ai()
