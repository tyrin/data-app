#run from app.py
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
def mergeframes(leftframe, rightframe, column):#---merges two tables based on the Username column
	#mergeframe = pd.merge(leftframe, rightframe, on=["Username"])
	mergeframe = pd.merge(rightframe, leftframe, how="outer", on=column)
#	st.write(mergeframe.shape)
	return(mergeframe)
def comboframes(leftframe, rightframe, column):#---merges two tables based on the Username column
	comboframe = pd.merge(rightframe, leftframe, how="outer", on=column)
#	st.write(mergeframe.shape)
	return(comboframe)

####################### MAIN ####################
def main():
	st.markdown('## Data App')
#---------------------------Sidebar--------------------------
	todo = st.sidebar.selectbox("Do you want to:",
		['<select>', "Enhance Confluence Data", "Merge Two Files", "Beta"])

#---------------------------Sidebar Logic --------------------------
	if todo == "<select>":
		st.write("Use the sidebar to the left to select about views or edits of Confluence pages.")

	if todo == "Enhance Confluence Data":
		#seldtype = st.radio("Viewtracker data type:", ('View Data', 'Edit Data',))
		selectviz = st.sidebar.radio("Select a visualization", ('Stacked Bar Graph', 'Organizational Sunburst', 'Parallel Categories', 'Three Dimensional Scatterplot', 'Beta',))
		cfile = st.file_uploader("Upload a Confluence Viewtracker file")
		ofile = st.file_uploader("Upload another data file")
		fixUsername = st.checkbox('Update Username column?', value=True,)
		if cfile is not None and ofile is not None:
			#dataframe = pd.read_csv(uploaded_file)
			otherdata = pd.read_csv(ofile)
			confdata = pd.read_csv(cfile)
			if fixUsername:
				st.write('Updated Username column to show full email')
				confdata['Username'] = confdata['Username'].astype(str)  + "@salesforce.com"
			st.write("Enter the name of the column used to combine the files:")
			colname = st.text_input('Column name')
			vf = mergeframes(otherdata, confdata, colname)

			#drop null values, because otherwise the data can't be used.
			UseIncomplete = st.sidebar.radio("Use incomplete data?", ('Yes','No')) #---------------Use Incomplete Data or Not?
			if UseIncomplete == 'No':
				vf = vf.dropna()
			else:
				vf = vf.fillna(value='Unknown')
			if colname is not None:
				graphs(vf, selectviz, todo)
	if todo == "Merge Two Files":
		st.markdown('### Combine two files')
		uploaded_files = st.file_uploader("Step 1: select two files to combine.", accept_multiple_files=True)
		if len(uploaded_files) < 2 or len(uploaded_files) > 2:
			st.write("Select exactly 2 files")
		if len(uploaded_files) == 2:
			file1 = pd.read_csv(uploaded_files[0])
			file2 = pd.read_csv(uploaded_files[1])
			st.write("Enter the name of the column used to combine the files:")
			combo = st.text_input('Column name')
			if combo is not None:
				st.write("Combine on column: " + combo)
				cf = comboframes(file1, file2, combo)
			#View the data?
			option = st.selectbox('Do you want to view, visualize, or download data?',
			('View Data', 'Visualize Data', 'Download Data'))
			if option == 'View Data':
			#	st.write(mergeframe.shape)
				st.write("Filename:", uploaded_files[0].name)
				st.write("Records and columns:", file1.shape)
				st.write(file1)
				st.write("filename:", uploaded_files[1].name)
				st.write("Records and columns:", file2.shape)
				st.write(file2)
				st.write("filename: combo.csv")
				st.write("Records and columns:", cf.shape)
				st.dataframe(cf)
#		for uploaded_file in uploaded_files:
#			#bytes_data = uploaded_file.read()
#			st.write("filename:", uploaded_file.name)
#			dataframe = pd.read_csv(uploaded_file)
#			st.write(dataframe)
#			# df.get("firstname")
#--------------------SELECT GRAPH TYPE-------------------------
def graphs(df, selectviz, todo):
	#Get unique values for user input
	spaces = df['Space Name'].unique()
	orgs = df['Cost Center'].unique()
	roles = df['Role'].unique()
	if selectviz == "Stacked Bar Graph":
		st.header( selectviz + " for Views")
		viewstackedbartitle = "Views By "
		stackedbar(df, viewstackedbartitle)
		showresults(df, todo)
	elif selectviz == "Organizational Sunburst": #-------------SUNBURST
		st.write("Organizational Sunburst")
		sunburst(df)
		showresults(df, todo)
	elif selectviz == "Parallel Categories": #-----------------PARALLEL CATEGORIES
		st.write("Parallel Categories")
		parallelCategories(df)
	elif selectviz == "Beta": #--------------------------------Beta
		st.write("Combined Raw Data")
		st.dataframe(df)
		#assign a unique ID for all users based on username
		df['User ID'] = df.groupby(['Username']).ngroup()

		st.write("Anonymous Raw Data")
		st.dataframe(df)
		st.write("Download Anonymous View Data")
		#showresults(dfff, ref, physics)
		st.write("Anonymous Edit Data")
#		detail(ef)
## search type input
#	searchterm = st.sidebar.text_input('Enter a keyword', value="", max_chars=25)
#	search = st.sidebar.radio(
#		"Keyword search for:",
#		('Role', 'Manager', 'Page', 'Space'))


####################### RENDERING FUNCTIONS ####################
#---------------------------Stacked Bar--------------------------
def stackedbar(frame, title):
	#st.markdown("# Select view comparisons")
	collist = list(frame)
	colsort  = np.sort(collist)
	colbar = colsort
	colseg = colsort
	col1, col2= st.columns(2)
	with col1:
#		st.markdown('**Bars:**')
#		st.write(collist)
		xselect = st.selectbox('Select Columns:', colbar)
	with col2:
#		st.markdown('**Colors:**')
		cselect = st.selectbox('Select Segments:', colseg)

	fig = px.histogram(frame, x=xselect, color=cselect)
	fig.update_layout(
		height=600,
		width=1000
	)
	st.plotly_chart(fig, use_container_width=True)

#---------------------------Sunburst--------------------------
def sunburst(frame):
	# insert at index 0 column Visits with value 1
	sdf=frame.assign(Views=1)
	#st.dataframe(sdf)

	fig1 = px.sunburst(sdf, path=['Country', 'State/Province', 'City'], values='Views',
		color='Country',
		color_continuous_scale="RdYlGn",
		width=750, height=750
	)
	fig2 = px.sunburst(sdf, path=['Mgmt Chain - Level 02', 'Mgmt Chain - Level 03', 'Mgmt Chain - Level 04', 'Mgmt Chain - Level 05'],
		values='Views',
		color='Mgmt Chain - Level 05',
		color_continuous_scale='RdBu',
		width=750, height=750
	)
	fig3 = px.sunburst(sdf, path=['Space Name', 'Content Type', 'Visit ID', 'Content Title'],
		values='Views',
		color='Space Name',
		color_continuous_scale='RdBu',
		width=750, height=750
	)
	st.markdown('## By Country, State, and City')
	st.plotly_chart(fig1, use_container_width=True)
	st.markdown('## By Management Chain')
	st.plotly_chart(fig2, use_container_width=True)
#	st.markdown('**Views by Space Name, Content Type, Visit ID, and Content Title**')
#	st.plotly_chart(fig3, use_container_width=True)
#---------------------------Parallel Categories--------------------------
def parallelCategories(frame):
	st.dataframe(frame)
	collist = list(frame)
	colsort  = np.sort(collist)
	colbar = colsort
	colseg = colsort
	col1, col2= st.columns(2)
	with col1:
#		st.markdown('**Bars:**')
#		st.write(collist)
		xselect = st.multiselect('Select Categories:', colbar)
		fframe = frame.loc[:, xselect]
	with col2:
		clrlist = list(fframe)
		clrsort  = np.sort(clrlist)
		clrbar = clrsort

#		st.markdown('**Colors:**')
		cselect = st.selectbox('Select Color:', clrbar)

		#Add a count of unique values for the color scale
		#frame['Counts'] = frame.groupby(['Title'])['Space Key'].transform('count')
		fframe['Counts'] = fframe.groupby(by=[cselect]).transform('count')

	#fig = px.parallel_categories(frame)

	fig = px.parallel_categories(fframe, color="Counts", color_continuous_scale=px.colors.sequential.Rainbow)
	st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
	main()