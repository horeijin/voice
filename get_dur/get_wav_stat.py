#
import os
import sys

import soundfile
import librosa
import numpy as np


def get_wav_duration_info(wav_fn):
    audio, sr = soundfile.read(wav_fn)
    audio = audio.T
    audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    spec = librosa.stft(y=audio, n_fft=int(1024), hop_length=int(160))
    mag = np.absolute(spec)

    energy = np.mean(mag, axis=0)
    # spd
    epd_energy_th = 0.15
    spd_frame = 0
    for i in range(len(energy)):
        if energy[i] > epd_energy_th:
            spd_frame = i
            break
    # epd
    epd_frame = len(energy)
    for i in reversed(range(epd_frame)):
        if energy[i] > epd_energy_th:
            epd_frame = i
            break

    spd_time = float(spd_frame) * 0.01
    epd_time = float(epd_frame) * 0.01
    return spd_time, epd_time


## main

if __name__ == "__main__":
    if len(sys.argv) == 2:
        celeb_name = sys.argv[1]
    else:
        print("Usage: python %s <celeb_name>".format(sys.argv[0]))
        print("Example: python %s Jone".format(sys.argv[0]))
        sys.exit(1)

    synth_dir = './synth/' + celeb_name
    filelist = os.listdir(synth_dir)
    filelist_wav = [file for file in filelist if celeb_name in file]

    out_str = ''
    for file in filelist_wav:
        wav_fn = synth_dir + "/" + file
        start_time, end_time = get_wav_duration_info(wav_fn)
        duration = end_time - start_time
        out_str += "{:.3f} {:.3f} {:.3f}\n".format(start_time, end_time, duration)

    out_fn = "./duration_" + celeb_name + ".txt"
    fp = open(out_fn, 'w')
    fp.write(out_str)
    fp.close()
