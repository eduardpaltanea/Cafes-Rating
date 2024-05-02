from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired()])
    opening_time = StringField("Opening time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField("Closing time e.g. 5:30PM", validators=[DataRequired()])
    rating = SelectField("Coffe Rating", choices=["❌","☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi = SelectField("Wifi Strength Rating", choices=["❌", "💪🏼", "💪🏼💪🏼", "💪🏼💪🏼💪🏼", "💪🏼💪🏼💪🏼💪🏼", "💪🏼💪🏼💪🏼💪🏼💪🏼"], validators=[DataRequired()])
    socket = SelectField("Power Socket Availability", choices=["❌", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline="", encoding="utf-8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},{form.location.data},{form.opening_time.data},{form.closing_time.data},{form.rating.data},{form.wifi.data},{form.socket.data}")
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
