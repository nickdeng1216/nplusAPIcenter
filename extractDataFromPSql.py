from flask import Flask
import psycopg2
from flask import request
from flask import render_template
import os
import json

app = Flask(__name__)
t_host = "10.16.18.10"  # either a domain name, an IP address, or "localhost"
t_port = "5432"  # This is the default postgres port
t_dbname = "ATC_Odoo"
t_user = "postgres"
t_pw = "Atc@2019"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()
directory = os.getcwd() + os.sep


@app.route("/")
@app.route("/export", methods=['POST'])
def csv_export():
    s = "SELECT *"
    s += " FROM "
    s += "stock_picking"
    raw_content = request.get_data().decode('utf-8')
    content = json.loads(raw_content)
    # s = content['sql']

    # set up our database connection.
    # conn = psycopg2.connect(host=t_host, dbname=t_dbname, user=t_user, password=t_pw)
    # db_cursor = conn.cursor()

    # Use the COPY function on the SQL we created above.
    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

    # Set up a variable to store our file path and name.
    t_path_n_file = directory + "result.csv"

    # Trap errors for opening the file
    try:
        with open(t_path_n_file, 'w') as f_output:
            db_cursor.copy_expert(SQL_for_file_output, f_output)
    except psycopg2.OperationalError as e:
        return 'Unable to connect!\n{0}'.format(e)
    except psycopg2.Error as e:
        return "Error: \n{0}".format(e) + "\n query we ran: " + s + "\n t_path_n_file: " + t_path_n_file
        # return render_template("error.html", t_message=t_message)

    # Success!

    # Clean up: Close the database cursor and connection
    db_cursor.close()
    db_conn.close()

    # Send the user on to some kind of informative screen.
    return "File is generated in {0}".format(t_path_n_file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6161)
