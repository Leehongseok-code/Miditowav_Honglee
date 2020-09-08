# Miditowav_Honglee
convert midi file to wav using python

## Requirements
numpy
pyaudio
fluidsynth
sounddevice
pretty_midi
scipy
pydub

## Usage
1.make your own directory to save instrumential files and input files. Each one's name should be 'Out' and 'Music'
2.put your midi files into Music folder, and write this code in your own code.
 
    from import  PyFluid import wavconverter
    wavcon=wavconverter()
    wavcon.midicomb(midi path,array of soundfont path,instrument index array)
    
instrument index array is used when you want to use General MIDI Soundfont.
You can find instrument index at here:
https://en.wikipedia.org/wiki/General_MIDI
    
## Example
    from import  PyFluid import wavconverter
    wavcon=wavconverter()
    wvcon.midicomb('./Music/hotcandy.mid',['C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2','C:\Users\User\Desktop\FluidR3_GM\FluidR3_GM.sf2'
                                ])
    
