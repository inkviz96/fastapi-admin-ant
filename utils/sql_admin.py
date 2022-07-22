from database.database_connection import session
from sqlalchemy.orm import Session
from string import Template

# Create a template that has placeholder for value of x
model_objects = Template("SELECT * FROM $table_name;")
model_fields = Template("SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name='$table_name';")
all_models = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
one_object = Template("SELECT * FROM $table_name WHERE id='$id';")
update = Template("UPDATE $table_name SET $query WHERE id='$id';")


def get_all():
    db: Session = session
    models = db.execute(all_models)
    return models.all().pop(-1)


def get_all_objects(table_name):
    db: Session = session
    objects = db.execute(model_objects.safe_substitute(table_name=table_name))
    return objects.all()


def get_model_fields(table_name):
    db: Session = session
    fields = db.execute(model_fields.safe_substitute(table_name=table_name))
    return fields.all()


def get_object(table_name, id):
    db: Session = session
    obj = db.execute(one_object.safe_substitute(table_name=table_name, id=id))
    return obj.all()

def update_obj(table_name, id, query, **kwargs):
    db: Session = session

    obj = db.execute(update.safe_substitute(table_name=table_name, id=id, query=query))
    return obj.all()