from flask import jsonify, Blueprint, request

trips_routes_bp = Blueprint("trip_routes", __name__)

from src.controllers.trip_creators import TripCreator
from src.controllers.trip_finder import TripFinder
from src.controllers.trip_confirmer import TripConfirmer
from src.controllers.link_creator import LinkCreator
from src.controllers.link_finder import LinkFinder
from src.controllers.participants_creator import ParticipantsCreator
from src.controllers.activity_creator import ActivityCreator
from src.controllers.participants_finder import ParticipantFinder
from src.controllers.activity_finder import ActivityFinder
from src.controllers.participants_confirmer import ParticipantConfirmer

from src.models.repositories.trips_repository import TripsRepository
from src.models.repositories.emails_to_invite_repository import EmailsToInviteRepository
from src.models.repositories.links_repository import LinksRepository
from src.models.repositories.participants_repository import ParticipantsRepository
from src.models.repositories.activity_repository import ActivityRepository

from src.models.settings.db_connection_handler import db_connection_handler


@trips_routes_bp.route("/trips", methods = ["POST"])

def create_trip():
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)
    emails_repository = EmailsToInviteRepository(conn)
    controller = TripCreator(trips_repository, emails_repository)

    response = controller.create(request.json)

    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>", methods = ["GET"])
def find_trip(tripId):
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)
    controller = TripFinder(trips_repository)

    response = controller.find_trip_details(tripId)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/confirm", methods = ["GET"])

def confirm_trip(tripId):
    conn = db_connection_handler.get_connection()
    trips_repository = TripsRepository(conn)
    controller = TripConfirmer(trips_repository)
    response = controller.confirm(tripId)

    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/confirm", methods = ["POST"])
def create_trip_link(trip_id):
    conn = db_connection_handler.get_connection()
    links_repository = LinksRepository(conn)
    controller = LinkCreator(links_repository)

    response = controller.create(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/links", methods = ["GET"])
def find_trip_link(trip_id):
    conn = db_connection_handler.get_connection()
    links_repository = LinksRepository(conn)
    controller = LinkFinder(links_repository)

    response = controller.find(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/invites", methods = ["POST"])
def invite_to_trip(trip_id):
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)
    emails_repository = EmailsToInviteRepository(conn)
    controller = ParticipantsCreator(participants_repository, emails_repository)

    response = controller.create(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/activities", methods = ["POST"])
def create_activity(trip_id):
    conn = db_connection_handler.get_connection()
    activity_repository = ActivityRepository(conn)
    controller = ActivityCreator(activity_repository)

    response = controller.create(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/participants", methods = ["GET"])
def get_trip_participants(trip_id):
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)
    controller = ParticipantFinder(participants_repository)

    response = controller.find_participants_from_trip(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/trips/<tripId>/activities", methods = ["GET"])
def get_trip_activities(trip_id):
    conn = db_connection_handler.get_connection()
    activity_repository = ActivityRepository(conn)
    controller = ActivityFinder(activity_repository)

    response = controller.find_from_trip(request.json, trip_id)
    return jsonify(response["body"]), response["status_code"]

@trips_routes_bp.route("/participants/<participantsId>/confirm", methods = ["PATH"])
def confirm_participants(participantsId):
    conn = db_connection_handler.get_connection()
    participants_repository = ParticipantsRepository(conn)
    controller = ParticipantConfirmer(participants_repository)
    response = controller.confirm(participantsId)

    return jsonify(response["body"]), response["status_code"]
