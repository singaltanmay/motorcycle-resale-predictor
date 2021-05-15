import pickle

from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('motorcycle_price_predictor_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    print(request.form.to_dict(flat=False))

    km_driven = float(request.form['kms-driven']) / 1000
    ex_showroom_price = float(request.form['showroom-price'])
    no_year = 2021 - int(request.form['year'])
    seller_type_individual = 1
    if request.form['seller-type'] == 'Dealer':
        seller_type_individual = 0
    owner_2nd_owner = 0
    owner_3rd_owner = 0
    owner_4th_owner = 0
    num_owners = request.form['num-owners']
    if num_owners == 2:
        owner_2nd_owner = 1
    elif num_owners == 3:
        owner_3rd_owner = 1
    elif num_owners == 4:
        owner_4th_owner = 1

    prediction = model.predict([[km_driven, ex_showroom_price, no_year, seller_type_individual, owner_2nd_owner,
                                 owner_3rd_owner, owner_4th_owner]])
    output = round(prediction[0], 2) * 1000
    print("prediction: " + str(output))
    return render_template('index.html',
                           prediction_text="You can sell this vehicle for approximately {}".format(int(output)))


if __name__ == "__main__":
    app.run()
