# These are Python modules being imported.
import pandas as pd
import webbrowser
from tkinter import Tk
from tkinter import filedialog

""" `Tk().withdraw()` is a method from the tkinter module in Python that hides the main window of the
tkinter application. In this code, it is used to hide the main window so that only the file dialog
box is displayed when the user selects a file."""
Tk().withdraw()


"""`file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])` opens a file dialog
 box that allows the user to select an Excel file with the extension ".xlsx". The selected file path
is then stored in the variable `file_path`."""
file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])

"""This code block checks if a file path has been selected by the user using a file dialog box. If a
file path has been selected, it reads the Excel file using pandas and stores the data in a DataFrame
called `df`. It then prints the shape of the DataFrame. If no file path has been selected, it prints
"No file selected." """
if file_path:
    
    df = pd.read_excel(file_path)
    
    print("DataFrame shape:", df.shape)
else:
    print("No file selected.")
    
    

    
""" `df_second` is a new DataFrame that is created by selecting specific columns from the original
DataFrame `df`. The selected columns are 'ID', 'Type', 'Subject', 'State', 'Assigned User', 'Total
number of tests executed?', 'Number of tests Passed', 'Number of tests Failed', 'Test Report
Checkpoint Label', and 'Test Data Checkpoint Label'."""
df_second = df [['ID', 'Type', 'Subject', 'State', 'Assigned User', 'Total number of tests executed?',
                'Number of tests Passed', 'Number of tests Failed', 'Test Report Checkpoint Label',
                'Test Data Checkpoint Label']]
user_data = df_second.to_html(index=False)



"""`df_state = df['State']` selects the column 'State' from the DataFrame `df` and assigns it to a new
variable `df_state`."""
df_state = df['State']
state_counts = df_state.value_counts()

""" `state_labels` is a list of the unique values in the 'State' column of the DataFrame `df`, and
`state_values` is a list of the count of each unique value in the 'State' column. These lists are
used to create a pie chart in the HTML file that displays the distribution of the 'State' column."""
state_labels = state_counts.index.tolist()
state_values = state_counts.tolist()


"""This code block is calculating the total number of tests passed and failed from the 'Number of tests
 Passed' and 'Number of tests Failed' columns of the DataFrame `df_second`. It then creates two
 lists, `labels` and `values`, where `labels` contains the strings 'Passed' and 'Failed', and
`values` contains the total number of tests passed and failed, respectively. These lists are used to
 create a pie chart in the HTML file that displays the distribution of passed and failed tests."""
passed_count = df_second['Number of tests Passed'].sum()
failed_count = df_second['Number of tests Failed'].sum()
labels = ['Passed', 'Failed']
values = [passed_count, failed_count]



""" `state_chart_script` is a string variable that contains JavaScript code for creating a pie chart
 using the Chart.js library. The chart displays the distribution of values in the 'State' column of
 the DataFrame `df`. The chart is created using a canvas element with the id 'stateChart'. The chart
 data is defined in the `stateData` object, which contains an array of labels and an array of data
 values. The chart options are defined in the `stateOptions` object, which includes options for
 displaying data labels and formatting the labels. The `Chart` constructor is used to create a new
 chart object with the specified options and data. The resulting chart is displayed in the canvas
 element with the id 'stateChart'."""
state_chart_script = f"""
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels"></script>
<canvas id="stateChart"></canvas>
<script>
    var ctx_state = document.getElementById('stateChart').getContext('2d');
    var stateData = {{
        labels: {state_labels},
        datasets: [{{
            data: {state_values},
            backgroundColor: [
                '#007bff',
                '#28a745',
                '#dc3545',
                '#ffc107',
                '#17a2b8',
                '#6c757d'
            ]
        }}]
    }};
    var stateOptions = {{
        responsive: true,
        plugins: {{
            datalabels: {{
                formatter: (value, ctx) => {{
                    let sum = 0;
                    let dataArr = ctx.chart.data.datasets[0].data;
                    dataArr.map(data => {{
                        sum += data;
                    }});
                    let percentage = (value * 100 / sum).toFixed(2) + "%";
                    return percentage;
                }},
                color: '#fff',
                font: {{
                    weight: 'bold'
                }}
            }}
        }}
    }};
    new Chart(ctx_state, {{
        type: 'pie',
        data: stateData,
        options: stateOptions
    }});
</script>
"""

""" `second_chart_script` is a string variable that contains JavaScript code for creating a pie chart
 using the Chart.js library. The chart displays the distribution of passed and failed tests from the
 'Number of tests Passed' and 'Number of tests Failed' columns of the DataFrame `df_second`. The
 chart is created using a canvas element with the id 'chart'. The chart data is defined in the `data`
 object, which contains an array of labels and an array of data values. The chart options are defined
 in the `options` object, which includes options for displaying data labels and formatting the
 labels. The `Chart` constructor is used to create a new chart object with the specified options and
 data. The resulting chart is displayed in the canvas element with the id 'chart'."""
second_chart_script = f"""
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    var ctx = document.getElementById('chart').getContext('2d');
    var data = {{
        labels: {labels},
        datasets: [{{
            data: {values},
            backgroundColor: [
                'green',
                'red'
            ]
        }}]
    }};
    var options = {{
        responsive: true,
        plugins: {{
            legend: {{
                display: true
            }},
            datalabels: {{
                formatter: (value, ctx) => {{
                    let sum = data.datasets[0].data.reduce((a, b) => a + b, 0);
                    let percentage = (value * 100 / sum).toFixed(2) + "%";
                    return percentage;
                }},
                color: '#fff',
                font: {{
                    weight: 'bold'
                }}
            }}
        }},
    }};
    new Chart(ctx, {{
        type: 'pie',
        data: data,
        options: options
    }});
</script>
"""




"""The above code is defining a string variable `first_page_content` which contains HTML, CSS, and
 JavaScript code for a dashboard webpage. The webpage includes a title, a header, a frame with
 project information and a button to navigate to a user page. It also includes a canvas element for a
 state chart, and a script for generating the state chart."""
first_page_content = f"""
<html>
<head>
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-image:linear-gradient(to right, #DECBA4, #3E5151);
        }}
        #frame-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #frame {{
            width: 600px;
            height: 600px;
            background-color: #D0D0D0;
            border: 5px solid #3E5151;
            border-radius: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 20px;
            box-sizing: border-box;
            text-align: center;
            margin-top:5px;
        }}
        header.container {{
            color: #333;
            margin-bottom: 10px;
            text-align:center;
        }}
        h1{{
            text-align:center;
            color:#3E5151;
            font-size:80px;
            margin-top: 5px;
            text-shadow: 5px 2px #222324, 2px 4px #222324, 3px 5px #222324
            
        }}
        title{{
            font-size : 100px;
            height: 50px;
        }}
        #stateChart {{
            display: block;
            margin: 0 auto;
            max-width: 100%;
            max-height: 100%;
        }}
        .button-container {{
            text-align: center;
            margin-top: 20px;
        }}
        .button {{
            background-color: #000000;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            animation: animate 8s 1;
        }}
        .button:hover {{
            background-color: #555555;
            color: #fff;
        }}
    </style>
    <script>
        function openUserPage() {{
            window.location.href = 'user.html';
        }}
    </script>
</head>
<body>
    <div class="w3-container w3-cursive w3-center w3-animate-top">
        <title>  Dashboard  </title>
        <h1> Welcome To Dashboard ! </h1>
    </div>
    <div id="frame-container">
        <div id="frame">
            <h2>Project - T1XX_GLOBAL B</h1>
            <h3>SW Release : SW38.0.2</h2>
            <canvas id="stateChart"></canvas>
            <div class="button-container">
                <button class="button" onclick="openUserPage()">User</button>
            </div>
        </div>
    </div>
    {state_chart_script}
</body>
</html>
"""




"""The above code is defining a string variable `second_page_content` that contains an HTML code for a
 dashboard page with a title, a heading, a chart, and a table. The HTML code also includes CSS
 styling for the page elements. The `user_data` and `second_chart_script` variables are expected to
 be defined elsewhere and will be inserted into the HTML code using string formatting."""
second_page_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-image:linear-gradient(to right, #DECBA4, #3E5151);
        }}
        h1 {{
            color:#3E5151;
            margin-top: 1px;
            font-size:50px;
        }}
        #chart {{
            display: block;
            margin: 0 auto;
            width: 300px;
            height: 200px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color:#3E5151;
        }}
    </style>
</head>
<body>
    <div class="heading-container">
        <title>  Dashboard  </title>
        <h1>Test Count</h1>
        <canvas id="chart"></canvas>
    </div>
    <div>
        <table>
            {user_data}
        </table>
    </div>
    {second_chart_script}
</body>
</html>
"""

""" The above code is creating a new file named "Dashboard.html" and writing the contents of the
 variable "first_page_content" to it. The file is opened in write mode using the 'w' parameter. The
 'with' statement is used to ensure that the file is properly closed after writing. The 'close()'
 method is not necessary since the file is automatically closed when the 'with' block is exited."""
with open('Dashboard.html', 'w') as f:
    f.write(first_page_content)
f.close()

    
""" The above code is writing the contents of the variable `second_page_content` to a file named
 `user.html`. The `with` statement is used to open the file in write mode and automatically close it
 when the block of code is finished. The `close()` method is not necessary since the file is
 automatically closed by the `with` statement."""
with open('user.html', 'w') as f:
    f.write(second_page_content)
f.close()

""" The above code is using the `webbrowser` module in Python to open a file named "Dashboard.html" in
 the default web browser of the user's system."""
webbrowser.open('Dashboard.html')