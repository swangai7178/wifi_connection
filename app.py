from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",  # Replace with your MySQL server address
    "user": "root",  # Replace with your MySQL username
    "password": "",  # Replace with your MySQL password
    "database": "wifi_config",  # Replace with your MySQL database name
}


def connect_to_database():
    return mysql.connector.connect(**db_config)


# Simulated user data (you should use a database)
users = {
    "user123": {
        "subscription_status": True,
        "wifi_ssid": "YourWiFiSSID",
        "wifi_password": "YourWiFiPassword",
        "subscription_type": "Premium",
        "subscription_expires": "31st October 2023",
    },
    "user456": {
        "subscription_status": False,
        "wifi_ssid": "YourWiFiSSID",
        "wifi_password": "YourWiFiPassword",
        "subscription_type": "Basic",
        "subscription_expires": "15th December 2022",
    },
    # Add more user data as needed
}


def is_subscription_active(user_id):
    user = users.get(user_id)
    if user:
        return user["subscription_status"]
    return False


def connect_to_wifi(user_id):
    user = users.get(user_id)
    if user:
        ssid = user["wifi_ssid"]
        password = user["wifi_password"]
        # Replace this line with the actual command to connect to Wi-Fi
        return f"Connected to Wi-Fi network '{ssid}' with password '{password}'"
    return "User not found or subscription inactive"


@app.route("/")
def home():
    user_id = request.args.get("user_id")
    if user_id:
        user = users.get(user_id)
        if user:
            if is_subscription_active(user_id):
                return render_template("dashboard.html", user_id=user_id, user=user)
            else:
                return render_template(
                    "subscription_expired.html", user_id=user_id, user=user
                )

    return redirect(url_for("login_page"))


@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        # Check if the user already exists in the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template(
                "signup.html",
                alert="User already exists. Please choose a different username.",
            )

        # If the user doesn't exist, insert them into the database
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, password) VALUES (%s, %s)", (user_id, password)
        )
        conn.commit()
        conn.close()

        # Redirect to the login page or any other page as needed
        return redirect(url_for("login_page"))

    return "Invalid request method."


@app.route("/payment_page.html")
def payment_page():
    user_id = request.args.get("user_id", "").strip()

    if user_id:
        return render_template("payment_page.html", user_id=user_id)
    else:
        # Handle the case when user_id is empty
        return "User ID is missing or invalid."


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get(
        "password"
    )  # Add this line to get the password from the form

    if user_id and password:
        # Connect to the database
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check if the user exists and the password is correct
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if (
            user and user[2] == password
        ):  # Assuming the password is stored in the third column of the 'users' table
            if is_subscription_active(user_id):
                conn.close()
                return redirect(url_for("home", user_id=user_id))
            else:
                conn.close()
                return redirect(url_for("home", user_id=user_id))
        else:
            conn.close()
            return render_template("login.html", alert="Invalid username or password")

    # If user_id or password is missing or invalid, return to the login page
    return redirect(url_for("login_page"))


@app.route("/payment_success")
def payment_success():
    # You can render a template for the payment success page here
    return render_template("payment_success.html")


@app.route("/connect_wifi", methods=["POST"])
def connect_wifi():
    user_id = request.form.get("user_id")
    if user_id and is_subscription_active(user_id):
        result = connect_to_wifi(user_id)
        return result
    return "Subscription not active. Cannot reconnect Wi-Fi."


@app.route("/process_payment", methods=["POST"])
def process_payment():
    if request.method == "POST":
        # Retrieve payment details from the form
        amount = request.form.get("amount")
        phone_number = request.form.get("phone_number")

        # Use the Daraja API or your chosen payment gateway to initiate the payment
        # Handle payment processing logic here

        # Redirect to a payment success or failure page
        # You'll need to create these pages

        return redirect(url_for("payment_success"))  # Use url_for to specify the route
        # or
        # return redirect(url_for("payment_failure"))

    return "Invalid request method."


if __name__ == "__main__":
    app.run(host="192.168.0.100", port=5000, debug=True)
