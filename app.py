from flask import Flask, render_template, Response, request, url_for, redirect
from flaskext.mysql import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sushi2021'
app.config['MYSQL_DATABASE_DB'] = 'TrainsDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/') #Landing Index page
def index():
    return render_template('index.html')


# Endpoint for search from sql
@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == "POST":
        if request.form['trains']: 
            trains = request.form['trains']

            cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id, addon_data from TrainsDB WHERE from_dest LIKE %s OR to_dest LIKE %s OR date_of_dep LIKE %s OR time_of_dep LIKE %s OR ticket_id LIKE %s OR addon_data LIKE %s" , (trains, trains, trains, trains, trains, trains))
            conn.commit()
            data = cursor.fetchall()
            if len(data) == 0 and trains == 'all': 
                cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id, addon_data from TrainsDB")
                conn.commit()
                data = cursor.fetchall()
            return render_template('search.html', data=data)
    return render_template('search.html')


# Endpoint for submit user choice from avalible tickets
@app.route("/submit", methods=['GET', 'POST'])
def results():

    if request.method == 'POST':
        user_data = request.form['user_choise']
        split_user_data = user_data.split(',')
        characters_to_remove = " ,()'r \ "
        clean_user_data = split_user_data

        for char in characters_to_remove:
            clean_user_data[0] = clean_user_data[0].replace(char, "")
            clean_user_data[1] = clean_user_data[1].replace(char, "")
            clean_user_data[2] = clean_user_data[2].replace(char, "")
            clean_user_data[3] = clean_user_data[3].replace(char, "")
            clean_user_data[4] = clean_user_data[4].replace(char, "")
            clean_user_data[5] = clean_user_data[5].replace(char, "")

        
        print("User Choice")
        print(clean_user_data[0])   # From
        print(clean_user_data[1])   # To
        print(clean_user_data[2])   # Date
        print(clean_user_data[3])   # Time
        print(clean_user_data[4])   # ID
        print(clean_user_data[5])   # Addon
        
        return render_template('present.html', data=clean_user_data)
  


# Endpoint for submit users ticket for change
@app.route("/submit_user_ticket", methods=['GET', 'POST'])
def submit_user_ticket():

    if request.method == 'POST':
        user_data = request.form['submit_user_ticket']
        split_user_data = user_data.split(',')
        characters_to_remove = " ,()' \ r "
        clean_user_data = split_user_data

        for char in characters_to_remove:
            clean_user_data[0] = clean_user_data[0].replace(char, "")
            clean_user_data[1] = clean_user_data[1].replace(char, "")
            clean_user_data[2] = clean_user_data[2].replace(char, "")
            clean_user_data[3] = clean_user_data[3].replace(char, "")
            clean_user_data[4] = clean_user_data[4].replace(char, "")
            clean_user_data[5] = clean_user_data[5].replace(char, "")

        print("User Choice")
        print(clean_user_data[0])   # From
        print(clean_user_data[1])   # To
        print(clean_user_data[2])   # Date
        print(clean_user_data[3])   # Time
        print(clean_user_data[4])   # ID
        print(clean_user_data[5])   # addon
        
        return render_template('users_ticket.html', data=clean_user_data)
  

# Endpoint for buy
@app.route("/buy", methods=['GET', 'POST'])
def buy():

    if request.method == "POST":
        user_ticket = request.form['buy']
        split_user_ticket = user_ticket.split(",")
        characters_to_remove = " [],()' \ r "
        clean_user_ticket = split_user_ticket

        for char in characters_to_remove:
            clean_user_ticket[0] = clean_user_ticket[0].replace(char, "")
            clean_user_ticket[1] = clean_user_ticket[1].replace(char, "")
            clean_user_ticket[2] = clean_user_ticket[2].replace(char, "")
            clean_user_ticket[3] = clean_user_ticket[3].replace(char, "")
            clean_user_ticket[4] = clean_user_ticket[4].replace(char, "")
            clean_user_ticket[5] = clean_user_ticket[5].replace(char, "")

        from_dest = clean_user_ticket[0]
        to_dest = clean_user_ticket[1]
        date_of_dep = clean_user_ticket[2]
        time_of_dep = clean_user_ticket[3]
        ticket_id = clean_user_ticket[4]
        addon_data = clean_user_ticket[5]

        cursor.execute("INSERT INTO UserDB (from_dest, to_dest, date_of_dep, time_of_dep, ticket_id, addon_data ) Values (%s, %s, %s, %s, %s, %s)", (from_dest, to_dest, date_of_dep, time_of_dep, ticket_id, addon_data ) )
        conn.commit()

    return render_template('receipt.html')


# Endpoint for change users choice
@app.route('/change', methods=['GET', 'POST'])
def change():

    if request.method == "POST":
        if request.form['trains']: 
            trains = request.form['trains']
            # search by date or trains
            cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id from UserDB WHERE from_dest LIKE %s OR to_dest LIKE %s OR date_of_dep LIKE %s OR time_of_dep LIKE %s OR ticket_id LIKE %s", (trains, trains, trains, trains, trains))
            conn.commit()
            data = cursor.fetchall()

            # all in the search box will return all the tuples
            if len(data) == 0 and trains == 'all': 
                cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id, addon_data from UserDB")
                conn.commit()
                data = cursor.fetchall()

            return render_template('change.html', data=data)

    return render_template('change.html')


# Endpoint for deleting tickets
@app.route("/sell", methods=['GET', 'POST'])
def sell():

    if request.method == "POST":
        user_ticket = request.form['sell']
        split_user_ticket = user_ticket.split(",")
        characters_to_remove = " [],()' \ r "
        clean_user_ticket = split_user_ticket

        for char in characters_to_remove:
            clean_user_ticket[0] = clean_user_ticket[0].replace(char, "")
            clean_user_ticket[1] = clean_user_ticket[1].replace(char, "")
            clean_user_ticket[2] = clean_user_ticket[2].replace(char, "")
            clean_user_ticket[3] = clean_user_ticket[3].replace(char, "")
            clean_user_ticket[4] = clean_user_ticket[4].replace(char, "")

        user_ticket_id = clean_user_ticket[4]
        cursor.execute("DELETE FROM UserDB WHERE ticket_id = %s", user_ticket_id)
        conn.commit()
    return render_template('receipt.html')


# Endpoint for add-ons
@app.route('/addons_present', methods=['GET', 'POST'])
def addons_present():

    add_on_list = ["Pets on board", "Food", "Bike", "Child"]
    return render_template('addons.html', data=add_on_list)

# Endpoint for Choosing addons
@app.route("/addons", methods=['GET', 'POST'])
def addons():

    if request.method == "POST":
        global user_addon
        user_addon = request.form['addons']
   
    return render_template('supplement.html', user_addon=user_addon)


# Endpoint for Choosing which ticket to suplement
@app.route("/supplement", methods=['GET', 'POST'])
def suplement():
    if request.method == "POST":
        if request.form['trains']: 
            trains = request.form['trains']
            # search by date or trains
            cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id from UserDB WHERE from_dest LIKE %s OR to_dest LIKE %s OR date_of_dep LIKE %s OR time_of_dep LIKE %s OR ticket_id LIKE %s", (trains, trains, trains, trains, trains))
            conn.commit()
            data = cursor.fetchall()

            # all in the search box will return all the tuples
            if len(data) == 0 and trains == 'all': 
                cursor.execute("SELECT from_dest, to_dest, date_of_dep, time_of_dep, ticket_id from UserDB")
                conn.commit()

                data = cursor.fetchall()

        return render_template('supplement.html', data=data, user_addon=user_addon )

    return render_template('supplement.html')



# Endpoint for submit users addon for change
@app.route("/submit_user_supp", methods=['GET', 'POST'])
def submit_user_supp():

    if request.method == 'POST':
        user_data = request.form['suplement']
        split_user_data = user_data.split(',')
        characters_to_remove = " ,()' \ r "
        clean_user_data = split_user_data

        for char in characters_to_remove:
            clean_user_data[0] = clean_user_data[0].replace(char, "")
            clean_user_data[1] = clean_user_data[1].replace(char, "")
            clean_user_data[2] = clean_user_data[2].replace(char, "")
            clean_user_data[3] = clean_user_data[3].replace(char, "")
            clean_user_data[4] = clean_user_data[4].replace(char, "")

        return render_template('user_supp.html', data=clean_user_data, user_addon=user_addon)




# Endpoint for buy
@app.route("/buy_addon", methods=['GET', 'POST'])
def buy_addon():

    if request.method == "POST":
        user_ticket = request.form['buy_addon']
        split_user_ticket = user_ticket.split(",")
        characters_to_remove = " [],()' \ r "
        clean_user_ticket = split_user_ticket

        for char in characters_to_remove:
            clean_user_ticket[0] = clean_user_ticket[0].replace(char, "")
            clean_user_ticket[1] = clean_user_ticket[1].replace(char, "")
            clean_user_ticket[2] = clean_user_ticket[2].replace(char, "")
            clean_user_ticket[3] = clean_user_ticket[3].replace(char, "")
            clean_user_ticket[4] = clean_user_ticket[4].replace(char, "")

        from_dest = clean_user_ticket[0]
        to_dest = clean_user_ticket[1]
        date_of_dep = clean_user_ticket[2]
        time_of_dep = clean_user_ticket[3]
        ticket_id = clean_user_ticket[4]
        
        cursor.execute("UPDATE UserDB SET addon_data = %s  WHERE ticket_id = %s", (user_addon,  ticket_id) ) 

        conn.commit()

    return render_template('receipt.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(host='127.1.2.3', port=port, debug=True)

