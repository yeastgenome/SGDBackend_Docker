from pyramid import testing

import unittest
import mock
import json
import test.fixtures as factory
from test.mock_helpers import MockQuery
from test.mock_helpers import author_side_effect
from src.views import author


class ReferenceauthorTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    @mock.patch('src.views.extract_id_request', return_value = b"Ninzima_S")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_valid_author_name(self, mock_search, mock_redis):

        mock_search.side_effect = author_side_effect
        source = factory.SourceFactory()
        journal = factory.JournalFactory()
        book = factory.BookFactory()
        refdb = factory.ReferencedbentityFactory()
        refdb.journal = journal

        a_name = factory.ReferenceauthorFactory()
        a_name.reference = refdb

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['format_name'] = "Ninzima_S"
        id = mock_redis.extract_id_request(request, 'author', param_name='id')

        response = author(request)
        self.assertEqual(response, {'references': [{'display_name': 'My entity', 'urls': [{'link': 'obj url', 'display_name': 'ref url'}], 'pubmed_id': 1, 'year': 2016, 'link': 'http://example.org/entity', 'abstract': {'text': '<'}, 'citation': 1, 'id': 1, 'reftypes': [{'display_name': 'd'}]}], 'display_name': 'Ninzima_S'})

    @mock.patch('src.views.extract_id_request', return_value=b"nonexistent_id")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_non_existent_author_name(self, mock_search, mock_redis):
        mock_search.return_value = MockQuery(None)

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['format_name'] = 'nonexistent_id'
        id = mock_redis.extract_id_request(request, 'author', param_name='id')
        print('*'*20)
        print(request)
        response = author(request)
        self.assertEqual(response.status_code, 404)