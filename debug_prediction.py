import pandas as pd
import pickle
import numpy as np

# Load model
with open('models/attrition_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the "Toxic" Profile
data = {
    # Demographics
    'Age': 19,
    'Gender': 'Male',
    'MaritalStatus': 'Single',
    'DistanceFromHome': 25,
    'Education': 1,
    'EducationField': 'Medical',
    
    # Professional
    'Department': 'Research & Development',
    'JobRole': 'Research Scientist',
    'JobLevel': 1,
    'MonthlyIncome': 2000,
    
    # Experience
    'TotalWorkingYears': 1,
    'YearsAtCompany': 1,
    'YearsWithCurrManager': 0,
    'YearsSinceLastPromotion': 0,
    'NumCompaniesWorked': 1,
    'BusinessTravel': 'Travel_Frequently',
    
    # Conditions
    'PercentSalaryHike': 11,
    'StockOptionLevel': 0,
    'TrainingTimesLastYear': 0,
    'PerformanceRating': 3,
    
    # Satisfaction (Low)
    'EnvironmentSatisfaction': 1,
    'JobSatisfaction': 1,
    'WorkLifeBalance': 1,
    'JobInvolvement': 1,
    
    # Temporal (Toxic / Burnout)
    'AvgWorkingHours': 11.0,
    'LateArrivals': 20,
    'AvgOvertime': 3.0,
    'AbsenceRate': 15.0,
    'WorkHoursVariance': 5.0
}

df = pd.DataFrame([data])

print("-" * 50)
print("Testing Toxic Profile...")
print("-" * 50)

# Predict
try:
    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    
    print(f"Prediction: {'Leave' if prediction == 1 else 'Stay'}")
    print(f"Probability Stay:  {proba[0]*100:.2f}%")
    print(f"Probability Leave: {proba[1]*100:.2f}%")
    
    # Feature Importance (if applicable to the pipeline step)
    # This might require accessing the classifier step inside the pipeline
    if hasattr(model, 'named_steps') and 'classifier' in model.named_steps:
        clf = model.named_steps['classifier']
        if hasattr(clf, 'feature_importances_'):
            print("\nmodel.named_steps['classifier'] has feature importances.")
            # We would need to map these back to feature names which is hard with the preprocessor
            # So just confirming the model structure for now.
except Exception as e:
    print(f"Error: {e}")
