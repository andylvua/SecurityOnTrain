""" write to a SQLite database with forms, templates
    add new record, delete a record, edit/update a record
    """

from flask import Flask, render_template, request, flash, abort, redirect
from flask_bootstrap import Bootstrap5
from sqlalchemy import select
from sqlalchemy.orm import query
from wtforms.validators import DataRequired

from db_tables import *
from table_add_forms import *

app = Flask(__name__)
# fill credentials for database connection
username = 'root'
password = 'Nastia!136850'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'

server = '127.0.0.1'
dbname = '/securityonatrain'

# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'sOmebiGseCretstrIng'

# initialize the app with Flask-SQLAlchemy
db.init_app(app)
# Flask-Bootstrap requires this line
bootstrap = Bootstrap5(app)


# form to select a table to work with
# on the index page
class TableSelect(FlaskForm):
    select = SelectField('Choose a table you want to explore:',
                         choices=TABLES)
    submit = SubmitField('Submit')


@app.route('/')
def index():
    form = TableSelect()
    return render_template('index_with_report.html', form=form)


@app.route('/table', methods=['GET'])
def get_table():
    name = request.args.get('select')
    return redirect('/table/' + name)


@app.route('/table/<name>', methods=['GET'])
def get_table_with_name(name):
    table_class = globals()[name]
    try:
        content = db.session.execute(db.select(table_class)).scalars()
        return render_template('list.html', name=name, items=content, columns=table_class.columns)
    except Exception as e:
        return render_template('error.html', pagetitle="Error from database",
                               pageheading="Error while reading from database", error=str(e)), 500


@app.route('/add_item/<name>', methods=['GET', 'POST'])
def add_item(name):
    table_class = globals()[name]
    form_class = globals()['Add' + name + 'Form']
    add_form = form_class()

    if add_form.validate_on_submit():
        values = []
        for i in range(1, len(table_class.columns)):
            values.append(getattr(add_form, table_class.columns[i]).data)

        record = table_class(values)
        db.session.add(record)
        try:
            db.session.commit()
        except Exception as e:
            return render_template('error.html', pagetitle="Error from database",
                                   pageheading="Error while writing in database", error=str(e)), 500

        message = f"New item has been added to the {name} table."
        return render_template('add_record.html', message=message, name=name)
    else:
        for field, errors in add_form.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(add_form, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form=add_form, name=name, columns=table_class.columns)


@app.route('/select_record/<name>')
def select_item(name):
    table_class = globals()[name]
    content = db.session.execute(db.select(table_class)).scalars()
    return render_template('select_record.html', items=content, name=name, columns=table_class.columns)


@app.route('/edit_or_delete/<name>', methods=['POST'])
def edit_or_delete(name):
    table_class = globals()[name]
    id_val = request.form['id']
    choice = request.form['choice']
    chosen_item = table_class.query.filter(table_class.id == id_val).first()
    # two forms in this template
    form1 = globals()['Add' + name + 'Form']()
    form2 = DeleteForm()
    return render_template('edit_or_delete.html', item=chosen_item, form1=form1, form2=form2, choice=choice, name=name,
                           columns=table_class.columns[1:], select_col_names=table_class.enum_col_names)


# result of delete - this function deletes the record
@app.route('/delete_result/<name>', methods=['POST'])
def delete_result(name):
    table_class = globals()[name]
    id_val = request.form['id']
    purpose = request.form['purpose']
    chosen_item = table_class.query.filter(table_class.id == id_val).first()
    if purpose == 'delete':
        try:
            db.session.delete(chosen_item)
            db.session.commit()
        except Exception as e:
            return render_template('error.html', pagetitle="Error from database",
                                   pageheading="Error while deleting from database", error=str(e)), 500
        message = f"The record with id {id_val} has been deleted from the {name} table."
        return render_template('result.html', message=message, name=name)
    else:
        abort(405)


# result of edit - this function updates the record
@app.route('/edit_result/<name>', methods=['POST'])
def edit_result(name):
    table_class = globals()[name]
    id_val = request.form['id']

    chosen_item = table_class.query.filter(table_class.id == id_val).first()
    for i in range(1, len(table_class.columns)):
        setattr(chosen_item, table_class.columns[i], request.form[table_class.columns[i]])

    form1 = globals()['Add' + name + 'Form'](obj=chosen_item)
    if form1.validate_on_submit():
        try:
            db.session.commit()
        except Exception as e:
            return render_template('error.html', pagetitle="Error from database",
                                   pageheading="Error while writing in database", error=str(e)), 500

        message = f"The record with id {id_val} has been updated in the {name} table."
        return render_template('result.html', message=message, name=name)
    else:
        chosen_item.id = id_val
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, item=chosen_item, choice='edit', name=name,
                               columns=table_class.columns[1:])


# --------------------- reports ---------------------
class PersonnelShiftInLocation(FlaskForm):
    personnel = IntegerField('Personnel ID', validators=[InputRequired(), NumberRange(min=1)])
    shift = IntegerField('Shift ID', validators=[InputRequired(), NumberRange(min=1)])

    submit = SubmitField('Find Personnel')


class PassengerByCamera(FlaskForm):
    camera = IntegerField('Camera ID', validators=[InputRequired(), NumberRange(min=1)])
    seatNum = IntegerField('Seat Number', validators=[InputRequired(), NumberRange(min=1)])

    submit = SubmitField('Get Passenger')


def handleLocationFormInput(personnel_id, shift_id):
    personnel = SecurityPersonnel.query.filter(SecurityPersonnel.id == personnel_id).first()
    shift = Shift.query.filter(Shift.id == shift_id).first()
    if personnel is None:
        location_result = f"Personnel with id {int(personnel_id)} does not exist."
        return location_result, None, None
    if shift is None:
        location_result = f"Shift with id {int(shift_id)} does not exist."
        return location_result, None, None
    if ShiftPersonnel.query.filter(ShiftPersonnel.idPersonnel == personnel_id,
                                   ShiftPersonnel.idShift == shift_id).first() is None:
        location_message = f"Personnel with id {personnel_id} is not assigned to shift with id {shift_id}."
        return location_message, None, None

    mates = ShiftPersonnel.query.filter(ShiftPersonnel.idShift == shift_id).all()
    shift_mates = []
    same_location = []
    for mate in mates:
        mate_values = SecurityPersonnel.query.filter(SecurityPersonnel.id == mate.idPersonnel).first()
        shift_mates.append(mate_values)
        if mate_values.id != personnel_id and mate_values.locationId == personnel.locationId and \
                mate_values.locationType == personnel.locationType:
            same_location.append(mate_values)

    location_message = "Result:"
    return location_message, shift_mates, same_location


def getCoveragePercentage():
    stations = Station.query.with_entities(Station.id).all()
    for i in range(len(stations)):
        stations[i] = (stations[i][0], 'Station')
    carriages = Carriage.query.with_entities(Carriage.id).all()
    for i in range(len(carriages)):
        carriages[i] = (carriages[i][0], 'Carriage')
    locations = stations + carriages
    locations = set(locations)

    sp = SecurityPersonnel.query.with_entities(SecurityPersonnel.locationId, SecurityPersonnel.locationType)
    camera = Camera.query.with_entities(Camera.locationId, Camera.locationType)
    result = sp.union(camera).all()
    result = set(result)
    covered_places = result.intersection(locations)
    percentage = len(covered_places) / len(locations) * 100

    sp_locations = set(SecurityPersonnel.query.with_entities(SecurityPersonnel.locationId, SecurityPersonnel.locationType).all())
    camera_locations = set(Camera.query.with_entities(Camera.locationId, Camera.locationType).all())
    camera_percentage = len(camera_locations) / len(locations) * 100
    sp_percentage = len(sp_locations) / len(locations) * 100

    uncovered_places = locations - covered_places

    return round(percentage, 2), round(sp_percentage, 2), round(camera_percentage, 2), uncovered_places


def getPassengersOnTrain():
    onboard = Ticket.query.with_entities(Ticket.idTrain).all()
    train_ids = Train.query.with_entities(Train.id).all()
    train_passnum = []
    for train in train_ids:
        train_passnum.append((train[0], onboard.count(train)))
    return train_passnum


def getPassengerFromCamera(camera_id, seat_num):
    camera = Camera.query.filter(Camera.id == camera_id).first()
    print(camera)
    if camera.locationType == 'Station':
        return f"Camera with id {camera_id} is not inside a carriage.", None, None
    carriage_id = camera.locationId
    ticket = Ticket.query.filter(Ticket.idCarriage == carriage_id, Ticket.seatNum == seat_num).first()
    if ticket is None:
        return f"There is no ticket with seat number {seat_num} in carriage with requested camara.", None, None
    ticket_passenger = PassengerTicket.query.filter(PassengerTicket.idTicket == ticket.id).first()
    if ticket_passenger is None:
        return f"There is no passenger assigned to ticket with seat number {seat_num} in carriage with requested camara.", None, None
    passenger = Passenger.query.filter(Passenger.id == ticket_passenger.idPassenger).first()

    security_personnel = SecurityPersonnel.query.filter(SecurityPersonnel.locationId == carriage_id,
                                                        SecurityPersonnel.locationType == 'Carriage').first()
    if security_personnel is None:
        return "Passenger found:", passenger, None

    return "Passenger found:", passenger, security_personnel



@app.route('/report', methods=['GET', 'POST'])
def report():
    location_message, shift_mates, same_location = None, None, None
    message, found_passenger, found_sp = None, None, None
    percentage, sp_percentage, cam_percentage, uncovered_places = getCoveragePercentage()
    train_pass_num = getPassengersOnTrain()

    personnel_location_form = PersonnelShiftInLocation()
    personnel_id = personnel_location_form.personnel.data
    shift_id = personnel_location_form.shift.data
    if personnel_id and shift_id:
        location_message, shift_mates, same_location = handleLocationFormInput(personnel_id, shift_id)

    cam_passenger_form = PassengerByCamera()
    camera_id = cam_passenger_form.camera.data
    seat_num = cam_passenger_form.seatNum.data
    if camera_id and seat_num:
        message, found_passenger,found_sp = getPassengerFromCamera(camera_id, seat_num)

    return render_template('reports.html', location_form=personnel_location_form, location_form_result=location_message,
                           shift_mates=shift_mates, same_location=same_location, personnel_columns=SecurityPersonnel.columns,
                           # cover percentage
                           percentage=percentage, sp_percentage=sp_percentage, cam_percentage=cam_percentage,
                           uncovered_places=uncovered_places, passengers_per_train=train_pass_num,
                           # passenger by camera
                           cam_passenger_form=cam_passenger_form, cam_passenger_form_result=message,
                           found_passenger=found_passenger, passenger_columns=Passenger.columns, found_sp=found_sp)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', pagetitle="404 Error - Page Not Found",
                           pageheading="Page not found (Error 404)", error=e), 404


@app.errorhandler(405)
def form_not_posted(e):
    return render_template('error.html', pagetitle="405 Error - Form Not Submitted",
                           pageheading="The form was not submitted (Error 405)", error=e), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', pagetitle="500 Error - Internal Server Error",
                           pageheading="Internal server error (500)", error=e), 500



if __name__ == '__main__':
    app.run(debug=True)
