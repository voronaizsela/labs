import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import signal

amplitude_st = 1.0
frequency_st = 1.0
phase_st = 0.5
noisemean_st = 0.0
noisecov_st = 0.1
sigma_st = 2
t = np.linspace(0, 10, 1000)  
noise_value = np.random.normal(noisemean_st, noisecov_st, size=1000)

def harmonic(t, amplitude, frequency, phase, show_noise, sigma):
    clean_harmonic = amplitude * np.sin(frequency * t + phase)
    if show_noise:
        noisy_harmonic = clean_harmonic + noise_value
        return noisy_harmonic
    else:
        return clean_harmonic

def update(val):
    amplitude = amp_sl.val
    frequency = freq_sl.val
    phase = phase_sl.val
    show_noise = noise_cb.get_status()[0]
    sigma = sigma_sl.val
    
    plot1.set_ydata(harmonic(t, amplitude, frequency, phase, show_noise, 0))
    
    filtered = harmonic(t, amplitude, frequency, phase, show_noise, sigma)
    window = signal.windows.gaussian(len(filtered), sigma)
    filtered_harmonic = signal.convolve(filtered, window / window.sum(), mode='same')
    plot2.set_ydata(filtered_harmonic)
    plt.draw()

def update_noise(val):
    noisemean = noisemean_sl.val
    noisecov = noisecov_sl.val
    global noise_value
    noise_value = np.random.normal(noisemean, noisecov, size=1000)
    update(None)

def reset(event):
    amp_sl.reset()
    freq_sl.reset()
    phase_sl.reset()
    noisemean_sl.reset()
    noisecov_sl.reset()
    sigma_sl.reset()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
plt.subplots_adjust(left=0.18, bottom=0.4, right=0.7, top=0.9, hspace=0.5)

# ПЕРШИЙ ГРАФІК
plot1, = ax1.plot(t, harmonic(t, amplitude_st, frequency_st, phase_st, True, 0), color='mediumorchid')
ax1.set_title('Графік гармоніки')

# ДРУГИЙ ГРАФІК
filtered_harmonic_initial = harmonic(t, amplitude_st, frequency_st, phase_st, True, sigma_st)
window = signal.windows.gaussian(len(filtered_harmonic_initial), sigma_st)
filtered_harmonic_manual_initial = signal.convolve(filtered_harmonic_initial, window / window.sum(), mode='same')
plot2, = ax2.plot(t, filtered_harmonic_manual_initial, color='mediumorchid')
ax2.set_title('Відфільтрований графік гармоніки')

# СЛАЙДЕРИ + КНОПКИ
amp_slx = plt.axes([0.16, 0.3, 0.65, 0.03])
amp_sl = Slider(amp_slx, 'Амплітуда(A)', 0.1, 10.0, valinit=amplitude_st, color='palegreen')
amp_sl.on_changed(update)

freq_slx = plt.axes([0.16, 0.25, 0.65, 0.03])
freq_sl = Slider(freq_slx, 'Частота(ω)', 0.1, 10.0, valinit=frequency_st, color='palegreen')
freq_sl.on_changed(update)

phase_slx = plt.axes([0.16, 0.2, 0.65, 0.03])
phase_sl = Slider(phase_slx, 'Фаза(φ)', 0, 2*np.pi, valinit=phase_st, color='palegreen')
phase_sl.on_changed(update)

noisemean_slx = plt.axes([0.16, 0.15, 0.65, 0.03])
noisemean_sl = Slider(noisemean_slx, 'Амплітуда шуму', -1.0, 1.0, valinit=noisemean_st, color='turquoise')
noisemean_sl.on_changed(update_noise)

noisecov_slx = plt.axes([0.16, 0.1, 0.65, 0.03])
noisecov_sl = Slider(noisecov_slx, 'Дисперсія', 0.0, 1.0, valinit=noisecov_st, color='turquoise')
noisecov_sl.on_changed(update_noise)

sigma_slx = plt.axes([0.16, 0.05, 0.65, 0.03])
sigma_sl = Slider(sigma_slx, 'Сігма (Гаус)', 0, 10, valinit=sigma_st, color='mediumpurple')
sigma_sl.on_changed(update)

noisex = plt.axes([0.85, 0.7, 0.11, 0.1])
noise_cb = CheckButtons(noisex, ['Показати шум'], [True])
noise_cb.on_clicked(update)

resetx = plt.axes([0.85, 0.65, 0.11, 0.04])
reset_button = Button(resetx, 'Скинути', color='plum')
reset_button.on_clicked(reset)

plt.show()