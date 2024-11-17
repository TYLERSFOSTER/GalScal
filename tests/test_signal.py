import os
import librosa
import soundfile as sf
import numpy as np
import pytest
from scipy.io import wavfile

import galscal



def detect_pitch(wav_file):
    data, samplerate = sf.read(wav_file)
    if len(data.shape) > 1:
        data = data[:, 0]
        
    pitches, magnitudes = librosa.piptrack(y=data, sr=samplerate, n_fft=4096, hop_length=512)
    
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:  # Avoiding zero (unvoiced)
            pitch_values.append(pitch)

    if pitch_values:
        return np.mean(pitch_values)
    else:
        return 0



@pytest.mark.parametrize("omega, answer", [
    (complex(1., 0.), 1.),
    (complex(0., 1.), complex(0., 1.)),
])
def test_Signal(omega, answer):
  signal = galscal.Signal(omega)

  assert signal.root == omega



@pytest.mark.parametrize("element_vec, field_vec, answer", [
    (np.array([1., 1., 1., 1.]), np.array([1., 0., 0., 0., 1.]), 1.),
])
def test_GalSignal(element_vec, field_vec, answer):
  element_poly = galscal.Polynomial(element_vec)
  field_poly = galscal.Polynomial(field_vec)

  alpha = complex(field_poly.roots()[0])  
  assert isinstance(alpha, complex)
  omega = element_poly.eval_at(alpha)

  signal = galscal.GalSignal(element_poly, field_poly)

  assert True



@pytest.mark.parametrize("omega, t, answer", [
    (complex(0., 2*np.pi), 1., 1.),
    (complex(1., 0.), 1., np.exp(complex(1., 0.))),
])
def test_eval_at(omega, t, answer):
  signal = galscal.Signal(omega)

  value = signal.eval_at(t)
  value = complex(round(value.real, 6), round(value.imag, 6))
  
  answer = complex(round(answer.real, 6), round(answer.imag, 6))
  assert value == answer



@pytest.mark.parametrize("save_path, interval, omega, samples_per_second, answer", [
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 44100, 44100),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 100, 100),
    ("TEST_FILE_TEST_FILE", (0., 2.), complex(0., 2*np.pi), 44100, 2 * 44100),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 4*np.pi), 44100, 44100),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 0.), 100, 100),
    ("TEST_FILE_TEST_FILE", (0., 2.), complex(-1., 4*np.pi), 44100, 2 * 44100),
])
def test_sav_wav_file_length(save_path, interval, omega, samples_per_second, answer):
  signal = galscal.Signal(omega)

  signal.save_wav(save_path, interval, samples_per_second=samples_per_second)
  sample_rate, saved_wav = wavfile.read(save_path)

  print("LENGTH:", saved_wav.shape)
  os.remove(save_path)

  assert saved_wav.shape[0] == answer



@pytest.mark.parametrize("save_path, interval, omega, samples_per_second, answer", [
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 44100, (1., -1.)),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 100, (1., -1.)),
    ("TEST_FILE_TEST_FILE", (0., 2.), complex(0., 2*np.pi), 44100, (1., -1.)),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 0.), 44100, (1., 1.)),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 0.), 100, (1., 1.)),
    ("TEST_FILE_TEST_FILE", (0., 2.), complex(-1., 0.), 44100, (1., 1.)),
])
def test_sav_wav_file_amplitudes(save_path, interval, omega, samples_per_second, answer):
  signal = galscal.Signal(omega)

  signal.save_wav(save_path, interval, samples_per_second=samples_per_second)
  sample_rate, saved_wav = wavfile.read(save_path)

  file_max = round(np.max(saved_wav)/np.iinfo(np.int16).max, 2)
  file_min = round(np.min(saved_wav)/np.iinfo(np.int16).max, 2)
  os.remove(save_path)

  assert file_max == answer[0] and file_min == answer[1]



@pytest.mark.parametrize("save_path, interval, omega, samples_per_second, pitch", [
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 44100, 666), # Mark of THE BEAST
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 44100, 440),
    ("TEST_FILE_TEST_FILE", (0., 1.), complex(0., 2*np.pi), 44100, 220),
])
def test_sav_wav_pitch(save_path, interval, omega, samples_per_second, pitch):
  signal = galscal.Signal(pitch * omega)

  signal.save_wav(save_path, interval, samples_per_second=samples_per_second)
  sample_rate, saved_wav = wavfile.read(save_path)

  wav_pitch = detect_pitch(save_path)
  os.remove(save_path)

  assert round(wav_pitch, 0) == pitch