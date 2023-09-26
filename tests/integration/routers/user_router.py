
from fastapi.testclient import TestClient


class TestUserReadSelf:
    """All tests for the endpoint GET /me"""

    def test_read_self_valid(client: TestClient):
        """Best case scenario"""
        # TODO là jsp vraiment comment ça marche parce qu'il y a
        # tout un bordel d'authentification ... on peut pas tester
        # l'envoi de SMS, et donc comment on récupère un token ?
        # A moins de recréer une fonction d'authentification qui fait un code
        # de vérification bidon et fixe comme on avait avant.
