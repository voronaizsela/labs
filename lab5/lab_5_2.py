import dash
from dash import dcc, html, Input, Output, State
import numpy as np
import plotly.graph_objs as go

amplitude_st = 1.0
frequency_st = 1.0
phase_st = 0.5
noisemean_st = 0.0
noisecov_st = 0.1
sigma_st = 2
t = np.linspace(0, 10, 1000)
noise_value = np.random.normal(noisemean_st, noisecov_st, size=1000)

def harmonic(t, amplitude, frequency, phase, show_noise, sigma, noise_value):
    clean_harmonic = amplitude * np.sin(frequency * t + phase)
    if show_noise:
        noisy_harmonic = clean_harmonic + noise_value
        return noisy_harmonic
    else:
        return clean_harmonic

def mediana(data, fullsize):
    medfil = np.zeros_like(data)
    half = fullsize // 2
    for i in range(half, len(data) - half):
        medfil[i] = np.median(data[i - half: i + half + 1])
    return medfil

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("LAB5"),
    dcc.Store(id='noise-data', data=noise_value), 
    html.Div([
        html.Div([
            dcc.Graph(id='harmonic-plot'),
            html.Label('Амплітуда (A):'),
            dcc.Slider(id='amplitude-slider', min=0.1, max=10, step=0.0001, value=amplitude_st,
                       marks={i: str(i) for i in range(1, 11)}),
            html.Label('Частота(ω):'),
            dcc.Slider(id='frequency-slider', min=0.1, max=10, step=0.0001, value=frequency_st,
                       marks={i: str(i) for i in range(1, 11)}),
            html.Label('Фаза(φ):'),
            dcc.Slider(id='phase-slider', min=0, max=2*np.pi, step=0.0001, value=phase_st, 
                       marks={i: str(i) for i in range(0, 8)}),
            dcc.Checklist(id='show-noise-checkbox', options=[{'label': 'Показати шум', 'value': True}], value=[True]),
            html.Button('Скинути', id='reset-button', n_clicks=0)
        ], style={'width': '40%', 'float': 'left'}),
        html.Div([
            dcc.Graph(id='filtered-harmonic-plot'),
            html.Label('Амплітуда шуму:'),
            dcc.Slider(id='noise-mean-slider', min=-1, max=1, step=0.1, value=noisemean_st,
                       marks={i: str(i) for i in range(-1, 2)}, className='slider'),
            html.Label('Дисперсія:'),
            dcc.Slider(id='noise-covariance-slider', min=0, max=1, step=0.01, value=noisecov_st,
                       marks={i/100: str(i/100) for i in range(0, 101, 10)}, className='slider'),
            html.Label('Розмір вікна для медіанного фільтра:'),
            dcc.Dropdown(id='median-window-dropdown', options=[{'label': str(size), 'value': size} for size in range(3, 25)], value=3)
        ], style={'width': '40%', 'float': 'left'})
    ])
])

@app.callback(
    [Output('amplitude-slider', 'value'),
     Output('frequency-slider', 'value'),
     Output('phase-slider', 'value'),
     Output('noise-mean-slider', 'value'),
     Output('noise-covariance-slider', 'value')],
    [Input('reset-button', 'n_clicks')]
)
def reset(n_clicks):
    if n_clicks > 0:
        return amplitude_st, frequency_st, phase_st, noisemean_st, noisecov_st
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    Output('noise-data', 'data'),
    [Input('noise-mean-slider', 'value'),
     Input('noise-covariance-slider', 'value')]
)
def update_noise_data(noisemean, noisecov):
    return np.random.normal(noisemean, noisecov, size=1000)

@app.callback(
    [Output('harmonic-plot', 'figure'),
     Output('filtered-harmonic-plot', 'figure')],
    [Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('show-noise-checkbox', 'value'),
     Input('median-window-dropdown', 'value'),
     Input('noise-data', 'data')]
)
def update_plots(amplitude, frequency, phase, show_noise, window_size, noise_value):
    noisy_signal = harmonic(t, amplitude, frequency, phase, show_noise, sigma_st, noise_value)
    filtered_signal = mediana(noisy_signal, window_size)

    plot1 = go.Scatter(x=t, y=noisy_signal, mode='lines', name='Гармоніка з шумом', line=dict(color='purple'))
    layout1 = go.Layout(title='Гармоніка з шумом', xaxis_title='Час', yaxis_title='Амплітуда')
    figure1 = {'data': [plot1], 'layout': layout1}

    plot2 = go.Scatter(x=t, y=filtered_signal, mode='lines', name='Відфільтрована гармоніка', line=dict(color='purple'))
    layout2 = go.Layout(title='Відфільтрована гармоніка', xaxis_title='Час', yaxis_title='Амплітуда')
    figure2 = {'data': [plot2], 'layout': layout2}

    return figure1, figure2

if __name__ == '__main__':
    app.run_server(debug=True)
