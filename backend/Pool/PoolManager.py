from uuid import UUID
from google.cloud import firestore
from .utils import delete_collection


LANE_NUMBER_ORDER = [4,5,3,6,2,7,1,8]

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

class ReservationAlreadyInserted(Exception):
    def __init__(self):
        super().__init__("Reservation already inserted")

class NoLanesAvaible(Exception):
    def __init__(self):
        super().__init__("No lines are avaible for that date and time")

class PoolManager(object):
    def __init__(self):
        self.db = firestore.Client()
        self.reservation_ref = self.db.collection('reservations')
        self.corsia_ref = self.db.collection('corsia')

    def _clean(self):
        delete_collection(self.reservation_ref, 5)
        delete_collection(self.corsia_ref, 5)

    def get_next_free_lane(self, date, time):
        reservs = self.reservation_ref.where("date", "==", date) \
                .where("time", "==", time).get()

        n = len(reservs)
        if n >= 16: return None
        return LANE_NUMBER_ORDER[n%8]


    def get_reservation(self, user_uuid, date):
        if not is_valid_uuid(user_uuid): raise ValueError
        reservation = self.reservation_ref.where("user_uuid", "==", user_uuid) \
                .where("date", "==", date).get()
        print(reservation)
        if reservation is None: raise Exception
        if len(reservation) > 1: raise Exception
        if len(reservation) == 0: return None

        reservation = reservation[0].to_dict()
        del reservation["user_uuid"]
        del reservation["date"]
        return reservation    

    def add_reservation(self, user_uuid, date, reservation_data):
        if not is_valid_uuid(user_uuid): raise ValueError

        reservation = self.get_reservation(user_uuid, date)
        time = reservation_data["time"]
        lane = self.get_next_free_lane(date, time)

        if reservation is not None: raise ReservationAlreadyInserted
        if lane is None: raise NoLanesAvaible

        if "others" not in reservation_data:
            reservation_data["others"] = []

        for reserv in reservation_data["others"]:
            reservation = self.get_reservation(user_uuid, date)
            time = reservation_data["time"]
            lane = self.get_next_free_lane(date, time)
            if reservation is not None: raise ReservationAlreadyInserted
            if lane is None: raise NoLanesAvaible

        reservations_done = []
        self.reservation_ref.document().set({ \
                "user_uuid": user_uuid, \
                "date": date, \
                "time": time, \
                "lane": lane \
                })

        reservations_done.append({"date": date, "time": time, "lane": lane})

        for reserv in reservation_data["others"]:
            date = reserv["date"]
            time = reserv["time"]
            lane = self.get_next_free_lane(date, time)
            self.reservation_ref.document().set({ \
                    "user_uuid": user_uuid, \
                    "date": reserv["date"], \
                    "time": reserv["time"], \
                    "lane": lane, \
                    })
            reservations_done.append({"date": reserv["date"],\
                    "time": reserv["time"], \
                    "lane": lane \
                    })
        return reservations_done

    def get_reservations(self, date):
        reservs = self.reservation_ref.where("date", "==", date).get()
        return [ r.to_dict() for r in reservs ]

