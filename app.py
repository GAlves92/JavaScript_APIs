from flask import Flask, render_template, jsonify, redirect
import pandas as pd

belly_button_df = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
biodiversity_df = pd.read_csv("belly_button_biodiversity_otu_id.csv")
samples_df = pd.read_csv("belly_button_biodiversity_samples.csv")
metadata_df = pd.read_csv("metadata_columns.csv")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/names') 
def names():
    samples_df_ready = samples_df.drop("otu_id", axis=1)
    samples_df_1 = samples_df_ready.columns.tolist()
    return jsonify(samples_df_1)

@app.route('/otu')
def otu():
    biodiversity_ready = biodiversity_df["lowest_taxonomic_unit_found"].tolist()
    return jsonify(biodiversity_ready)

@app.route('/metadata/<sample>')
def metadata(sample):
    belly_button_json = belly_button_df[["AGE", "BBTYPE", "ETHNICITY", "GENDER", "LOCATION", "SAMPLEID"]]
    sample = int(sample.strip('BB_'))
    belly_input = belly_button_json[belly_button_json["SAMPLEID"] == sample]
    belly_sample = belly_input.to_dict(orient='records')
    return jsonify(belly_sample)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    belly_frequency = belly_button_df[["WFREQ", "SAMPLEID"]]
    sample = int(sample.strip('BB_'))
    belly_frequency.set_index('SAMPLEID', inplace = True)
    sample_frequency = belly_frequency.loc[sample, 'WFREQ']
    return jsonify(sample_frequency)

@app.route('/samples/<sample>')
def samples(sample):
    samples_df[["otu_id", sample]]
    samples_ready = samples_df[["otu_id", sample]]
    samples_filter = samples_ready[samples_ready[sample] > 0]
    samples_filter.columns = ["otu_id", "sample_values"]
    sorted_samples = samples_filter.sort_values(by='sample_values', ascending = False)
    my_dict = [{'otu_ids': list(sorted_samples['otu_id'].values.tolist()),
                           'sample_values': list(sorted_samples['sample_values'].values.tolist())
           }]
    return jsonify(my_dict)

if __name__ == "__main__":
    app.run(debug=False)

