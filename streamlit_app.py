import numpy as np
import pandas as pd
import streamlit as st
import asyncio
from src.onederful import get_eligibility

# Show the page title and description.
st.set_page_config(
    page_title="Eligibility", 
    layout="wide",
    page_icon="🦷")
st.title("🦷 Eligibility - Onederful")
st.write("""\
This page documents the responses returned using the Onederful Sandbox [here](https://developers.onederful.co/documentation/#response-eligibility-and-benefits)
""")

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
# @st.cache_resource
# async def load_data():
#     data = await get_eligibility()
#     return data

data = asyncio.run(get_eligibility())

def normalize_column(x):
    if isinstance(x, list):
        return x  # Keep lists as they are
    elif pd.isnull(x):
        return []  # Keep NaN as is
    else:
        return []  # Replace non-list, non-null values with an empty list


st.write("""\
Each request requires the following information (examples filled in):
""")
request_df = pd.json_normalize({
                "subscriber": {               
                    "first_name": "TEST",               
                    "last_name": "PERSON",               
                    "dob": "01/01/2011",               
                    "member_id": "1234567890"           
                },           
                "provider": {               
                    "npi": "1234567890"           
                },           
                "payer": {               
                    "id": "AETNA_DENTAL_PLANS"         
                },           
                "version": "v2"       
})
st.dataframe(request_df, use_container_width=True)
st.write("""\
... which gets returned as the following
""")
subscriber_df = pd.json_normalize(data['subscriber'])
st.dataframe(subscriber_df, use_container_width=True)
st.write("""\
Below is all of the data that gets returned:
""")

deductible, maximum, coinsurance, limitations, exceptions = st.tabs(['Deductible', 'Maximums', 'Coinsurance', 'Limitations', 'Exceptions'])


with deductible:
    st.write("Deductibles")
    deduct_df = pd.DataFrame(data['deductible'])
    st.dataframe(deduct_df, use_container_width=True)


with maximum:
    st.write("Maximums")
    max_df = pd.DataFrame(data['maximums'])
    st.dataframe(max_df, use_container_width=True)


with coinsurance:
    st.write("Coinsurance")
    coins_df = pd.DataFrame(data['coinsurance'])
    st.dataframe(coins_df, use_container_width=True)


with limitations:
    st.write("Limitations")
    limits_df = pd.DataFrame(data['limitations'])
    limits_df['service_dates'] = limits_df['service_dates'].apply(normalize_column)
    limits_df['eligibility_details'] = limits_df['eligibility_details'].apply(normalize_column)
    limits_df['service_dates'] = limits_df['service_dates'].apply(
    lambda x: [f"{d['procedure_code']} : ({d['service_date']})" for d in x] if isinstance(x, list) else ''
    )
    limits_df['eligibility_details'] = limits_df['eligibility_details'].apply(
    lambda x: [
        f"{d['eligibility']} : ({d['date']})" if 'date' in d else f"{d['eligibility']}" 
        for d in x
    ] if isinstance(x, list) else ''
)

    st.dataframe(limits_df, use_container_width=True)


with exceptions:
    st.write("Exceptions (not covered)")
    except_df = pd.DataFrame(data['not_covered'])
    st.dataframe(except_df, use_container_width=True)
