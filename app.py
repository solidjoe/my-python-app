import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import random
import datetime

# 1. Database Connection Logic
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

# 2. Expert-Verified Stimuli List
stimuli = [
    {"verb": "जानना", "type": "factive", "sentence": "क्या राम जानता है कि दरवाज़ा खुला था?", "p": "दरवाज़ा खुला था"},
    {"verb": "समझना", "type": "factive", "sentence": "क्या सीता समझती है कि परीक्षा कठिन थी?", "p": "परीक्षा कठिन थी"},
    {"verb": "देखना", "type": "factive", "sentence": "क्या अमित ने देखा कि बत्ती जल रही थी?", "p": "बत्ती जल रही थी"},
    {"verb": "सुनना", "type": "factive", "sentence": "क्या रीता ने सुना कि घंटी बजी थी?", "p": "घंटी बजी थी"},
    {"verb": "पता चलना", "type": "factive", "sentence": "क्या राम को पता चला कि बारिश रुकी थी?", "p": "बारिश रुकी थी"},
    {"verb": "याद होना", "type": "factive", "sentence": "क्या सीता को याद था कि दुकान बंद थी?", "p": "दुकान बंद थी"},
    {"verb": "कहना", "type": "non-factive", "sentence": "क्या अमित ने कहा कि ट्रेन देर से आई थी?", "p": "ट्रेन देर से आई थी"},
    {"verb": "बताना", "type": "non-factive", "sentence": "क्या रीता ने बताया कि बैठक रद्द की गई थी?", "p": "बैठक रद्द की गई थी"},
    {"verb": "पूछना", "type": "non-factive", "sentence": "क्या राम ने पूछा कि रास्ता लंबा था?", "p": "रास्ता लंबा था"},
    {"verb": "सोचना", "type": "non-factive", "sentence": "क्या सीता ने सोचा कि फिल्म अच्छी थी?", "p": "फिल्म अच्छी थी"},
    {"verb": "मानना", "type": "non-factive", "sentence": "क्या अमित ने माना कि नियम सख़्त था?", "p": "नियम सख़्त था"},
    {"verb": "लगना", "type": "non-factive", "sentence": "क्या रीता को लगा कि मौसम ठंडा था?", "p": "मौसम ठंडा था"}
]

# 3. Session Management
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = random.randint(1000, 9999)
    st.session_state.step = 0
    st.session_state.blocks = random.sample(["Projection", "At-issueness"], 2)
    # Shuffle stimuli for each participant
    temp_list = stimuli.copy()
    random.shuffle(temp_list)
    st.session_state.stimuli = temp_list

# 4. App Interface
st.title("Hindi Linguistics Pilot Study")

if st.session_state.step < 24:
    current_idx = st.session_state.step % 12
    current_block = st.session_state.blocks[0] if st.session_state.step < 12 else st.session_state.blocks[1]
    item = st.session_state.stimuli[current_idx]

    # Display the sentence
    st.info(f"वाक्य: {item['sentence']}")

    # Display the judgment question based on the block
    if current_block == "Projection":
    label = f"क्या आप निश्चित हैं कि {item['p']}?"
    else:
    # The new, better At-issueness phrasing
    label = f"क्या यहाँ मुख्य बात यह है कि {item['p']}?"

    # 0-100 Slider
    rating = st.slider(label, 0, 100, 50)

    if st.button("अगला (Next)"):
        try:
            client = get_gspread_client()
            sheet = client.open("Hindi_Experiment_Data").sheet1
            
            # Save data
            row = [str(datetime.datetime.now()), st.session_state.participant_id, item['verb'], item['type'], current_block, rating]
            sheet.append_row(row)
            
            st.session_state.step += 1
            st.rerun()
        except Exception as e:
            st.error(f"Error saving data: {e}")
else:

    st.success("धन्यवाद! आपका डेटा सुरक्षित रूप से जमा हो गया है। (Thank you! Your data has been recorded.)")

