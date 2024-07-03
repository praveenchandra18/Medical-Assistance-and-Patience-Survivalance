from flask import Blueprint, render_template,request,session,redirect
import pickle
import pandas as pd


suggestor_bp=Blueprint('suggestor',__name__)

@suggestor_bp.route('/food_suggestor')
def food_suggestor_page():
    return render_template('food_suggestor.html')

@suggestor_bp.route('/diet_prediction',methods=['GET','POST'])
def diet_prediction():
    gender=request.form.get("gender")
    weight=request.form.get("num1")
    height=request.form.get("num2")

    with open('bmi_model.pkl', 'rb') as f:
        model = pickle.load(f)

    new_data_point = pd.DataFrame({'Gender': [gender],'Height': [height], 'Weight': [weight]})
    predicted_bmi = model.predict(new_data_point)
    person_bmi=predicted_bmi[0]

    cluster_0=[['Bread made in wheat', 1, 1, 1, 1], 
            ['Brown Rice', 0, 1, 1, 1], 
            ['Fruit and Nut chocolate', 0, 0, 1, 0], 
            ['White Rice', 0, 1, 1, 1], 
            ['Chocos', 0, 0, 1, 0], 
            ['Mutton', 1, 0, 1, 1], 
            ['Kheer', 0, 0, 0, 1], 
            ['Whole Wheat Pasta', 0, 1, 1, 1],     
            ['Salmon', 1, 0, 1, 1],                
            ['Quinoa', 0, 1, 1, 1],                
            ['Chicken Breast', 1, 0, 1, 1],        
            ['Greek Yogurt', 0, 1, 1, 1],          
            ['Hummus', 0, 1, 1, 1],                
            ['Avocado', 0, 1, 1, 1]]
    
    cluster_1=[['Aloo Tikki', 1, 0, 1, 1], ['Bananas', 1, 1, 0, 0], ['Baati', 1, 0, 1, 1], ['Cauliflower', 1, 0, 1, 1], ['Coffee', 1, 1, 0, 0], ['Corn', 1, 1, 1, 1], ['Grapes', 1, 1, 0, 0], ['Milk', 1, 1, 0, 1], ['Paneer Tikka', 1, 0, 1, 1], ['Orange', 1, 1, 0, 0], ['Maggie', 1, 0, 1, 1], ['Pears', 1, 1, 0, 0], ['Aloo Matar ', 1, 0, 1, 1], ['Sitafal', 1, 0, 1, 1], ['Poha', 1, 1, 0, 0], ['Tomato', 1, 1, 1, 1], ['Dahi', 1, 1, 1, 1], ['Chowmein', 1, 0, 1, 1], ['Dal Makhani', 1, 0, 1, 1], ['Mushrooms', 1, 1, 1, 1], ['Sweet Potatoes ', 1, 1, 1, 0], ['Masala Aloo', 1, 1, 1, 1], ['Orange juice', 1, 1, 0, 0], ['Sweet Dahi', 1, 1, 1, 1], ['Cornflakes', 1, 1, 0, 0], ['Laal Chai', 1, 1, 0, 0], ['Butter Paneer', 1, 0, 1, 1], ['Beans', 1, 0, 1, 1], ['Dal Fry', 1, 0, 1, 1], ['Red Sauce Pasta', 1, 0, 1, 1], ['Chai', 1, 1, 0, 0], ['Apples', 1, 1, 0, 0], ['Strawberries', 1, 1, 0, 0], ['Kiwi', 1, 1, 1, 0]]
    cluster_2=[['Cheese', 2, 1, 0, 0], ['Cashew Nuts', 2, 1, 0, 0], ["Glucone'D", 2, 1, 0, 0], ['Surmai', 2, 0, 0, 1], ['Butter Chicken', 2, 0, 1, 1], ['Almonds', 2, 1, 0, 0], ['Egg Yolk ', 2, 1, 0, 0], ['Pumpkin seeds', 2, 1, 0, 0], ['Salmon', 2, 0, 1, 1], ['Boiled Chicken', 2, 0, 1, 1], ['Chicken Tandoori', 2, 0, 0, 1], ['Prawns', 2, 0, 0, 1], ['Chicken sausage', 2, 0, 0, 1], ['Malai Chicken', 2, 0, 0, 1], ['Chicken Popcorn', 2, 0, 1, 1], ['Nalli Nihari', 2, 0, 1, 1], ['Fish Eggs', 2, 0, 1, 1], ['King Fish', 2, 1, 0, 0]]
    cluster_3=[['Kadhi', 3, 1, 0, 0],['Mango Chutney', 4, 1, 0, 0], ['Rohu Curry', 3, 0, 1, 1], ['Veg Pizza', 3, 0, 0, 1],['Honey', 4, 1, 0, 1], ['Cheese Pizza', 3, 0, 0, 1], ['Onion Pakoda', 3, 0, 1, 1], ['Chicken Kolapuri', 3, 0, 1, 1], ['Chicken 65', 3, 0, 1, 1], ['Dosa', 3, 1, 1, 1], ['Idli', 3, 1, 1, 1], ['Chappati', 3, 0, 1, 1], ['Uttapam', 3, 1, 1, 1], ['Bhaji Pav', 3, 1, 0, 0], ['Kebab', 3, 0, 1, 1], ['Tomato Rice', 3, 0, 1, 1], ['Momos', 3, 0, 0, 1], ['Mixed Veg', 3, 0, 1, 1], ['Nachos', 3, 1, 1, 1], ['Chocolate Icecream', 3, 0, 0, 1]]
    message="You come under "
    
    # print(person_bmi)
    
    if(person_bmi<2):
        message=message+"Underweight category."
        lst=cluster_1
    elif(person_bmi>=2 and person_bmi<=3):
        message=message+"Normal weight. "
        lst=cluster_0
    elif(person_bmi>3 and person_bmi<=4):
        message=message+"Overweight. "
        lst=cluster_2
    else:
        message=message+"Obesity category."
        lst=cluster_3

    message=message+"Taking these foods may help you to be healthy."

    breakfast=[]
    lunch=[]
    dinner=[]

    for i in lst:
        if(i[2]==1):
            breakfast.append(i)
        if(i[3]==1):
            lunch.append(i)
        if(i[4]==1):
            dinner.append(i)

    return render_template('diet_for_you.html',message=message,breakfast=breakfast,lunch=lunch,dinner=dinner)