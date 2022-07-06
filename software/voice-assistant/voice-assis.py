################ Henri Lahousse ################
# voice assistant
# 05/31/2022

# libraries
import struct              
import pyaudio            
import pvporcupine        # for wakeword
import pvrhino            # for situations

porcupine = None
pa = None
audio_stream = None
rhino = None


# documentation picovoice https://picovoice.ai/docs/
# create model wakeword   https://console.picovoice.ai/ppn
# create model situation  https://console.picovoice.ai/rhn

access_key = 'ENTER_KEY'          # find on picovoice website  https://console.picovoice.ai/access_key // my_key 0nevFcYH3LlyYTajYWkG44d+vLWdm5Njxe8tr6xNrj/Kn9/m2qOjeg==

def voice_ass():
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=['ENTER_PATH']  # download model from website and extract file for wakeword detection  // my_path /home/pi/Downloads/wakeword.ppn
    )

    # setup
    def setup(path):
        rhino = pvrhino.create(
            access_key=access_key,
            context_path=path)
        return rhino

    rhino_drive = setup('ENTER_PATH')               # download model from website and extract for situation recognission // /home/pi/Downloads/drive.rhn
    rhino_roof = setup('ENTER_PATH')                # =  // /home/pi/Downloads/roof.rhn
    rhino_smartlights = setup('ENTER_PATH')         # = // /home/pi/Downloads/smartlights.rhn

    pa = pyaudio.PyAudio()

    # prepare audio for processing
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

    # prepare audio for processing
    def audio(rhino):
        audio_stream_rhn = pa.open(
            rate=rhino.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=rhino.frame_length)
        return audio_stream_rhn

    audio_sm = audio(rhino_smartlights)
    audio_rf = audio(rhino_roof)
    audio_dr = audio(rhino_drive)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        
        # finalizing audio
        def fin(aud, rhino):
            rh = aud.read(rhino.frame_length)
            rh = struct.unpack_from("h" * rhino.frame_length, rh)
            is_finalized = rhino.process(rh)
            return is_finalized

        is_fin_sm = fin(audio_sm, rhino_smartlights)
        is_fin_rf = fin(audio_rf, rhino_roof)
        is_fin_dr = fin(audio_dr, rhino_drive)
 
        # results, get the understood situation returned
        def rs(is_fin, rhino):
            if is_fin:
                inference = rhino.get_inference()  # if if_fin is True we get the inference
                if inference.is_understood:  # use intent and slots if it understands
                    intent = inference.intent  # intent is a string
                    slots = inference.slots  # slots is a dictionary
                    return intent, slots
        
        # returns wakeword
        if keyword_index == 0:
            return 1

        rs(is_fin_sm, rhino_smartlights)
        rs(is_fin_rf, rhino_roof)
        rs(is_fin_dr, rhino_drive)

    porcupine.delete()
    rhino.delete()
