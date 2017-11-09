import unittest

from kanapy.api import APIClient
from kanapy.resources import deserialize, Resource

class TestAPIClient(unittest.TestCase):

    def test_session_always_set(self):
        c = APIClient("testDomain", "testUser", "testPass")
        self.assertIsNotNone(c._session)

    def test_session_always_set_without_init(self):
        c = APIClient()
        self.assertIsNotNone(c._session)


class ClassA(Resource):
    resource_type = 'ClassA'
    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class ClassB(Resource):
    resource_type = 'ClassB'
    def __init__(self, role=None, classA=None, **kwargs):
        super().__init__(**kwargs)
        self.role, self.classA = role, classA


class ClassC(Resource):
    resource_type = 'ClassC'
    def __init__(self, role=None, not_defined=None, classAs=None, **kwargs):
        super().__init__(**kwargs)
        self.role, self.classAs = role, classAs
        self.not_defined = not_defined

json_classA = {
    "id": 42,
    "name": "The answer to life, universe and everything",
    "resource_type": "ClassA",
    'created_at': None,
    'updated_at': None,
    'resource_url': None,
}

json_classB = {
    "id": 42,
    "role": "Super Sayian",
    "resource_type": "ClassB",
    "classA": json_classA,
    'created_at': None,
    'updated_at': None,
    'resource_url': None,
}

json_classC = {
    "id": 42,
    "role": "Super Sayian",
    "resource_type": "ClassC",
    "classAs": [
        json_classA,
        {
            "id": 41,
            "name": "Not the answer to life, universe and everything",
            "resource_type": "ClassA",
            'created_at': None,
            'updated_at': None,
            'resource_url': None,
        },
    ],
    "not_defined": {
        "id": "lol",
        "resource_type": "nodef",
    },
    'created_at': None,
    'updated_at': None,
    'resource_url': None,
}

class TestDeserialize(unittest.TestCase):

    def test_handles_base_case(self):
        expected = ClassA(id=json_classA["id"], name=json_classA["name"])
        actual = deserialize(json_classA, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.name, actual.name)

    def test_handles_nested_objects(self):
        classA = ClassA(id=json_classB["classA"]["id"], name=json_classB["classA"]["name"])
        expected = ClassB(id=json_classB["id"], role=json_classB["role"], classA=classA)
        actual = deserialize(json_classB, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.role, actual.role)
        self.assertEqual(expected.classA.id, actual.classA.id)

    def test_handles_nested_objects_and_arrays(self):
        classA1 = ClassA(id=json_classC["classAs"][0]["id"], name=json_classC["classAs"][0]["name"])
        classA2 = ClassA(id=json_classC["classAs"][1]["id"], name=json_classC["classAs"][1]["name"])
        expected = ClassC(id=json_classC["id"], role=json_classC["role"], classAs=[classA1, classA2])
        actual = deserialize(json_classC, module_source=__name__)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.classAs[0].id, actual.classAs[0].id)
        self.assertEqual(expected.classAs[1].id, actual.classAs[1].id)
        self.assertNotEqual('dict', type(actual.not_defined))


class ResourceSerialize(unittest.TestCase):

    def test_serialize_on_base_case(self):
        classA = ClassA(**json_classA)
        expected = json_classA
        actual = classA.serializeable()
        self.assertEqual(sorted(expected), sorted(actual))
        for t1, t2 in zip(sorted(expected.items()), sorted(actual.items())):
            self.assertEqual(t1, t2)

    def test_serialize_on_nested_object(self):
        classA1 = ClassA(id=json_classC["classAs"][0]["id"], name=json_classC["classAs"][0]["name"])
        classA2 = ClassA(id=json_classC["classAs"][1]["id"], name=json_classC["classAs"][1]["name"])
        classC = ClassC(id=json_classC["id"], role=json_classC["role"], classAs=[classA1, classA2])
        actual = classC.serializeable()
        self.assertListEqual(sorted(list(json_classC.keys())), sorted(list(actual.keys())))
