from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from .PoolManager import NoLanesAvaible, PoolManager, ReservationAlreadyInserted
from .SchemaValidator import ReservationSchema

poolManager = PoolManager()

class PoolController(Resource):
    def get(self, user_uuid, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError as e:
            print(e)
            return None, 404

        try:
            reserv = poolManager.get_reservation(user_uuid, date)
        except Exception as e:
            print(e)
            return None, 404

        if reserv is None: return None, 404
        reserv["date"] = date
        return {"reservations": [reserv]}, 200

    def post(self, user_uuid, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError as e:
            return None, 400

        try:
            reservation_data = ReservationSchema().load(request.json)
        except Exception as e:
            print(e)
            return None, 400
        try:
            reservations_inserted = poolManager.add_reservation(user_uuid, date, reservation_data)
        except ReservationAlreadyInserted as e:
            print(e)
            return None, 409
        except NoLanesAvaible as e:
            print(e)
            return None, 412
        except Exception as e:
            print(e)
            return None, 400
        return {"reservations": reservations_inserted}, 201

class PoolStatus(Resource):
    def get(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError as e:
            print(e)
            return None, 400

        reservs = poolManager.get_reservations(date)
        return {"reservations": reservs}, 200

class CleanDB(Resource):
    def get(self):
        if (len(request.args) != 0):
            return None, 400
        poolManager._clean()

    

