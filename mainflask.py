import base64
import random
import threading
from flask import Flask, request
from pydantic import BaseModel
import io
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

some_var = 0
lo = threading.Lock()
app = Flask(__name__)
origins = ["*"]

def plot_mac(data: dict):
    projects = data["projects"]
    ers = data["ers"]
    macs = data["macs"]
    df = pd.DataFrame({"Projects": projects,
                       "ER (CO2e)": ers,
                       "MAC ($/CO2e)": macs,
                       })
    df.sort_values(by=['MAC ($/CO2e)'], inplace=True)
    df.reset_index()
    df.set_index("Projects", inplace=True)
    df["Cumulative ER"] = df["ER (CO2e)"].cumsum()
    df["xpos"] = ""

    for index in df.index:
        i = df.index.get_loc(index)

        if i == 0:
            df.loc[index, "xpos"] = df.loc[index, "ER (CO2e)"] / 2

        else:
            a = df.loc[index, "ER (CO2e)"] / 2
            b = df.iloc[i-1 , 2]
            df.loc[index, "xpos"] = b+a
           
    df["xpos_labels"] = df["xpos"] 
    plt.figure(figsize=(14, 8))
    plt.rcParams["font.size"] = 12
    xpos = df["xpos"].values.tolist()
    y = df["MAC ($/CO2e)"].values.tolist()
    w = df["ER (CO2e)"].values.tolist()
    l = []

    for i in range(0, len(y) + 1):
        l.append((random.random(), random.random(), random.random()))
    
    plt.bar(xpos,
            height=y,
            width=w,
            fill=True,
            color=l,
            alpha=0.75)
    
    for index in df.index:
        x_ref = df.loc[index, "xpos_labels"]
        y_ref = df.loc[index, "MAC ($/CO2e)"]

        if y_ref<=0:
            plt.annotate(index, xy=(x_ref, y_ref), xytext=(x_ref, y_ref - 0.05*y_ref),rotation=90)
        else:
            plt.annotate(index, xy=(x_ref, y_ref), xytext=(x_ref,  0.05*y_ref),rotation=90)
    
    plt.grid(True, color="lightgray", linewidth="1.4", linestyle="-")
    plt.xlim(0, df["ER (CO2e)"].sum())
    
    if df["MAC ($/CO2e)"].max()<0:
        plt.ylim(df["MAC ($/CO2e)"].min() + df["MAC ($/CO2e)"].min()*0.1,
            -df["MAC ($/CO2e)"].min()*0.1)
    elif df["MAC ($/CO2e)"].min()>0:
        plt.ylim(-df["MAC ($/CO2e)"].max()*0.1,
            df["MAC ($/CO2e)"].max() + df["MAC ($/CO2e)"].max()*0.1)
    else:         
        plt.ylim(df["MAC ($/CO2e)"].min() + df["MAC ($/CO2e)"].min()*0.1,
            df["MAC ($/CO2e)"].max() + df["MAC ($/CO2e)"].max()*0.1 )
    
    current_values = plt.gca().get_xticks()
    plt.gca().set_xticklabels(['{:,}'.format(x) for x in current_values])
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,}'.format(x) for x in current_values])
    plt.xlabel("Reduction of GHG equivalent(tCO₂e/yr) ")
    plt.ylabel("Cost of reduction options(US$/tCO₂e)")
    plt.tight_layout()
    string_bytes = io.BytesIO()
    plt.savefig(string_bytes, format='jpg')
    string_bytes.seek(0)
    plt.cla()
    plt.clf()
    plt.close('all')
    base64_jpg_data = base64.b64encode(string_bytes.read())

    return base64_jpg_data

class PlotData(BaseModel):
    projects: list
    ers: list
    macs: list

@app.route('/image', methods=['POST'])
def image():
    global lo
    with lo:
        data = request.json
        return plot_mac({
            "projects": data["projects"],
            "ers": data["ers"],
            "macs": data["macs"]
        })

@app.route("/")
async def root():
    return "index"

@app.route("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=False, use_reloader=True)
