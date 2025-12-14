import requests
import json

url = 'http://localhost:5000/predict'

# The "Toxic" Profile Payload
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

try:
    print(f"Sending POST request to {url}...")
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nResponse:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Failed to connect: {e}")
