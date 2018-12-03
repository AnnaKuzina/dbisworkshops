"""
Створити два словника User, Gift
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

first_table_dict = {
    "user_name": "Bob",
    "user_age": "20"
}

second_table_dict = {
    "gift_name": "Ball",
    "gift_price": "20",
    "gift_description": "Ball red"
}
available_dictionary = dict.fromkeys(['user', 'gift', 'all'], "dictionary_name")


@app.route('/api/<action>', methods=['GET'])
def apiget(action):
    if action == "user":
        return render_template("user.html", user_result=first_table_dict)

    elif action == "gift":
        return render_template("gift.html", gift_result=second_table_dict)

    elif action == "all":
        return render_template("all.html", user_result=first_table_dict, gift_result=second_table_dict)

    else:
        return render_template("404.html", action_value=action)


@app.route('/api', methods=['POST'])
def apipost():
    # <button type="submit" form="form_user" name="action" value="user_update">Submit</button>
    # send name="action" and value="user_update" to POST

    if request.form["action"] == "update_user":
        first_table_dict["user_name"] = request.form["user_name"]
        first_table_dict["user_age"] = request.form["user_age"]
        return redirect(url_for('apiget', action="all"))

    if request.form["action"] == "update_gift":
        second_table_dict["gift_name"] = request.form["gift_name"]
        second_table_dict["gift_price"] = request.form["gift_price"]
        second_table_dict["gift_description"] = request.form["gift_description"]

        return redirect(url_for('apiget', action="all"))


if __name__ == '__main__':
    app.run()
