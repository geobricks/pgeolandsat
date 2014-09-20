import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException
from pgeolandsat.core import landsat_core as m


landsat = Blueprint('landsat', __name__)


@landsat.route('/')
@cross_origin(origins='*')
def list_wrs_service():
    try:
        out = m.list_wrs()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@landsat.route('/<wrs>/')
@cross_origin(origins='*')
def list_paths_service(wrs):
    try:
        out = m.list_paths(wrs)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@landsat.route('/<wrs>/<path>/')
@cross_origin(origins='*')
def list_rows_service(wrs, path):
    try:
        out = m.list_rows(wrs, path)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@landsat.route('/<wrs>/<path>/<row>/')
@cross_origin(origins='*')
def list_dates_service(wrs, path, row):
    try:
        out = m.list_dates(wrs, path, row)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@landsat.route('/<wrs>/<path>/<row>/<date>')
@cross_origin(origins='*')
def list_layers_service(wrs, path, row, date):
    try:
        out = m.list_layers(wrs, path, row, date)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())