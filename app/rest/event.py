import datetime

from flask_restful import Resource, reqparse

from exceptions import AccessDeniedException, EventNotFoundException, SubjectNotFoundException
from service.api_token import get_user
from service.event import get_event_safe, create_event, get_all_events, delete_event_safe, get_current_event, \
    get_next_event
from service.subject import get_subject_safe
from rest import validation


class Event(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('api_token', required=True, type=validation.api_token())
    parser_get.add_argument('event_id', required=True, type=validation.int_value(0))

    parser_post = parser_get.copy()
    parser_post.remove_argument('event_id')
    parser_post.add_argument('start_time', required=True, type=validation.int_value(0, 1440))
    parser_post.add_argument('end_time', required=True, type=validation.int_value(0, 1440))
    parser_post.add_argument('weekday', required=True, type=validation.int_value(0, 6))
    parser_post.add_argument('subject_id', required=True, type=validation.int_value(0))

    parser_delete = parser_get.copy()

    def get(self):
        args = self.parser_get.parse_args()

        try:
            event = get_event_safe(
                get_user(args['api_token']),
                args['event_id']
            )
        except (EventNotFoundException, AccessDeniedException):
            return {'message': 'Event not found'}, 404

        return {'event': event.serialize}, 200

    def post(self):
        args = self.parser_post.parse_args()

        if int(args['start_time']) > int(args['end_time']):
            return {'message': 'Invalid start/end time'}, 400

        try:
            event = create_event(
                get_subject_safe(
                    get_user(args['api_token']),
                    args['subject_id']
                ),
                args['start_time'],
                args['end_time'],
                args['weekday']
            )
        except (AccessDeniedException, SubjectNotFoundException):
            return {'message': 'Subject not found'}, 404

        return {'message': 'Created', 'id': event.id}, 201

    def delete(self):
        args = self.parser_delete.parse_args()

        try:
            delete_event_safe(
                get_user(args['api_token']),
                args['event_id']
            )
        except (EventNotFoundException, AccessDeniedException):
            return {'message': 'Event not found'}, 404

        return {'message': 'Deleted'}, 200


class Events(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('api_token', required=True, type=validation.api_token())

    def get(self):
        args = self.parser_get.parse_args()

        events = [event.serialize
                  for event
                  in get_all_events(get_user(args['api_token']))]

        return {'events': events}, 200


class Now(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('api_token', required=True, type=validation.api_token())

    def get(self):
        args = self.parser_get.parse_args()

        current_event = get_current_event(get_user(args['api_token']))
        if current_event:
            current_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
            return {'event': current_event.serialize,
                    'time_left_min': current_event.end_time-current_time}, 200
        return {'event': None}, 200


class Next(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('api_token', required=True, type=validation.api_token())

    def get(self):
        args = self.parser_get.parse_args()

        next_event = get_next_event(get_user(args['api_token']))
        return {'event': next_event.serialize if next_event else None}, 200
