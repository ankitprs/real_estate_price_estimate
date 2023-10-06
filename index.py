import streamlit as st
import numpy as np
import pickle
import json

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)



def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    try: 
      if __model is None:
        with open('banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    except ModuleNotFoundError as e:
      print(f"Error loading the model: {e}")

    print("loading saved artifacts...done")


def main():

    # giving a title
    st.title('Bangalore Real Estate price Prediction Web App')

    load_saved_artifacts()
    
    # getting the input data from the user
    location = st.selectbox('Which Locality ', __locations)
    st.write('You selected:', location) 
    # location = st.text_input('Locality')
    total_sqft = st.text_input('Square feet area')
    bhk = st.text_input('Number of BHK')
    bath = st.text_input('Number of Bathroom') 
  

    # code for Prediction
    prediction = ''
    
    if st.button('Estimate Price'):
      if(not location or not total_sqft or  not bhk or not bath):
        st.error("Please Fill Complete Details then Estimated")
      else:
        prediction = get_estimated_price(location,total_sqft,bhk,bath)
    
    if(prediction != ''):
      st.success(f'{prediction} Lakhs')
    
    
    
if __name__ == '__main__':
    main()