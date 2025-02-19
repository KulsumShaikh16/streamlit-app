import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title = "Data Sweeper", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp {
       background-color: #f5f5f5;
       color:white
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#title and description
st.title("Data Growth")
st.write("This page is for data growth")

#file upload
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"],accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Invalid file format: {file.ext}")
            continue

        #file details
        st.write("Preview of the file")
        st.dataframe(df.head())
        

        #data cleaning and transformation
        st.subheader("Data Cleaning and Transformation")
        if st.checkbox("Remove duplicates{file.name}"):
           col1, col2 = st.columns(2)
           with col1:
              if st.button(f"Remove duplicates:{file.name}"):
                 df.drop_duplicates(inplace=True)
                 st.write("Duplicates removed")

              with col2:
                    if st.button("Show duplicates{file.name}"):
                        numeric_cols = df.select_dtypes(includes=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Duplicates shown")

        st.subheader("Select columns to Keep")
        selected_columns = st.multiselect("Select columns to keep {file.name}", df.columns, defauly=df.columns)
        df = df[selected_columns]
  #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"show visualizations {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

  #conversion options

        st.subheader("Conversion Options")
        convert_format = st.radio(f"Convert {file.name} to", ["csv", "xlsx"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if convert_format == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"

            elif convert_format == "xlsx":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(
                    label=f"Click here to download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mine_type,
                )

        st.success("All files processed successfully.")
        