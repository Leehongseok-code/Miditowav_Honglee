import time
import numpy
import pyaudio
import fluidsynth
import wave
import mido
import sounddevice as sd
import string
import pretty_midi
from scipy.io.wavfile import write
from playsound import playsound
from audio2numpy import open_audio
from pydub import AudioSegment

def snotetodict(mid,i):
    ndict={}
    instrument=mid.instruments[i]
    for note in instrument.notes:
        temp=[]
        ndict[note.start]=temp
    for note in instrument.notes:
        ndict[note.start].append(note)
    return ndict

def enotetodict(mid,i):
    ndict = {}
    instrument = mid.instruments[i]
    for note in instrument.notes:
        temp = []
        ndict[note.end] = temp
    for note in instrument.notes:
        ndict[note.end].append(note)
    return ndict

def nnotetodict(mid,i):
    ndict={}
    instrument = mid.instruments[i]
    for note in instrument.notes:
        temp=[]
        ndict[note.start]=temp
    for note in instrument.notes:
        temp = []
        ndict[note.end] = temp
    for note in instrument.notes:
        ndict[note.end].append(note)
    for note in instrument.notes:
        ndict[note.start].append(note)





    return ndict

def isSameNote(note1,note2):
    if note1.start==note2.start and note1.end==note2.end and note1.pitch==note2.pitch:
        return True
    else:
        return False

def miditowav(inst,mid,sf):
    #mid = pretty_midi.PrettyMIDI('./Music/kkhouse.mid') #1


    pa = pyaudio.PyAudio()
    sd.query_devices()
    strm = pa.open(
        format = pyaudio.paInt16,
        channels = 2,
        rate = 44100,
        output = True)

    s = []


    #result_array = mid2arry(mid)


    #selecting soundfont
    fl = fluidsynth.Synth()
    # Initial silence is 1 second
    #s = numpy.append(s, fl.get_samples(44100 * 1))
    #fl.start('dsound')
    sfid = fl.sfload(r'C:\Users\User\Desktop\FluidR3_GM\yk.sf2')
    sfid = fl.sfload(sf)
    #selecting instrumnet
    fl.program_select(0, sfid, 0, 0)


    startdict=snotetodict(mid,inst)
    enddict=enotetodict(mid,inst)

    #notedict=startdict.copy()
    #notedict.update(enddict)
    notedict=nnotetodict(mid,inst)

    instrument=mid.instruments[inst]
    startarr=[]
    endarr=[]
    for note in instrument.notes:
        startarr.append(note.start)
        endarr.append(note.end)

    startkey=startdict.keys()
    startkey.sort()
    endkey=enddict.keys()
    endkey.sort()

    #delete same notes in notekey
    notekey=startkey+endkey
    notekey=set(notekey)
    notekey=list(notekey)
    notekey.sort()
    #print notekey


    print len(startarr),len(endarr)

    fl.noteon(0,0,0)
    fl.noteon(0, 30, 98)
    s = numpy.append(s, fl.get_samples(int(44100 * 1 / 2)))
    s = numpy.append(s, fl.get_samples(int(44100 * notekey[0]/2)))
    playtime = {}
    #print notedict
    print mid.instruments[inst]

    for note in instrument.notes:
        fl.noteon(0,note.pitch,98)
        s = numpy.append(s, fl.get_samples(int(44100 * 1/2)))
        #fl.noteoff(0,0)
    fl.delete()

    samps = fluidsynth.raw_audio_string(s)

    print (len(s))
    print ('Starting playback')
    #strm.write(samps)

    scaled = numpy.int16(s/numpy.max(numpy.abs(s)) * 32767)
    name='./Out/inst'+str(inst)+'.wav'
    write(name, 44100, scaled)
    #playsound(name)

def midicomb(midifile,sf):
    mid = pretty_midi.PrettyMIDI(midifile)
    midarr=[]
    for j in range(len(mid.instruments)):
        if j<len(sf):
            miditowav(j,mid,sf[j])
        else:
            miditowav(j,mid,'C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2')
    for j in range(len(mid.instruments)):
        midarr.append(AudioSegment.from_wav('./Out/inst'+str(j)+'.wav'))
    combined = midarr[0]
    for j in range(len(mid.instruments)):
        combined = combined.overlay(midarr[j])
    combined.export("joinedFile.wav", format="wav")

midicomb('./Music/raindropflower.mid',['C:\Users\User\Desktop\FluidR3_GM\Book.sf2','C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2','C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2'])
#mid=pretty_midi.PrettyMIDI('./Music/raindropflower.mid')
#miditowav(1,mid)
