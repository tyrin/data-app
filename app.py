import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import os
import sys
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt
####################### UTILITY FUNCTIONS ####################
def convert_df(frame):#-------------------converts a dataframe to csv data
	return frame.to_csv().encode('utf-8')

def showresults(frame, file): #-----------displays data frame and lets you download it.
	#HtmlFile = open("data.html", 'r', encoding='utf-8')
	#source_code = HtmlFile.read()
	#components.html(source_code, height = 775,width=900)
	st.dataframe(frame)
	csv = convert_df(frame)
	csvname = file + ".csv"
	st.download_button(
	   "Press to Download",
	   csv,
	   csvname,
	   "text/csv",
	   key='download-csv'
	)
def mergeframes(leftframe, rightframe):#---merges two tables based on the Username column
	#mergeframe = pd.merge(leftframe, rightframe, on=["Username"])
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=["Username"])
#	st.write(mergeframe.shape)
	return(mergeframe)
####################### MAIN ####################
def main():
	st.markdown('## Data App')
	st.markdown('### Upload your data')
#	uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
#	for uploaded_file in uploaded_files:
#		bytes_data = uploaded_file.read()
#		st.write("filename:", uploaded_file.name)
#		st.write(bytes_data)