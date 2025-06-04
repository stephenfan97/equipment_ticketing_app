from flask import Flask, render_template, request, redirect, url_for
from models import db, Equipment, Ticket, Booking
from forms import TicketForm, BookingForm
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    form = TicketForm()
    form.equipment_id.choices = [(e.id, e.name) for e in Equipment.query.all()]
    if form.validate_on_submit():
        ticket = Ticket(
            equipment_id=form.equipment_id.data,
            description=form.description.data
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('view_tickets'))
    return render_template('submit_ticket.html', form=form)

@app.route('/view_tickets')
def view_tickets():
    tickets = Ticket.query.all()
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    form = BookingForm()
    form.equipment_id.choices = [(e.id, e.name) for e in Equipment.query.all()]
    if form.validate_on_submit():
        conflict = Booking.query.filter(
            Booking.equipment_id == form.equipment_id.data,
            Booking.start_time < form.end_time.data,
            Booking.end_time > form.start_time.data
        ).first()
        if conflict:
            return "Time slot already booked!", 409
        booking = Booking(
            equipment_id=form.equipment_id.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('scheduler'))
    bookings = Booking.query.all()
    return render_template('scheduler.html', form=form, bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)