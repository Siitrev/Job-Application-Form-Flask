from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from utils.constants import SECRET_KEY, MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT
from datetime import datetime

# Create app instance
app = Flask(__name__)

# Set config
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

# Create database instance
db = SQLAlchemy(app)

# Create mail instance
mail = Mail(app)

# Create a table
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

# Create home page
@app.route("/", methods = ["GET","POST"])
def index():
    # Handle request
    if request.method == "POST":
        
        # Get form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]
        
        # Add data to database
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()
        
        # Prepare message
        message_body = f"""Thank you for your submission, {first_name}.
        Here are your data: 
        {first_name}
        {last_name}
        {date}
        Thank you!
        """
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        
        # Send email
        mail.send(message)
        
        # Show confirmation alert
        flash(f"{first_name}, your form was submitted successfully!", "success")
        
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=5001)