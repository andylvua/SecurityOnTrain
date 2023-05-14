from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TABLES = ['Train', 'Carriage', 'TrainCarriage', 'Station', 'Route', 'Ticket', 'Passenger',
          'PassengerTicket', 'Shift', 'SecurityPersonnel', 'ShiftPersonnel', 'Camera']


class Train(db.Model):
    __tablename__ = 'Train'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=True)
    type = db.Column(db.Enum('Freight', 'Passenger'), nullable=False)
    numOfCarriages = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=True, default=None)
    departureStationId = db.Column(db.Integer, db.ForeignKey('Station.id'), nullable=True, default=None)
    destinationStationId = db.Column(db.Integer, db.ForeignKey('Station.id'), nullable=True, default=None)

    columns = ['id', 'name', 'type', 'numOfCarriages', 'capacity', 'departureStationId', 'destinationStationId']
    enum_col_names = ['type']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Train {self.id} {self.name} {self.type} {self.numOfCarriages} {self.capacity}'


class Shift(db.Model):
    __tablename__ = 'Shift'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)

    columns = ['id', 'startTime', 'endTime']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Shift {self.id} {self.startTime} {self.endTime}'


class Station(db.Model):
    __tablename__ = 'Station'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    location = db.Column(db.String(45), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    columns = ['id', 'name', 'location', 'capacity']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Station {self.id} {self.name} {self.location} {self.capacity}'


class Carriage(db.Model):
    __tablename__ = 'Carriage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum('VIP', '1class', '2class', 'restaurant'), nullable=True)

    columns = ['id', 'capacity', 'type']
    enum_col_names = ['type']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Carriage {self.id} {self.capacity} {self.type}'


class Camera(db.Model):
    __tablename__ = 'Camera'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locationId = db.Column(db.Integer, nullable=True)
    locationType = db.Column(db.Enum('Carriage', 'Station'), nullable=False)
    status = db.Column(db.String(45), nullable=False)
    datastorage = db.Column(db.String(50), nullable=False)

    columns = ['id', 'locationId', 'locationType', 'status', 'datastorage']
    enum_col_names = ['locationType']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Camera {self.id} {self.locationId} {self.locationType} {self.status} {self.datastorage}'


class Passenger(db.Model):
    __tablename__ = 'Passenger'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    columns = ['id', 'firstname', 'surname', 'age']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Passenger {self.id} {self.firstname} {self.surname} {self.age}'


class Ticket(db.Model):
    __tablename__ = 'Ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTrain = db.Column(db.Integer, db.ForeignKey('Carriage.id'), nullable=False)
    idCarriage = db.Column(db.Integer, db.ForeignKey('TrainCarriage.id'), primary_key=True, nullable=False)
    seatNum = db.Column(db.Integer, nullable=False)
    departureStationId = db.Column(db.Integer, db.ForeignKey('Station.id'), nullable=False)
    destinationStationId = db.Column(db.Integer, db.ForeignKey('Station.id'), nullable=False)

    columns = ['id', 'idCarriage', 'idTrain', 'seatNum', 'departureStationId', 'destinationStationId']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Ticket {self.id} {self.idTrain} {self.idCarriage} {self.seatNum} {self.departureStationId} {self.destinationStationId}'


class SecurityPersonnel(db.Model):
    __tablename__ = 'SecurityPersonnel'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Enum('onStation', 'onTrain', 'Dispatcher'), nullable=False)
    locationId = db.Column(db.Integer, nullable=True)
    locationType = db.Column(db.Enum('Carriage', 'Station'), nullable=False)

    columns = ['id', 'firstname', 'surname', 'age', 'role', 'locationId', 'locationType']
    enum_col_names = ['role', 'locationType']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'SecurityPersonnel {self.id} {self.firstname} {self.surname} {self.age} {self.role} {self.locationId} {self.locationType}'


class Route(db.Model):
    __tablename__ = 'Route'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTrain = db.Column(db.Integer, db.ForeignKey('Train.id'), primary_key=True)
    idStation = db.Column(db.Integer, db.ForeignKey('Station.id'), primary_key=True)
    arrivalTime = db.Column(db.DateTime, nullable=False)
    departureTime = db.Column(db.DateTime, nullable=False)

    columns = ['id', 'idTrain', 'idStation', 'arrivalTime', 'departureTime']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'Route {self.id} {self.idTrain} {self.idStation} {self.arrivalTime} {self.departureTime}'


class ShiftPersonnel(db.Model):
    __tablename__ = 'ShiftPersonnel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idShift = db.Column(db.Integer, db.ForeignKey('Shift.id'), primary_key=True)
    idPersonnel = db.Column(db.Integer, db.ForeignKey('SecurityPersonnel.id'), primary_key=True)

    columns = ['id', 'idShift', 'idPersonnel']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'ShiftPersonnel {self.id} {self.idShift} {self.idPersonnel}'


class TrainCarriage(db.Model):
    __tablename__ = 'TrainCarriage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTrain = db.Column(db.Integer, db.ForeignKey('Train.id'), primary_key=True)
    idCarriage = db.Column(db.Integer, db.ForeignKey('Carriage.id'), primary_key=True)

    columns = ['id', 'idTrain', 'idCarriage']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'TrainCarriage {self.id} {self.idTrain} {self.idCarriage}'


class PassengerTicket(db.Model):
    __tablename__ = 'PassengerTicket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPassenger = db.Column(db.Integer, db.ForeignKey('Passenger.id'), primary_key=True)
    idTicket = db.Column(db.Integer, db.ForeignKey('Ticket.id'), primary_key=True)

    columns = ['id', 'idPassenger', 'idTicket']
    enum_col_names = ['']

    def __init__(self, lst):
        self.id = None
        for i in range(len(lst)):
            setattr(self, self.columns[i + 1], lst[i])

    def __repr__(self):
        return f'PassengerTicket {self.id} {self.idPassenger} {self.idTicket}'
