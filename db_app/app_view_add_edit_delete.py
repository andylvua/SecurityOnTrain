""" write to a SQLite database with forms, templates
    add new record, delete a record, edit/update a record
    """

from flask import Flask, render_template, request, flash, abort, redirect
from flask_bootstrap import Bootstrap5
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
    return render_template('index.html', form=form)


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
