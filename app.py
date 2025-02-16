from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model
model = pickle.load(open("model_rf_smote.pkl", "rb"))

# Model's expected features
expected_cols = model.feature_names_in_

# ----- ML Prediction Endpoint -----
# One-hot encoding function
def preprocess_input(data):
    df = pd.DataFrame([data])

    # One-hot encoding categorical features with corrected mappings
    df['gender_Female'] = 1 if data['gender'] == 0 else 0
    df['gender_Male'] = 1 if data['gender'] == 1 else 0

    df['Partner_No'] = 1 if data['Partner'] == 0 else 0
    df['Partner_Yes'] = 1 if data['Partner'] == 1 else 0

    df['Dependents_No'] = 1 if data['Dependents'] == 0 else 0
    df['Dependents_Yes'] = 1 if data['Dependents'] == 1 else 0

    df['PhoneService_No'] = 1 if data['PhoneService'] == 0 else 0
    df['PhoneService_Yes'] = 1 if data['PhoneService'] == 1 else 0

    df['MultipleLines_No phone service'] = 1 if data['PhoneService'] == 0 else 0
    df['MultipleLines_Yes'] = 1 if data['MultipleLines'] == 1 and data['PhoneService'] == 1 else 0
    df['MultipleLines_No'] = 1 if data['MultipleLines'] == 0 and data['PhoneService'] == 1 else 0

    df['InternetService_DSL'] = 1 if data['InternetService'] == 0 else 0
    df['InternetService_Fiber optic'] = 1 if data['InternetService'] == 1 else 0
    df['InternetService_No'] = 1 if data['InternetService'] == 2 else 0

    # Adjusting "No Internet Service" handling
    for feature in ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']:
        df[f'{feature}_No internet service'] = 1 if data['InternetService'] == 2 else 0
        df[f'{feature}_Yes'] = 1 if data[feature] == 1 and data['InternetService'] != 2 else 0
        df[f'{feature}_No'] = 1 if data[feature] == 0 and data['InternetService'] != 2 else 0

    df['Contract_Month-to-month'] = 1 if data['Contract'] == 0 else 0
    df['Contract_One year'] = 1 if data['Contract'] == 1 else 0
    df['Contract_Two year'] = 1 if data['Contract'] == 2 else 0

    df['PaperlessBilling_No'] = 1 if data['PaperlessBilling'] == 0 else 0
    df['PaperlessBilling_Yes'] = 1 if data['PaperlessBilling'] == 1 else 0

    df['PaymentMethod_Bank transfer (automatic)'] = 1 if data['PaymentMethod'] == 0 else 0
    df['PaymentMethod_Credit card (automatic)'] = 1 if data['PaymentMethod'] == 1 else 0
    df['PaymentMethod_Electronic check'] = 1 if data['PaymentMethod'] == 2 else 0
    df['PaymentMethod_Mailed check'] = 1 if data['PaymentMethod'] == 3 else 0

    # Encode tenure into groups
    tenure = data['tenure']
    df['tenure_group_1 - 12'] = 1 if tenure <= 12 else 0
    df['tenure_group_13 - 24'] = 1 if 13 <= tenure <= 24 else 0
    df['tenure_group_25 - 36'] = 1 if 25 <= tenure <= 36 else 0
    df['tenure_group_37 - 48'] = 1 if 37 <= tenure <= 48 else 0
    df['tenure_group_49 - 60'] = 1 if 49 <= tenure <= 60 else 0
    df['tenure_group_61 - 72'] = 1 if tenure >= 61 else 0

    # Ensure correct column order and missing columns filled with 0
    df = df.reindex(columns=expected_cols, fill_value=0)

    return df

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received data:", data)

        # Preprocess input features
        df = preprocess_input(data)
        print("Processed input for model:", df.to_dict(orient="records"))

        # Make prediction
        probs = model.predict_proba(df)[0]  # Get probabilities
        prediction = 1 if probs[1] > 0.5 else 0  # Convert probability to class

        print(f"Churn Probability: {probs[1]}, Predicted Class: {prediction}")

        return jsonify({"prediction": prediction, "probability": float(probs[1])})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400

# my power flurries through the air into the ground
@app.route('/get_csv')
def get_csv():
    try:
        return send_file("static/churn_head.csv", mimetype='text/csv', as_attachment=True)
    except:
        return "CSV file not found", 404
    
@app.route('/get_shape')
def get_shape():
    try:
        return send_file("static/dataset_shape.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Shape file not found", 404
    
@app.route('/get_columns')
def get_columns():
    try:
        return send_file("static/columns.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Columns file not found", 404
    
@app.route('/get_dtypes')
def get_dtypes():
    try:
        return send_file("static/dtypes.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Data types file not found", 404
    
@app.route('/get_describe_stats')
def get_describe_stats():
    try:
        return send_file("static/describe_stats.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Descriptive statistics file not found", 404

@app.route('/get_churn_counts_image')
def get_churn_counts_image():
    try:
        return send_file("static/churn_counts.png", mimetype='image/png', as_attachment=True)
    except:
        return "Churn counts plot not found", 404
    
@app.route('/get_churn_percentage')
def get_churn_percentage():
    try:
        return send_file("static/churn_percentage.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Churn percentage file not found", 404
    
@app.route('/get_churn_value_counts')
def get_churn_value_counts():
    try:
        return send_file("static/churn_value_counts.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Churn value counts file not found", 404
    
@app.route('/get_churn_info')
def get_churn_info():
    try:
        return send_file("static/churn_info.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Churn info file not found", 404
    
@app.route('/get_missing_values')
def get_missing_values():
    try:
        return send_file("static/missing_values.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Missing values file not found", 404

@app.route('/get_missing_values_plot')
def get_missing_values_plot():
    try:
        return send_file("static/missing_values_plot.png", mimetype='image/png')
    except:
        return "Missing values plot not found", 404

@app.route('/get_tenure_group_counts')
def get_tenure_group_counts():
    try:
        return send_file("static/tenure_group_counts.txt", mimetype='text/plain', as_attachment=True)
    except:
        return "Tenure group counts file not found", 404

@app.route('/get_countplot/<predictor>')
def get_countplot(predictor):
    try:
        # Serve the countplot image for the predictor
        return send_from_directory('static', f"{predictor}_countplot.png")
    except:
        return "Countplot image not found", 404
    
@app.route('/get_monthly_vs_total_charges')
def get_monthly_vs_total_charges():
    try:
        # Serve the countplot image for the predictor
        return send_file("static/monthly_vs_total_charges.png", mimetype='image/png')
    except:
        return "Monthly vs total charges image not found", 404
    
@app.route('/get_monthly_charges_kde')
def get_monthly_charges_kde():
    try:
        return send_file("static/monthly_charges_kde.png", mimetype='image/png', as_attachment=False)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_total_charges_kde')
def get_total_charges_kde():
    try:
        return send_file("static/total_charges_kde.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_churn_correlation_bar')
def get_churn_correlation_bar():
    try:
        return send_file("static/churn_correlation_bar.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404
    
@app.route('/get_correlation_heatmap')
def get_correlation_heatmap():
    try:
        return send_file("static/correlation_heatmap.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404
    
@app.route('/get_distribution_of_gender_for_churned_customers')
def get_distribution_of_gender_for_churned_customers():
    try:
        return send_file("static/Distribution_of_Gender_for_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_distribution_of_gender_for_non_churned_customers')
def get_distribution_of_gender_for_non_churned_customers():
    try:
        return send_file("static/Distribution_of_Gender_for_Non_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_distribution_of_paymentmethod_for_churned_customers')
def get_distribution_of_paymentmethod_for_churned_customers():
    try:
        return send_file("static/Distribution_of_PaymentMethod_for_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_distribution_of_contract_for_churned_customers')
def get_distribution_of_contract_for_churned_customers():
    try:
        return send_file("static/Distribution_of_Contract_for_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_distribution_of_techsupport_for_churned_customers')
def get_distribution_of_techsupport_for_churned_customers():
    try:
        return send_file("static/Distribution_of_TechSupport_for_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404

@app.route('/get_distribution_of_seniorcitizen_for_churned_customers')
def get_distribution_of_seniorcitizen_for_churned_customers():
    try:
        return send_file("static/Distribution_of_SeniorCitizen_for_Churned_Customers.png", mimetype='image/png', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404
    
@app.route('/get_distribution_tenure_by_churn')
def get_distribution_tenure_by_churn():
    try:
        return send_file("static/distribution_tenure_by_churn.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500  # Send error if the file is not found

# Route to get the saved plot for 'Distribution of MonthlyCharges by Churn'
@app.route('/get_distribution_monthlycharges_by_churn')
def get_distribution_monthlycharges_by_churn():
    try:
        return send_file("static/distribution_monthlycharges_by_churn.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500  # Send error if the file is not found

# Route to get the saved plot for 'Distribution of TotalCharges by Churn'
@app.route('/get_distribution_totalcharges_by_churn')
def get_distribution_totalcharges_by_churn():
    try:
        return send_file("static/distribution_totalcharges_by_churn.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500  # Send error if the file is not found

# Route to get the saved boxplot for 'Customer Segmentation by Contract Type and Tenure'
@app.route('/get_customer_segmentation_by_contract_tenure')
def get_customer_segmentation_by_contract_tenure():
    try:
        return send_file("static/customer_segmentation_by_contract_tenure.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500  # Send error if the file is not found
    
@app.route('/get_feature_importance_random_forest')
def get_feature_importance_random_forest():
    try:
        return send_file("static/feature_importance_random_forest.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500  # Send error if the file is not found
    
@app.route('/get_customer_clusters_plot')
def get_customer_clusters_plot():
    try:
        return send_from_directory('static', 'customer_clusters_tenure_monthlycharges.png')
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)