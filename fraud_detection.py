from flask import Flask, render_template_string, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load your saved model
model = joblib.load('fraud_detection_piple.pkl')

# Basic HTML form (no need for separate template files)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fraud Detection App</title>
    <style>
    .main_container{
        display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
   .select_field {
    width: 269px;
    height: 26px;
    margin-top: 10px;
    border-radius: 13px;
    border: 1px solid #999;
    padding: 0 10px;
    background-color: #fff;
    font-size: 14px;
    color: #333;
    appearance: none;           /* Remove default arrow */
    -webkit-appearance: none;
    -moz-appearance: none;
    background-image: url("data:image/svg+xml;utf8,<svg fill='black' height='12' viewBox='0 0 24 24' width='12' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>");
    background-repeat: no-repeat;
    background-position-x: 95%;
    background-position-y: 50%;
    cursor: pointer;
}

/* Style dropdown options */
.select_field option {
    background-color: #f4f4f4;
    color: #333;
    padding: 10px;
}

    .input_fields{
        width: 250px;
        height: 26px;
        margin-top: 10px;
        border-radius: 20px;
        border:1px solid;
        padding: 0 10px;
        }
    .button{
        width: 100px;
        height: 30px;
        border-radius: 20px;
        border: 1px solid;
        }

    </style>
</head>
<body style="font-family: Arial;background-image: linear-gradient(90deg,rgba(42, 123, 155, 1) 0%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%);">
<div class="main_container">
    <h2>💳 Fraud Detection App</h2>
    <form method="POST">
        <label>Transaction Type:</label><br>
        <select name="type" class="select_field">
        <option value="CASH_OUT">CASH_OUT</option>
        <option value="PAYMENT">PAYMENT</option>
        <option value="CASH_IN">CASH_IN</option>
        <option value="TRANSFER">TRANSFER</option>
        <option value="DEBIT">DEBIT</option>
        </select><br><br>

        <label>Amount:</label><br>
        <input type="number" name="amount" class="input_fields" placeholder="Enter the Amount" step="any" required><br><br>

        <label>New Balance Origin:</label><br>
        <input type="number" name="newbalanceorigin" class="input_fields" placeholder="Enter New Balance Origin after Transfer" step="any" required><br><br>

        <label>Balance Difference Origin:</label><br>
        <input type="number" name="balancedifforigin" step="any" placeholder="Enter Difference of Amount in Origin After Transfer" class="input_fields" required><br><br>

        <label>New Balance Destination:</label><br>
        <input type="number" name="newbalancedest" step="any" placeholder="Enter New Balance Destination after Transfer" class="input_fields" required><br><br>

        

        <label>Balance Difference Destination:</label><br>
        <input type="number" name="balancedifferencedest" step="any" placeholder="Enter Difference of Amount in Destination After Transfer" class="input_fields" required><br><br>

        <button type="submit" class="button">Predict</button>
    </form>

    {% if prediction is not none %}
        <h3>Prediction: {{ '🚨 Fraud Transaction' if prediction == 1 else '✅ Not Fraud' }}</h3>
    {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None
    if request.method == "POST":
        # Get form values
        transaction_type = request.form["type"]
        amount = float(request.form["amount"])
        old_balance = float(request.form["newbalanceorigin"])
        new_balance = float(request.form["newbalancedest"])
        Origin_balance_difference = float(request.form["balancedifforigin"])
        Dest_balance_difference = float(request.form["balancedifferencedest"])

        # Adjust according to how your model expects input
        data = pd.DataFrame([[transaction_type, amount, old_balance, new_balance,Origin_balance_difference,Dest_balance_difference]],
                            columns=["type", "amount", "newbalanceOrig", "newbalanceDest","balanceDiffOrigin",'balanceDiffDest'])

        # Make prediction
        prediction = int(model.predict(data)[0])

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
