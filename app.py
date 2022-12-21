import streamlit as st
from PIL import Image
# import ElectronicEye as ee
import os
from streamlit_option_menu import option_menu
import requests
import cv2
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import model_from_json

try:
    if K.backend() == 'theano':
        K.set_image_data_format('channels_first')
    else:
        K.set_image_data_format('channels_last')
except AttributeError:
    if K._BACKEND == 'theano':
        K.set_image_dim_ordering('th')
    else:
        K.set_image_dim_ordering('tf') 


json_file = open('model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_final.h5")
print("model loaded")

def ElelctronicEye(Img):
	
    img = cv2.imread(Img,cv2.IMREAD_GRAYSCALE)
    print("image loaded")
    #kernel = np.ones((3,3),np.uint8)

    #erosion = cv2.erode(img,kernel,iterations = 3)
    #dilation = cv2.dilate(img,kernel,iterations = 1)
    #img=dilation
    if img is not None:
        #images.append(img)
        img = ~img
        _,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        train_data=[]
        #print(len(cnt))
        rects=[]
        for c in cnt :
            x,y,w,h= cv2.boundingRect(c)
            rect=[x,y,w,h]
            rects.append(rect)
        #print(rects)
        bool_rect=[]
        for r in rects:
            l=[]
            for rec in rects:
                flag=0
                if rec!=r:
                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                        flag=1
                    l.append(flag)
                if rec==r:
                        l.append(0)
            bool_rect.append(l)
        #print(bool_rect)
        dump_rect=[]
        for i in range(0,len(cnt)):
            for j in range(0,len(cnt)):
                if bool_rect[i][j]==1:
                    area1=rects[i][2]*rects[i][3]
                    area2=rects[j][2]*rects[j][3]
                    if(area1==min(area1,area2)):
                        dump_rect.append(rects[i])
        #print(len(dump_rect)) 
        final_rect=[i for i in rects if i not in dump_rect]
        #print(final_rect)
        for r in final_rect:
            x=r[0]
            y=r[1]
            w=r[2]
            h=r[3]
            im_crop =thresh[y:y+h+10,x:x+w+10]
                

            im_resize = cv2.resize(im_crop,(28,28))
            im_resize=np.reshape(im_resize,(1,28,28))
            train_data.append(im_resize)

        components = []
        for i in range(len(train_data)):
            train_data[i]=np.array(train_data[i])
            train_data[i]=train_data[i].reshape(1,28,28,1)
            result = np.argmax(loaded_model.predict(train_data[i]), axis= -1)
            
            if(result[0]==0):
                components.append('Capacitor')
            if(result[0]==1):
                components.append('Diodes')
            if(result[0]==2):
                components.append('Inductor')
            if(result[0]==3):
                components.append('LED')
            if(result[0]==4):
                components.append('Op-Amp')
            if(result[0]==5):
                components.append('Resistor')
            if(result[0]==6):
                components.append('Switch')
            if(result[0]==7):
                components.append('Transformer')
            if(result[0]==8):
                components.append('Transistor')

#         components_final = components
    
    return components
	



if 'component_dict' not in st.session_state:
    st.session_state.component_dict = {}
st.session_state.component_dict={
"Capacitor":["Capacitance value","Voltage rating","Temperature coefficient","Frequency range","Dielectric constant","Dielectric strength","Power factor"],               
"Diodes":["Rectifier Diode","Limiter","Switching","Modulation","Voltage Regulation","Damper","Low Leakage","Detector","Mixer","Protector","Power Diode","High Voltage","Other"],
"Inductor":["Inductance","Tolerance","DCresistance","Saturation current","Incremental current","Rated current"],
"LED":["Color","light intensity value","current\voltage specification"],
"Op-Amp":["Supply current","Gain bandwidth product","Gain bandwidth product","Low level output current","Input resistance","Output resistance","Input voltage range","Common mode input impedance","Output impedance","Total power dissipation","Large signal voltage amplification","Differential voltage gain","Input capacitance","Common mode rejection ratio","Slew rate"],
"Resistor":["rating","tolerance","type","power_rating","temperature_specification","max_voltage"],
"Switch":["switch resistance","operating force","stroke","type"],
"Transformer":["type","winding_connection","efficiency","applicable_standard","rated_power","primary_voltage/secondry_voltage"],
"Transistor":["type","polarity","material","collector_to_base_voltage","collector_to_emitter_breakdown_voltage","collector_current_specification","collector_emitter_saturstion_voltage","forward_current_gain","transition_frequency","device_power_dissipation","package_type"]\
}


# WebPage Configurations

st.set_page_config(
    page_title= 'ElectronicEye', 
    page_icon='img\page_icon.png',  
    initial_sidebar_state="auto", 
    
)

st.title(
    'ELECTRONIC EYE'
)

st.caption(
    'An A.I Powered web application for electronic components selection.'
)

st.markdown('--------------------------------------------------------------------------')



st.session_state.uploaded_img = st.file_uploader(
        'Choose an Image', 
        type=['png', 'jpg', 'jpeg'],  
        on_change=None
    )




#initializing submit_image_button
submit_image_button = st.button('SUBMIT')

#initializing a session variable to store state of image submit button
if 'submit_image_button_state' not in st.session_state:
    st.session_state.submit_image_button_state = False

#what happens when submit_image_button is pressed
if submit_image_button or st.session_state.submit_image_button_state :
    
        #changing the state of submit_image_button to True and storing it.
        st.session_state.submit_image_button_state = True

        #what happpens when Image is properly uploaded
        if st.session_state.uploaded_img is not None:

            #opening image into a variable  using PIL Image.open() function
            image = Image.open(st.session_state.uploaded_img)

            #displaying the image on page
            st.image(image, caption='Your Uploaded Image', use_column_width='always')

            #saving the image in a folder for further processing; new image  automatically overwrites older one, if exists
            with open(os.path.join("img", 'img.jpeg'),"wb") as f: 
                f.write(st.session_state.uploaded_img.getbuffer())   

            #loading the saved image
            Img = "img\img.jpeg"
            
	    ####################################################
	    ####################################################
	    #passing the image into Componet Detetcion function
            #and fetching list of detected components
            
            #initializing a session variable to store the fetched list of detected components
            if 'components' not in st.session_state:
                st.session_state.components = []
		
	    components = ElelctronicEye(Img)

            #storing the list of detected components in the respective session variable
            st.session_state.components = components

            #---------------------------------------------------------------------------------------------------------------------------------
            # CODE TO NUMBER THE REPEATED COMPONENTS IN THE DETECTED COMPONENT LIST AND DISPLAYING THEM AS STRING.

            #initializing a session variable to store the lists of numbered  repeated components from the detected component list
            if 'components_numbered' not in st.session_state:
                st.session_state.components_numbered = []

            #generating the numbered list of components and storing it in respective session variable
            st.session_state.components_numbered = list(map(lambda x: x[1] + str(st.session_state.components[:x[0]].count(x[1]) + 1) if st.session_state.components.count(x[1]) > 1 else x[1], enumerate(st.session_state.components)))

            #initialising a session varible to store final string of numbered components
            if 'components_numbered_string' not in st.session_state:
                st.session_state.components_numbered_string = ""
            #rendering the items in the list as string
            st.session_state.components_numbered_string = 'Following components detected : ' + '' +  ' ; '.join(st.session_state.components_numbered)

            #displaying the string
            st.write(st.session_state.components_numbered_string) 

            #a divider  for some aesthetics 
            st.markdown('--------------------------------------------------------------------------')
            #---------------------------------------------------------------------------------------------------------------------------------


            #---------------------------------------------------------------------------------------------------------------------------------
            #CODE TO 

            #initializing button to display input for and  specifications
            choose_specs_button = st.button('CHOOSE SPECIFICATION')
            #what happens when choose specification button is pressed

            #initializing a session variable to store state of choose specification button
            if "choose_specs_button_state" not in st.session_state:
                st.session_state.choose_specs_button_state = False
        
            if choose_specs_button or  st.session_state.choose_specs_button_state:

                #changing the state of choose_specs_button to True and storing it.
                st.session_state.choose_specs_button_state = True

                # print(type(st.session_state.components_numbered))

                #a parallel iteration to fetch components and their numbered version from respective lists.
                for (component,component_numbered) in zip(st.session_state.components,st.session_state.components_numbered):

                    #initialising a session variable to store in a list: [component, {'specification': 'value'}]
                    if component_numbered not in st.session_state:
                        st.session_state[f'{component_numbered} Specifications'] = []
                    #appending component (name) in the list
                    st.session_state[f'{component_numbered} Specifications'].append(component)
                    #displaying corresponding component numbered as header
                    st.subheader(component_numbered)
                    #displaying the list of specification corresponding to the component
                    #st.text(st.session_state.component_dict.get(component))

                    #an iteration to fetch each specification form the list of specification corresponding to the component
                    for specification in st.session_state.component_dict.get(component):
                        #st.text(specification)

                        #initializing a session variable to store user input corresponding to each specification of the component
                        if f'{specification}_of_{component_numbered}' not in st.session_state:
                            st.session_state[f'{specification}_of_{component_numbered}'] = ""
                        
                        #generating a text-input area for the component in the iteration and
                        #storing the user input in the respective session variable
                        st.session_state[f'{specification}_of_{component_numbered}'] = st.text_input(
                            f'Choose {specification} for {component_numbered}', 
                            key = f'NumberInputOf_{specification}_of_{component_numbered}')

                        #displaying the entered value below the input area
                        st.write(st.session_state[f'{specification}_of_{component_numbered}'])
                        
                        #appending the dictionary : {'specification': 'value'} , in the list for [component, {'specification': 'value'}]
                        st.session_state[f'{component_numbered} Specifications'].append({f'{specification}' : str(st.session_state[f'{specification}_of_{component_numbered}'])})

                        
                    

                    if f'submit_specs_button_for_{component_numbered}' not in st.session_state:
                        st.session_state[f'submit_specs_button_for_{component_numbered}'] = ''
                    st.session_state[f'submit_specs_button_for_{component_numbered}'] = st.button(f'SUBMIT {component_numbered} Specifications')

                    if f'submit_specs_button_state_for_{component_numbered}' not in st.session_state:
                        st.session_state[f'submit_specs_button_state_for_{component_numbered}'] = False


                    if st.session_state[f'submit_specs_button_for_{component_numbered}'] or st.session_state[f'submit_specs_button_state_for_{component_numbered}'] :
                        st.session_state[f'submit_specs_button_state_for_{component_numbered}'] = True

                        if f'Final_List_Of_{component_numbered}_Specifications' not in st.session_state:
                            st.session_state[f'Final_List_Of_{component_numbered}_Specifications'] = []
                        st.session_state[f'Final_List_Of_{component_numbered}_Specifications'].append(f'{component}')          
                        for dict in st.session_state[f'{component_numbered} Specifications'][1:]:
                            for k,v in dict.items():
                                if v != '':
                                    st.session_state[f'Final_List_Of_{component_numbered}_Specifications'].append({k:v})
                        #st.write(st.session_state[f'Final_List_Of_{component_numbered}_Specifications'])
                        

                        if f'query_of_{component_numbered}' not in st.session_state:
                            st.session_state[f'query_of_{component_numbered}'] = ""         
                        st.session_state[f'query_of_{component_numbered}'] = st.session_state[f'Final_List_Of_{component_numbered}_Specifications'][0] + " "
                        for i in range(1,len(st.session_state[f'Final_List_Of_{component_numbered}_Specifications'])):
                            for key in st.session_state[f'Final_List_Of_{component_numbered}_Specifications'][i]:
                                st.session_state[f'query_of_{component_numbered}'] += key + " " + st.session_state[f'Final_List_Of_{component_numbered}_Specifications'][i][key] + " "
                        #st.write(st.session_state[f'query_of_{component_numbered}'])


                        st.session_state[f'query_of_{component_numbered}'] = st.session_state[f'query_of_{component_numbered}'].replace(' ', '+')
                        HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
                        if f'link_for_{component_numbered}' not in st.session_state:
                            st.session_state[f'link_for_{component_numbered}'] = ''
                        st.session_state[f'link_for_{component_numbered}'] = requests.get('https://octopart.com/search?q='+ st.session_state[f'query_of_{component_numbered}'] +'&currency=USD&specs=0', headers=HEADERS).url
                        st.write(f'Link for {component_numbered} : ' + st.session_state[f'link_for_{component_numbered}'] )
                        st.session_state[f'Final_List_Of_{component_numbered}_Specifications'].clear()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)                      

                        
                        
            
	                            

                        

                        


                                    
                        



                




                        

