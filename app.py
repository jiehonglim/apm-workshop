import subprocess
import streamlit as st
import elasticapm

import requests
import random

from bs4 import BeautifulSoup

# Initialize Elasticsearch and APM clients
# Configure APM and Elasticsearch clients
@st.cache_resource
def initElastic():

    elastic_service = {}

    output = subprocess.check_output(['bash', '-c', 'kubectl get service apm-lb | awk \'NR==2 {print $4}\''])

    # Decode the output from bytes to string
    service_url = output.decode().strip()

    with open('env.yaml') as myfile:
        for line in myfile:
            key, value = line.partition('=')[::2]
            elastic_service[key.strip()] = str(value).replace("\n", "")
        
    ELASTIC_APM = {
    'SERVICE_NAME': 'streamlit_test',
    'SECRET_TOKEN': elastic_service['elastic-apm-secret-token'],
    'SERVER_URL': 'http://' + service_url + ':8200',
    'ENVIRONMENT': 'Py Prod',
    }

    apmclient = elasticapm.Client(ELASTIC_APM)
    elasticapm.instrument()
    return apmclient

@elasticapm.capture_span("Make a Request")
def make_a_req(url, apmclient, method='GET', data=None, headers=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        apmclient.capture_exception()
        return False

@elasticapm.capture_span("Get Page Title")
def get_page_title(response):
    soup = BeautifulSoup(response.text, 'html.parser')        
    title = soup.title.string if soup.title else 'No title found'
    return title

@elasticapm.capture_span("Random URLs")
def return_a_url():
    urls = [
        "https://doesnt.exist",
        "https://www.elastic.co",
        "https://www.elastic.co/observability",
        "https://www.elastic.co/observability-labs",
        "https://generate.some.errors",
        "https://opentelemetry.io",
        "https://www.tech.gov.sg",
        "https://www.developer.tech.gov.sg",
        "http://docs.developer.tech.gov.sg/docs/stackops-documentation",
        "https://www.developer.tech.gov.sg/products/categories/devops/stackops/overview.html"
    ]
    random.shuffle(urls)
    return urls[0]

@elasticapm.capture_span("Dividing")
def divide(a, b):
    # if b == 0:
    #     raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def get_url(apmclient):
    apmclient.begin_transaction("I'm feeling lucky")
    elasticapm.set_transaction_name("Lucky URLs")
    url = return_a_url()
    apmclient.end_transaction("I'm feeling lucky")
    return url

def get_title(apmclient, url):
    try:
        apmclient.begin_transaction("I'm feeling lucky")
        elasticapm.set_transaction_name("Lucky Page Titles")
        response = make_a_req(url, apmclient)

        if response != False:
            title = get_page_title(response)
            apmclient.end_transaction("I'm feeling lucky")
            return title
        else:
            raise ValueError("Received an invalid response from make_a_req.")
        
    except Exception as e:
        # Capture the exception and end the transaction
        apmclient.capture_exception()
        apmclient.end_transaction("Transaction failed")
        return False       

def get_numbers(apmclient, dividend, divisor):
    try:
        apmclient.begin_transaction("I'm feeling lucky")
        elasticapm.set_transaction_name("Division")
        result = divide(dividend, divisor)
        apmclient.end_transaction("I'm feeling lucky")
        return result
    except ZeroDivisionError as e:
        apmclient.capture_exception()
        apmclient.end_transaction("Transaction failed")

st.title('Streamlit app with Elastic APM Python')

apmclient = initElastic()

if "url" not in st.session_state:
    st.session_state.url_button_clicked = False
    st.session_state.url = ""

if "title" not in st.session_state:
    st.session_state.title_button_clicked = False
    st.session_state.title = ""

if st.button("Generate Random URL", key="gen_url_button"):
    st.session_state.url_button_clicked = True
    st.session_state.title = ""
    st.session_state.url = get_url(apmclient)

if st.session_state.url != "":
    st.write(f"This is your random URL: {st.session_state.url}")

if st.button("Get Page Title", key="get_title_button"):
    if st.session_state.url != "":
        st.session_state.title_button_clicked = True
        st.write(f"Getting title from page: {st.session_state.url}")
        st.session_state.title = get_title(apmclient, st.session_state.url)
    else:
        st.write("Click the URL button first")

if st.session_state.title is False:
    st.write("Something bad happen, try again")
    
elif st.session_state.title != "":
    st.write(f"The page title is {st.session_state.title}")

st.subheader("Try creating an error, Dividend / Divisor")

dividend = st.slider("Select Dividend", 0, 100, 10, 1, key="dividend")
divisor = st.slider("Select Divisor", 0, 100, 10, 1, key="divisor")

btn_label = "Divide " + str(dividend) + "/" + str(divisor)

if st.button(btn_label, key="divide_button"):
    result = get_numbers(apmclient, dividend, divisor)
    st.write(f"The result is: {result}")
