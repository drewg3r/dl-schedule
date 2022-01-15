from flask_restful import Resource, reqparse

from exceptions import DuplicateSubjectNameException, SubjectNotFoundException, AccessDeniedException
from service.api_token import get_user
from service.subject import get_subjects, create_subject, search_subject, get_subject_safe, \
    delete_subject_safe, update_subject_safe

from rest import validation


class Subject(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('api_token', required=True, type=validation.api_token())
    parser_get.add_argument('id', required=True, type=validation.int_value(0))

    parser_post = parser_get.copy()
    parser_post.remove_argument('id')
    parser_post.add_argument('name', required=True, type=validation.str_length(2, 255))
    parser_post.add_argument('abbr', required=True, type=validation.str_length(1, 10))
    parser_post.add_argument('lecturer', required=True, type=validation.str_length(2, 255))
    parser_post.add_argument('link', required=True, type=validation.str_length(5, 1024))

    parser_delete = parser_get.copy()

    parser_put = parser_post.copy()
    parser_put.add_argument('id', required=True, type=validation.int_value(0))

    def get(self):
        args = self.parser_get.parse_args()

        try:
            subject = get_subject_safe(
                get_user(args['api_token']),
                args['id']
            ).serialize
        except (SubjectNotFoundException, AccessDeniedException):
            return {'message': 'Subject not found'}, 404

        return {'subject': subject}, 200

    def post(self):
        args = self.parser_post.parse_args()

        try:
            subject = create_subject(
                        args['name'],
                        args['abbr'],
                        args['lecturer'],
                        args['link'],
                        get_user(args['api_token'])
            )
        except DuplicateSubjectNameException:
            return {'message': 'Duplicated subject name'}, 400

        return {'message': 'Created', 'id': subject.id}, 200

    def delete(self):
        args = self.parser_delete.parse_args()

        try:
            delete_subject_safe(
                get_user(args['api_token']),
                args['id']
            )
            return {'message': 'Deleted'}, 200
        except (SubjectNotFoundException, AccessDeniedException):
            return {'message': 'Subject not found'}, 404

    def put(self):
        args = self.parser_put.parse_args()

        try:
            update_subject_safe(
                get_user(args['api_token']),
                args['id'],
                args['name'],
                args['abbr'],
                args['lecturer'],
                args['link']
            )
        except SubjectNotFoundException:
            # If subject was not found create new one
            try:
                subject = create_subject(
                    args['name'],
                    args['abbr'],
                    args['lecturer'],
                    args['link'],
                    get_user(args['api_token'])
                )
            except DuplicateSubjectNameException:
                return {'message': 'Duplicated subject name'}, 400
            return {'message': 'Created', 'id': subject.id}, 200
        except AccessDeniedException:
            return {'message': 'Subject not found'}, 404
        return {'message': 'Updated'}, 200


class Subjects(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('api_token', required=True, type=validation.api_token())

    def get(self):
        args = self.parser.parse_args()

        subjects = [subject.serialize
                    for subject
                    in get_subjects(get_user(args['api_token']))]

        return {'subjects': subjects}, 200


class Search(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('api_token', required=True, type=validation.api_token())
    parser.add_argument('name', required=True, type=validation.str_length(0, 255))

    def get(self):
        args = self.parser.parse_args()

        subjects = [subject.serialize
                    for subject
                    in search_subject(args['name'], get_user(args['api_token']))]

        return {'subjects': subjects}, 200
