from pyramid import testing

import unittest
import mock
import json
import test.fixtures as factory
from test.mock_helpers import MockQuery
from test.mock_helpers import observable_side_effect
from src.views import observable, observable_locus_details, observable_locus_details_all, observable_ontology_graph


class ObservableTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @mock.patch('src.views.extract_id_request', return_value="APO:0000007")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_valid_observable(self, mock_search, mock_redis):
        mock_search.side_effect = observable_side_effect

        obs = factory.ApoFactory()
        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        request.matchdict['format_name'] = "APO:0000007"
        format_name = mock_redis.extract_id_request(request, 'observable', param_name='format_name')

        response = observable(request)
        self.assertEqual(response, obs.to_dict())

    @mock.patch('src.views.extract_id_request', return_value="169841")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_valid_observable_locus_details(self, mock_search, mock_redis):
        mock_search.side_effect = observable_side_effect

        obs = factory.ApoFactory()
        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')

        response = observable_locus_details(request)
        self.assertEqual(response, obs.annotations_to_dict())

    @mock.patch('src.views.extract_id_request', return_value="169841")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_valid_observable_locus_details_all(self, mock_search, mock_redis):
        mock_search.side_effect = observable_side_effect

        obs = factory.ApoFactory()
        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')

        response = observable_locus_details_all(request)
        self.assertEqual(response, obs.annotations_and_children_to_dict())

    @mock.patch('src.views.extract_id_request', return_value="169841")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_valid_observable_ontology_graph(self, mock_search, mock_redis):
        mock_search.side_effect = observable_side_effect

        obs = factory.ApoFactory()
        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')

        response = observable_ontology_graph(request)
        self.assertEqual(response, obs.ontology_graph())

    @mock.patch('src.views.extract_id_request', return_value="nonexistent_id")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_non_existent_observable(self, mock_search, mock_redis):
        mock_search.return_value = MockQuery(None)

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        request.matchdict['format_name'] = 'nonexistent_id'
        format_name = mock_redis.extract_id_request(request, 'observable', param_name='format_name')

        response = observable(request)
        self.assertEqual(response.status_code, 404)

    @mock.patch('src.views.extract_id_request', return_value="nonexistent_id")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_non_existent_observable_locus_details(self, mock_search, mock_redis):
        mock_search.return_value = MockQuery(None)

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')
        response = observable_locus_details(request)
        self.assertEqual(response.status_code, 404)

    @mock.patch('src.views.extract_id_request', return_value="nonexistent_id")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_non_existent_observable_locus_details_all(self, mock_search, mock_redis):
        mock_search.return_value = MockQuery(None)

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')
        response = observable_locus_details_all(request)
        self.assertEqual(response.status_code, 404)

    @mock.patch('src.views.extract_id_request', return_value="nonexistent_id")
    @mock.patch('src.models.DBSession.query')
    def test_should_return_non_existent_observable_ontology_graph(self, mock_search, mock_redis):
        mock_search.return_value = MockQuery(None)

        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        #request.matchdict['id'] = "169841"
        id = mock_redis.extract_id_request(request, 'observable', param_name='id')
        response = observable_ontology_graph(request)
        self.assertEqual(response.status_code, 404)
