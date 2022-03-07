from collections import namedtuple

import pytest

from models import User, Subject
from service.subject import get_subjects, create_subject, get_subject


class TestSubject:
    subject = namedtuple('Subject', ['name', 'abbr', 'lecturer', 'link'])
    test_subjects = [
        subject('Algebra', 'ALG', 'A. J. Brown', 'https://algebra.com'),
        subject('Chemistry', 'CHM', 'Peter Taylor', 'https://chemistry.com'),
        subject('History', 'HST', 'Omar Harvey', 'https://history.com')
    ]
    test_subjects_ids = []

    def test_get_subject_empty(self, client, temp_db):
        assert get_subject(0) is None

    def test_get_subjects_empty(self, client, temp_db, test_user):
        assert get_subjects(test_user) == []

    @pytest.mark.parametrize('name, abbr, lecturer, link', test_subjects)
    def test_create_subject(self, client, temp_db, test_user, name, abbr, lecturer, link):
        subject = create_subject(name, abbr, lecturer, link, test_user)
        assert isinstance(subject.id, int)
        self.test_subjects_ids.append(subject.id)

    # def test_get_subject(self, client, temp_db, subject_id):
    #     assert get_subject(subject_id).name in [s.name for s in self.test_subjects]

    @pytest.mark.parametrize('subject_name', [s.name for s in test_subjects])
    def test_get_subjects(self, client, temp_db, test_user, subject_name):
        assert subject_name in [s.name for s in test_user.subjects]
