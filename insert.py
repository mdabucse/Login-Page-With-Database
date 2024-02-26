import pymongo as po
import json
import streamlit as slt
import datetime
import pandas as pd



# Backend
def clickme():
    data = {
        'Email':Email,
        'Password':Password,
        'Confirm':Confirm
    }
    return data
# Insert The Data Into The Data Base
database_name = "INTERNREACT"
collection_name= "Login"
clint = po.MongoClient('mongodb://localhost:27017/')
def insert(data):
    db = clint[database_name]
    collection = db[collection_name]
    collection.insert_one(data)

# Front End
page = slt.sidebar.selectbox(
    'Goto',
    ['Sign Up', 'Sign in','Login Logs']
)

if page == 'Sign Up':
    slt.title("Sign Up")
    Email = slt.text_input("Email ")
    Password = slt.text_input("Password ")
    Confirm = slt.text_input("Re-Enter Password")
    if slt.button("Sign Up"):
        datas=clickme()
        if Password=='':
            slt.write("""
            <div style='background-color:#ff0000;padding:10px;border-radius:5px;'>
                <strong>Warning!</strong> Enter Valid Data
            </div>
            """, unsafe_allow_html=True)
        elif Password == Confirm:
            slt.write("""
            <div style='background-color:#00ff00;padding:10px;border-radius:5px;'>
                <strong>Success!</strong> Sign Up Successful
            </div>
            """, unsafe_allow_html=True)
            insert(datas)
            
        else:
            slt.write("""
            <div style='background-color:#ff0000;padding:10px;border-radius:5px;'>
                <strong>Warning!</strong> Check The Password
            </div>
            """, unsafe_allow_html=True)
if page == 'Sign in':
    slt.title("Sign In")
    db = clint[database_name]
    collection = db[collection_name]
    Val_Email = slt.text_input("Email")
    Val_Password = slt.text_input("Password")
    if slt.button("Sign In"):
        Check_Email = collection.find_one({"Email":Val_Email})
        Check_Password = collection.find_one({"Password":Val_Password})

        if Check_Password  and Check_Email :
            if Val_Email== Check_Email.get('Email') and Val_Password == Check_Password.get('Password'):
                slt.write("""
                    <div style='background-color:#00ff00;padding:10px;border-radius:5px;'>
                        <strong>Login Successful</strong> 
                    </div>
                    """, unsafe_allow_html=True)
        else: 
            slt.write("""
            <div style='background-color:#ff0000;padding:10px;border-radius:5px;'>
                <strong>It is Not Found !</strong> Go to Sign Up Page
            </div>
            """, unsafe_allow_html=True)

if page == 'Login Logs':
    db = clint[database_name]
    collection = db[collection_name]
    slt.title('Login Logs')
    data={
        'Email':[],
        'Password':[]
    }
    result = collection.find()
    for i in result:
        data['Email'].append(i['Email'])
        data['Password'].append(i['Password'])
    result_in_df = pd.DataFrame(data)
    slt.write(result_in_df)
