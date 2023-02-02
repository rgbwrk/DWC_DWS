from math import floor, ceil
from typing import Callable

from flask import redirect, render_template, request


def init_views(app, db_access: dict[str, Callable]):
    @app.route("/", methods=["GET", "POST"])
    def index(): # invoca la página index
        print('path',request.path) # esto es para debug, realmente no va
        page = int(request.args.get("page", 1))
    # request es el objeto que tiene todo lo del pedido realizado por el cliente
    # cuando refresco index el cliente hace 
        species_list = db_access["species_list"] # está invocando a la función species_list que está en models con un pagination 
        species = species_list(page=page)        # 10 elementos como máximo por página

        total_pages = ceil (species.total / 10)

        # Ordenamiento en python
        # def cmp(sp):
        #     return sp.name

        # species.sort(key=cmp, reverse=True)

        return render_template( # se lanza la página index con los parámetros species (las 10 de la página activa) y el listado de páginas de especies
            "index.html", species=species, pages=[i + 1 for i in range(total_pages)] # ver en models.py
        )

    @app.route("/species/<uid>", methods=["GET", "POST"])
    def list_species_surveys(uid: str):
        page = int(request.args.get("page", 1))

        species_surveys = db_access["species_surveys"]
        surveys = species_surveys(uid, page)
        total_pages = ceil(surveys.total / 10)

        species_read = db_access["species_read"]
        species = species_read(uid)

        if request.method == "POST": # el request tiene toda la información
            species_update = db_access["species_update"] # db_access está en los models.py
            print(f"{request.form=}") # estás para depurar, no va
            species_update( # se están asignando los valores en la base de datos
                uid=uid,
                taxa=request.form["taxa"],
                name=request.form["name"],
                genus=request.form["genus"],
            )
            return redirect("/")

        return render_template(
            "species.html",
            species=species,
            surveys=surveys,
            pages=[i + 1 for i in range(total_pages)],
        )

    @app.route("/species/<species_id>/surveys/<int:survey_id>/delete", methods=["GET"])
    def delete_species_survey(species_id: str, survey_id: int):
        survey_delete = db_access["survey_delete"]
        survey_delete(survey_id)

        # species_read = db_access["species_read"]
        # species = species_read(species_id)

        return redirect(f"/species/{species_id}")

        # return render_template("species_surveys.html", species=species)

    @app.route("/species/<uid>/delete", methods=["POST"])
    def species_delete(uid: int):
        if request.method == "POST":
            species_delete = db_access["species_delete"]
            species_delete(uid=uid)
            return redirect("/")
