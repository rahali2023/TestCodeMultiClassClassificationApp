from flask import Flask, render_template, request, jsonify
import pickle
import sys


# This is took from the labels csv file of the dataset.
categories_map = {
    1: "Neoplasms",
    2: "Digestive system diseases",
    3: "Nervous system diseases",
    4: "Cardiovascular diseases",
    5: "General pathological conditions",
}

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('main_page.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model = pickle.load(open('models\Trained_NeuralNet_MedicalDataset_MODEL_LowAccuracy.sav', 'rb'))
    except IOError:
        print("Could not load the model")
        sys.exit()

    
    # If you are using browser to test the app please uncomment this part
    if request.method == 'POST':
        abstract = request.form['abstract']
        category_number = model.predict([abstract])
        category_name = categories_map[category_number[0]]
        prediction_proba = "%.2f" % (max(model.predict_proba([abstract])[0])*100) + "%"
        return render_template('prediction_page.html',
                               abstract = abstract,
                               predicted_class = category_name,
                               confidence = prediction_proba)
    
    # If you are using postman to test this app please uncomment this part
    # if request.method == 'POST':
    #     request_json = request.json
    #     abstract = request_json["Abstract"]
    #     category_number = model.predict([abstract])
    #     category_name = categories_map[category_number[0]]
    #     prediction_proba = "%.2f" % (max(model.predict_proba([abstract])[0])*100) + "%"

    #     return jsonify({"Abstract": abstract,
    #                     "Predicted Class": category_name,
    #                     "Confidence": prediction_proba})


    


if __name__ == '__main__':
    app.run(debug=True)
