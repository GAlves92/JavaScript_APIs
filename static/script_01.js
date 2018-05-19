function piechart(sample_data, otu_data) {
    console.log(sample_data[0]['sample_values'].slice(0, 10))
    var z = document.getElementById("graph");
    var pies = [{
        values: sample_data[0]['sample_values'].slice(0,10),
        labels: sample_data[0]['otu_ids'].slice(0, 10),
        type: 'pie'
        }];

    var layout = {
        margin: {t: 0, l: 0}
    };

    Plotly.newPlot(z, pies, layout);
    }

function bubblechart(sample_data, otu_data) {
    console.log(sample_data);
    var b = document.getElementById("bubble");
    var bubbles = [{
        x: sample_data[0]['otu_ids'],
        y: sample_data[0]['sample_values'],
        mode: 'markers',
        marker: {
            size: sample_data[0]['sample_values'],
        }
    }];

    var data = [bubbles];

    var layout =  {
        title: 'Bubble Plot',
        x: 'OTU ID',
        showlegend: false,
        };

    Plotly.newPlot(b, bubbles, layout);
    }      

function getNumbers(user_input, callback) {

    Plotly.d3.json(`/samples/${user_input}`, function(error, sample_data) {
        if (error) return console.warn(error);
        Plotly.d3.json('/otu', function(error, otu_data) {
            if (error) return console.warn(error);
            callback(sample_data, otu_data);
        });
    });
    Plotly.d3.json(`/metadata/${user_input}`, function(error, metaData) {
        if (error) return console.warn(error);
    })
 }

function dropdown() {
    var x = document.getElementById("selDataset");
    Plotly.d3.json("/names", function (error, data) {
        for (var i = 0; i < data.length; i++) {
            var currentOption = document.createElement('option');
            currentOption.text = data[i];
            currentOption.value = data[i];
            x.appendChild(currentOption);
        }
        getNumbers(data[0], piechart);
        getNumbers(data[0], bubblechart);
    })
}

function option(user_input) {
    getNumbers(user_input, piechart);
    console.log(user_input);
}


function init() {
    dropdown();
}

init();