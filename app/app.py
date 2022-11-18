# Demo application for JCB

import numpy as np
import pandas as pd

from flask import Flask, render_template

app = Flask(__name__)
generatedDataFrame = {}

@app.route("/data", methods=['GET'])
def get_df():
    data = np.random.randint(0, 100, size=1000)
    df = pd.DataFrame(data, columns=['a'])
    df['b'] = df.mod(10)
    generatedDataFrame = df.to_json(orient='records')
    return generatedDataFrame
