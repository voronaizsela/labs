import os
import pandas as pd
from spyre import server
import seaborn as sns
import matplotlib.pyplot as plt

def read(directory, week_range, year, area_id):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    files = os.listdir(directory)
    result_df = pd.DataFrame()

    for i, file in enumerate(files, start=1):
        filepath = os.path.join(directory, file)
        df = pd.read_csv(filepath, header=1, names=headers, skiprows=1)

        df = df.dropna(subset=['VHI'])
        df = df[df['VHI'] != -1]

        df = df.replace({'<tt>': '', '<pre>': ''})

        df['Area_ID'] = i

        if 'empty' in df.columns:
            df.drop('empty', axis=1, inplace=True)

        if not df.empty:
            result_df = pd.concat([result_df, df], ignore_index=True)

    result_df['Year'] = pd.to_numeric(result_df['Year'])
    result_df['Week'] = pd.to_numeric(result_df['Week'])

    start_week, end_week = map(int, week_range.split('-'))
    result_df = result_df[(result_df['Week'] >= start_week) & (result_df['Week'] <= end_week) & (result_df['Year'] == year)]
    result_df = result_df[result_df['Area_ID'] == int(area_id)]

    return result_df

class StockExample(server.App):
    title = "LABA 3.NOAA data visualization" 
    
    inputs = [
        { "type": 'dropdown',
          "label": 'Options',
          "options": [{"label": "VCI", "value": "VCI"},
                      {"label": "TCI", "value": "TCI"},
                      {"label": "VHI", "value": "VHI"}],
          "key": 'ticker',
          "action_id": "update_data"},
          
        { "type": 'dropdown',
          "label": 'Area',
          "options": [{"label": "Вінницька", "value": "1"},
                      {"label": "Волинська", "value": "2"},
                      {"label": "Дніпропетровська", "value": "3"},
                      {"label": "Донецька", "value": "4"},
                      {"label": "Житомирська", "value": "5"},
                      {"label": "Закарпатська", "value": "6"},
                      {"label": "Запорізька", "value": "7"},
                      {"label": "Івано-Франківська", "value": "8"},
                      {"label": "Київська", "value": "9"},
                      {"label": "Кіровоградська", "value": "10"},
                      {"label": "Луганська", "value": "11"},
                      {"label": "Львівська", "value": "12"},
                      {"label": "Миколаївська", "value": "13"},
                      {"label": "Одеська", "value": "14"},
                      {"label": "Полтавська", "value": "15"},
                      {"label": "Рівенська", "value": "16"},
                      {"label": "Сумська", "value": "17"},
                      {"label": "Тернопільська", "value": "18"},
                      {"label": "Харківська", "value": "19"},
                      {"label": "Херсонська", "value": "20"},
                      {"label": "Хмельницька", "value": "21"},
                      {"label": "Черкаська", "value": "22"},
                      {"label": "Чернівецька", "value": "23"},
                      {"label": "Чернігівська", "value": "24"},
                      {"label": "Севастопіль", "value": "25"},
                      {"label": "Київ", "value": "26"},
                      {"label": "Республіка Крим", "value": "27"}],  
          "key": 'area_id',
          "action_id": "update_data"},
        { "type":'text',
          "label": 'Week range',
          "key": 'week_range',
          "value": "1-52",
          "action_id": "update_data"},
        { "type":'text',
          "label": 'Year',
          "key": 'year',
          "value": 2023, 
          "action_id": "update_data"}
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "View"
    }]

    tabs = ["Table", "Plot"]

    outputs = [
        {   "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": False
        },
        {  "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        directory = "/Users/violetta/Desktop/VHI(lab2)"
        week_range = params['week_range']
        year = int(params['year'])  
        area_id = params['area_id']
        df = read(directory, week_range, year, area_id)
        return df

    def getPlot(self, params):
     df = self.getData(params).drop(['SMN', 'SMT'], axis=1).set_index(['Week', 'Year'])
     selected_column = params['ticker']
     plt.figure(figsize=(12, 6))
    
     if selected_column == 'VCI':
        sns.histplot(data=df[selected_column], color='blue', edgecolor='purple', kde=True, bins=10)
        plt.ylabel("Frequency")
        plt.xlabel(selected_column)
        plt.title(f"Visualization of {selected_column}")
     
     elif selected_column == 'TCI':
        sns.lineplot(data=df, x='Week', y=selected_column, color="purple", marker="o")
        plt.ylabel(selected_column)
        plt.xlabel("Selected period")
        plt.title(f"Visualization of {selected_column}")
     
     elif selected_column == 'VHI':
        pivot_df = df.pivot_table(index='Year', columns='Week', values=selected_column)
        cmap = sns.color_palette("viridis", as_cmap=True)
        sns.heatmap(data=pivot_df, cmap=cmap)
        plt.ylabel("Year")
        plt.xlabel("Weeks")
        plt.title(f"Visualization of {selected_column}")
     
     else:
        return None

     return plt.gcf()

    def getTable(self, params):
        df = self.getData(params)
        selected_column = params['ticker']
        table_df = df[['Area_ID', 'Year', 'Week', selected_column]]
        return table_df

app = StockExample()
app.launch(port=9093)

