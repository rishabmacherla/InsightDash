from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

app = Flask(__name__)

@app.route('/')
def frontend():
    return render_template('frontend.html')

@app.route('/ppt')
def ppt():
    return render_template('ppt.html')

@app.route('/datareport', methods = ['POST', 'GET'])
def datareport():
    return render_template('datareport.html')

@app.route('/datastats', methods=['POST', 'GET'])
def datastat():
    if request.method == 'POST':
        excel_file_datareport = request.files['excel_file_datareport']
        if excel_file_datareport.filename == '':
            return render_template('error.html')
        elif 'xlsx' not in excel_file_datareport.filename:
            return render_template('error_wrong_file.html')
        excel_file_datareport.save(excel_file_datareport.filename)
        excel_data_datareport = pd.read_excel(excel_file_datareport)
        data_stats = {}
        no_of_rows = {}
        no_of_null_before = {}
        no_of_nulls_after = {}
        datatype = {}

        for i in excel_data_datareport.columns :
            no_rows = excel_data_datareport[i].count()
            no_nulls_before = excel_data_datareport[i].isna().sum()
            if (excel_data_datareport.dtypes[i] == "int64") or (excel_data_datareport.dtypes[i] == "float64"):
                mean_value = excel_data_datareport[i].mean()
                excel_data_datareport[i].fillna(value = mean_value, inplace = True)

            no_nulls_after = excel_data_datareport[i].isna().sum()

            data_type = excel_data_datareport.dtypes[i]
            no_of_rows[i] = no_rows
            no_of_null_before[i] = no_nulls_before
            no_of_nulls_after[i] = no_nulls_after
            datatype[i] = data_type

        data_stats["Number of Columns"] = len(excel_data_datareport.columns)
        data_stats["Number of Duplicate values"] = excel_data_datareport.duplicated().sum()
        data_stats["Number of Rows"] = no_of_rows
        data_stats["Number of Null values before"] = no_of_null_before
        data_stats["Number of Null values after"] = no_of_nulls_after
        data_stats["Data Type"] = datatype

        return render_template('datareport_output.html', result = data_stats)


@app.route('/uploader', methods = ['GET', 'POST'])
def reading_excel():
    if request.method == 'POST':
        excel_file = request.files['excel_file']
        if excel_file.filename == '':
            return render_template('error.html')
        elif 'xlsx' not in excel_file.filename:
            return render_template('error_wrong_file.html')
        excel_file.save(excel_file.filename)
        print(excel_file.filename)
        excel_data = pd.read_excel(excel_file)
        categorical_columns = []
        numeric_columns = []
        datetime_columns = []
        titles_filenames = {}

        for i in excel_data.columns:
            if 'datetime64' in str(excel_data.dtypes[i]):
                datetime_columns.append(i)
            elif (excel_data.dtypes[i] == "int64") or (excel_data.dtypes[i] == "float64"):
                numeric_columns.append(i)
            elif 'date' in i.lower():
                if excel_data.dtypes[i] != 'datetime64':
                    excel_data[i] = pd.to_datetime(excel_data[i])
                    print(excel_data.dtypes[i])
                    datetime_columns.append(i)
            else:
                categorical_columns.append(i)

        for i in excel_data:
            if (excel_data.dtypes[i] == "int64") or (excel_data.dtypes[i] == "float64"):
                excel_data[i] = excel_data[i].fillna(excel_data[i].mean())
            print(excel_data[i].isna().sum())
        for plots_a in numeric_columns:
            if len(categorical_columns) != 0:
                for plots_b in categorical_columns:
                    if len(excel_data[plots_b].unique()) <=10:
                        matplotlib.use('agg')
                        fig = plt.figure(num =1 , clear=True, figsize=(12,10))
                        sns.barplot(data=excel_data, x=plots_b, y=plots_a)
                        plt.xticks(rotation=45)
                        plots_b = plots_b.replace(" ", "")
                        print(plots_b)
                        name = plots_b
                        filepath = 'static/images/'
                        filenames = filepath + name + 'bargraph' + '.png'
                        fig.savefig(filenames)
                        title = "Bar graph representing " + plots_a + " by " + plots_b
                        titles_filenames[title] = filenames

            if len(datetime_columns) != 0:
                for plots_datetime in datetime_columns:
                    print(plots_datetime)
                    matplotlib.use('agg')
                    fig = plt.figure(num =1 , clear=True, figsize=(10,8))
                    sns.lineplot(data=excel_data, x=plots_datetime, y=plots_a)
                    plt.xticks(rotation=45)
                    if ' ' in plots_datetime:
                        plots_datetime.replace(' ','')
                    name = plots_datetime
                    filepath = 'static/images/'
                    filenames = filepath + name + 'linegraph' + '.png'
                    fig.savefig(filenames)
                    title = "Line graph representing " + plots_a + " by " + plots_datetime
                    titles_filenames[title] = filenames
        return render_template("output.html", result = titles_filenames)
    else:
        return render_template("error.html")


if __name__ == '__main__':
   app.run(port = 4000)