from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, HiddenField, FloatField, DateTimeField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange


class AddTrainForm(FlaskForm):
    # id used only by update/edit
    id = HiddenField()
    name = StringField('Train name', [InputRequired(),
                                      Length(min=1, max=45, message="Invalid train name length")])
    type = SelectField('Train type', [InputRequired()],
                       choices=[('', ''), ('Freight', 'Freight'), ('Passenger', 'Passenger')])
    numOfCarriages = IntegerField('Number of carriages', [InputRequired(),
                                                          NumberRange(min=1, max=100,
                                                                      message="Invalid number of carriages")])
    capacity = IntegerField('Capacity', [NumberRange(min=1, max=999, message="Invalid capacity range")])
    departureStationId = IntegerField('Departure station id', [InputRequired()])
    destinationStationId = IntegerField('Destination station id', [InputRequired()])

    submit = SubmitField('Add/Update Train Record')


class AddShiftForm(FlaskForm):
    # id used only by update/edit
    id = HiddenField()

    startTime = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S',
                              validators=[InputRequired()],
                              render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})
    endTime = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S',
                            validators=[InputRequired()],
                            render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"})

    submit = SubmitField('Add/Update Shift Record')


class AddStationForm(FlaskForm):
    # id used only by update/edit
    id = HiddenField()

    name = StringField('Name', validators=[InputRequired(),
                                           Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid station name"),
                                           Length(min=3, max=45, message="Invalid station name length")])

    location = StringField('Location', validators=[InputRequired(),
                                                   Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid location"),
                                                   Length(min=3, max=45, message="Invalid location length")])

    capacity = IntegerField('Capacity', validators=[InputRequired(),
                                                    NumberRange(min=1, max=999, message="Invalid capacity range")])

    submit = SubmitField('Add/Update Station Record')


class AddCarriageForm(FlaskForm):
    # id used only by update/edit
    id = HiddenField()

    capacity = IntegerField('Capacity', [InputRequired(),
                                         NumberRange(min=1, max=999, message="Invalid capacity")])

    type = SelectField('Type', [InputRequired()],
                       choices=[('VIP', 'VIP'),
                                ('1class', '1st Class'),
                                ('2class', '2nd Class'),
                                ('restaurant', 'Restaurant')])

    submit = SubmitField('Add/Update Carriage Record')


class AddCameraForm(FlaskForm):
    # id used only by update/edit
    id = HiddenField()
    locationId = IntegerField('Location ID', [InputRequired()])
    locationType = SelectField('Location Type', [InputRequired()],
                               choices=[('Carriage', 'Carriage'), ('Station', 'Station')])
    status = StringField('Status', [InputRequired()])
    datastorage = StringField('Storage of Data', [InputRequired()])

    submit = SubmitField('Add/Update Camera')


class AddPassengerForm(FlaskForm):
    id = HiddenField()
    firstname = StringField('First Name', [InputRequired()])
    surname = StringField('Last Name', [InputRequired()])
    age = IntegerField('Age', [InputRequired(), NumberRange(min=0, max=150)])
    submit = SubmitField('Add/Update Passenger Record')


class AddTicketForm(FlaskForm):
    id = HiddenField()
    idTrain = IntegerField('Train ID', [InputRequired()])
    idCarriage = IntegerField('Carriage ID', [InputRequired()])
    seatNum = IntegerField('Seat Number', [InputRequired()])
    departureStationId = IntegerField('Departure Station ID', [InputRequired()])
    destinationStationId = IntegerField('Destination Station ID', [InputRequired()])

    submit = SubmitField('Add/Update Ticket Record')


class AddSecurityPersonnelForm(FlaskForm):
    id = HiddenField()
    firstname = StringField('First Name', [InputRequired(),
                                Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
                                Length(min=3, max=45, message="Invalid name length")
                                ])
    surname = StringField('Last Name', [InputRequired(),
                                Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
                                Length(min=3, max=45, message="Invalid name length")
                                ])
    age = IntegerField('Age', [InputRequired(),
                               NumberRange(min=18, max=99, message="Invalid age range")
                               ])
    role = SelectField('Role', [InputRequired()],
                       choices=[('', ''), ('onStation', 'On Station'),
                                ('onTrain', 'On Train'),
                                ('dispatcher', 'Dispatcher')])
    locationId = IntegerField('Location ID', [InputRequired(),
                                              NumberRange(min=1, max=999, message="Invalid ID range")])
    locationType = SelectField('Location Type', [InputRequired()],
                               choices=[('', ''), ('Carriage', 'Carriage'),
                                        ('Station', 'Station')])
    submit = SubmitField('Add/Update SecurityPersonnel Record')


class AddRouteForm(FlaskForm):
    id = HiddenField()
    idTrain = IntegerField('Train ID', [InputRequired()])
    idStation = IntegerField('Station ID', [InputRequired()])
    arrivalTime = DateTimeField('Arrival Time', [InputRequired()], format='%Y-%m-%d %H:%M:%S')
    departureTime = DateTimeField('Departure Time', [InputRequired()], format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Add/Update Route Record')


class AddShiftPersonnelForm(FlaskForm):
    id = HiddenField()
    idShift = IntegerField('Shift ID', [InputRequired(), NumberRange(min=1)])
    idPersonnel = IntegerField('Personnel ID', [InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Add/Update ShiftPersonnel Record')


class AddTrainCarriageForm(FlaskForm):
    id = HiddenField()
    idTrain = IntegerField('Train ID', [InputRequired(), NumberRange(min=1)])
    idCarriage = IntegerField('Carriage ID', [InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Add/Update TrainCarriage Record')


class AddPassengerTicketForm(FlaskForm):
    id = HiddenField()
    idPassenger = IntegerField('Passenger ID', [InputRequired(), NumberRange(min=1)])
    idTicket = IntegerField('Ticket ID', [InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Add/Update PassengerTicket Record')


# delete form
class DeleteForm(FlaskForm):
    id = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Delete This Record')