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


class wavconverter:
    maxendtime=0
    maxendindex=0
    def miditowav(self,inst,mid,sf,inst_index=0):
        #mid = pretty_midi.PrettyMIDI('./Music/kkhouse.mid') #1

        pa = pyaudio.PyAudio()
        sd.query_devices()
        strm = pa.open(
            format = pyaudio.paInt16,
            channels = 2,
            rate = 44100,
            output = True)

        s = []

        #selecting soundfont
        fl = fluidsynth.Synth()
        # Initial silence is 1 second
        #s = numpy.append(s, fl.get_samples(44100 * 1))
        #fl.start('dsound')
        #sfid = fl.sfload(r'C:\Users\User\Desktop\FluidR3_GM\yk.sf2')
        #sfid = fl.sfload(sf)
        #selecting instrumnet
        fl.program_select(0, sfid, 0, inst_index)


        startdict=snotetodict(mid,inst)
        enddict=enotetodict(mid,inst)

        #notedict=startdict.copy()
        #notedict.update(enddict)
        notedict=nnotetodict(mid,inst)

        instrument=mid.instruments[inst]
        print instrument.is_drum
        '''
        if instrument.is_drum==True:
            sfid=fl.sfload('C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2')
            fl.program_select(10, sfid, 0, 35)
        '''

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

        print inst,len(startarr),len(endarr)

        fl.noteon(0,0,0)
        s = numpy.append(s, fl.get_samples(int(44100 * notekey[0]/2)))
        playtime = {}
        notekey.append(notekey[len(notekey)-1]+1)
        for i in range(len(notekey)-1):

            term=0
            pl = 0

            '''
            for note in notedict[notekey[i]]:
                if notekey[i] == note.start:
                    fl.noteon(0, note.pitch, note.velocity)
                    playtime=note.end-note.start
                    print notekey[i],note.pitch,'start'
                elif notekey[i] == note.end:
                    s = numpy.append(s, fl.get_samples(int(44100 * playtime / 2)))
                    fl.noteoff(0, note.pitch)
                    print notekey[i],note.pitch, 'end'
            '''
            #print notekey[i],notedict[notekey[i]]
            for j in range(len(notedict[notekey[i]])):
                note=notedict[notekey[i]][j]
                #print "i:",i,"inst:",inst,note
                if notekey[i] == note.start:
                    #beacuse fluidsynth can't make note which have pitch more than 88(when sf is koto)
                    if note.pitch>120:
                        fl.noteon(0, note.pitch-12, note.velocity)
                    # beacuse fluidsynth can't make note which have pitch lee than 48(when sf is koto)
                    #elif note.pitch<48:
                        #fl.noteon(0,note.pitch+12,note.velocity)
                    else:
                        fl.noteon(0, note.pitch, note.velocity)
                elif notekey[i] == note.end:
                    fl.noteoff(0, note.pitch)
                    p=0
            term = notekey[i+1] - notekey[i]
            s = numpy.append(s, fl.get_samples(int(44100 * term/2)))
        fl.delete()

        samps = fluidsynth.raw_audio_string(s)

        print (len(s))
        print ('Starting playback')
        #strm.write(samps)

        #scaled = numpy.int16(s/numpy.max(numpy.abs(s)) * 32767)
        scaled = numpy.int16(s*0.8 / numpy.max(numpy.abs(s)) * 32767)
        name='./Out/inst'+str(inst)+'.wav'
        write(name, 44100, scaled)
        #playsound(name)
        if self.maxendtime<notekey[len(notekey)-1]:
            self.maxendtime=max(notekey[len(notekey)-1],self.maxendtime)
            self.maxendindex=inst

    #mix many inst.wav to full music using pydub
    def midicomb(self,midifile,sf,inst_index=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
        mid = pretty_midi.PrettyMIDI(midifile)
        #print mid.instruments
        midarr=[]
        for j in range(len(mid.instruments)):
            if j<len(sf):
                if j<len(inst_index):
                    self.miditowav(j,mid,sf[j],inst_index[j])
                else:
                    self.miditowav(j, mid, sf[j])
            else:
                self.miditowav(j,mid,'C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2')
        for j in range(len(mid.instruments)):
            midarr.append(AudioSegment.from_wav('./Out/inst'+str(j)+'.wav'))
        combined = midarr[self.maxendindex]
        for j in range(len(mid.instruments)):
            combined = combined.overlay(midarr[j])
        combined.export("Output.wav", format="wav")


