from typing import Callable

from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import desc


def init_db(app) -> dict[str, Callable]:
    db = SQLAlchemy(app)
    
    # se declara una clase por cada tabla de la BD
    class Plot(db.Model):
        __tablename__ = "plots"

        uid = db.Column("plot_id", db.BigInteger, primary_key=True)
        plot_type = db.Column("plot_type", db.Text)
        surveys = db.relationship("Survey", backref="plot", lazy=True)

    class Species(db.Model):
        __tablename__ = "species"

        uid = db.Column("species_id", db.String, primary_key=True)
        genus = db.Column("genus", db.String)
        name = db.Column("species", db.String)
        taxa = db.Column("taxa", db.String)
        surveys = db.relationship("Survey", backref="species", lazy=True)

    class Survey(db.Model):
        __tablename__ = "surveys"

        uid = db.Column("record_id", db.BigInteger, primary_key=True)
        day = db.Column("day", db.BigInteger)
        month = db.Column("month", db.BigInteger)
        year = db.Column("year", db.BigInteger)
        plot_id = db.Column(db.BigInteger, db.ForeignKey("plots.plot_id"))
        species_id = db.Column(db.String, db.ForeignKey("species.species_id"))
        sex = db.Column("sex", db.String)
        hindfoot_length = db.Column("hindfoot_length", db.Float)
        weight = db.Column("weight", db.Float)

    # las funciones que operan sobres los datos, al final se retornan de la función init_db para poder usarlos fuera de ella
    def species_list(page: int = 1) -> list[Species]: # se pasa como parámetro la página, por defecto es página 1
        # Ordenamiento en el motor de base de datos
        species_list = Species.query.order_by(Species.name).paginate(
            page=page, max_per_page=10 # divide en páginas de 10 elementos y devuelve solamente los 10 (o menos si es la última)
        )  # Ordenamiento Ascendente   # del número de página que se ha pasado como parámetro 
        print(f"{species_list=}") # esto es para debug, no va
        # species_list = Species.query.order_by(desc(Species.name)).all()   # Ordenamiento Descendente

        # return [sp for sp in species_list]
        return species_list

    def species_read(uid: str) -> Species:
        return Species.query.get(uid)

    def species_surveys(uid: str, page: int = 1):
        return Survey.query.filter_by(species_id=uid).paginate(
            page=page, max_per_page=10
        )
    # esta función void es la que hace el update sobre la base de datos
    def species_update(uid: int, taxa: str, name: str, genus: str):
        species = Species.query.get(uid)
        species.taxa = taxa
        species.name = name
        species.genus = genus
        db.session.commit()

    def species_delete(uid: str):
        species = Species.query.get(uid)
        db.session.delete(species)
        db.session.commit()

    def survey_delete(uid: int):
        survey = Survey.query.get(uid)
        db.session.delete(survey)
        db.session.commit()

    db.create_all()

    return { # aquí se publican las funciones internas de init_db, para poder llamarlas desde 
             # fuera de init_db
        "species_list": species_list,
        "species_read": species_read,
        "species_surveys": species_surveys,
        "species_update": species_update,
        "species_delete": species_delete,
        "survey_delete": survey_delete,
    }
