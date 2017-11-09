import unittest

from kanapy.api import APIClient
from kanapy.resources import deserialize, Resource

class ClassA(Resource):
    resource_type = 'ClassA'
    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.id, self.name = id, name


class ClassB(Resource):
    resource_type = 'ClassB'
    def __init__(self, role=None, classA=None, **kwargs):
        super().__init__(**kwargs)
        self.id, self.role, self.classA = id, role, classA


class ClassC(Resource):
    resource_type = 'ClassC'
    def __init__(self, role=None, not_defined=None, classAs=None, **kwargs):
        super().__init__(**kwargs)
        self.id, self.role, self.classAs = id, role, classAs
        self.not_defined = not_defined


class TestAPIClient(unittest.TestCase):

    def test_session_always_set(self):
        c = APIClient("testDomain", "testUser", "testPass")
        self.assertIsNotNone(c._session)

    def test_session_always_set_without_init(self):
        c = APIClient()
        self.assertIsNotNone(c._session)


class TestDeserialize(unittest.TestCase):

    def test_handles_base_case(self):
        json_obj = {
            "id": 42,
            "name": "The answer to life, universe and everything",
            "resource_type": "ClassA",
        }
        expected = ClassA(id=json_obj["id"], name=json_obj["name"])
        actual = deserialize(json_obj, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.name, actual.name)

    def test_handles_nested_objects(self):
        json_obj = {
            "id": 42,
            "role": "Super Sayian",
            "resource_type": "ClassB",
            "classA": {
                "id": 42,
                "name": "The answer to life, universe and everything",
                "resource_type": "ClassA",
            },
        }
        classA = ClassA(id=json_obj["classA"]["id"], name=json_obj["classA"]["name"])
        expected = ClassB(id=json_obj["id"], role=json_obj["role"], classA=classA)
        actual = deserialize(json_obj, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.role, actual.role)
        self.assertEqual(expected.classA.id, actual.classA.id)

    def test_handles_nested_objects_and_arrays(self):
        json_obj = {
            "id": 42,
            "role": "Super Sayian",
            "resource_type": "ClassC",
            "classAs": [
                {
                    "id": 42,
                    "name": "The answer to life, universe and everything",
                    "resource_type": "ClassA",
                },
                {
                    "id": 41,
                    "name": "Not the answer to life, universe and everything",
                    "resource_type": "ClassA",
                },
            ],
            "not_defined": {
                "id": "lol",
                "resource_type": "nodef",
            },
        }
        classA1 = ClassA(id=json_obj["classAs"][0]["id"], name=json_obj["classAs"][0]["name"])
        classA2 = ClassA(id=json_obj["classAs"][1]["id"], name=json_obj["classAs"][1]["name"])
        expected = ClassC(id=json_obj["id"], role=json_obj["role"], classAs=[classA1, classA2])
        actual = deserialize(json_obj, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.classAs[0].id, actual.classAs[0].id)
        self.assertEqual(expected.classAs[1].id, actual.classAs[1].id)

