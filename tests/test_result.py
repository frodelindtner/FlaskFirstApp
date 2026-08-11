import unittest

from models.result import Result


class TestResultModel(unittest.TestCase):
    def test_initial_values(self):
        result = Result(id=10, team_id=42, wins=5, losses=3)

        self.assertEqual(result.id, 10)
        self.assertEqual(result.teamid, 42)
        self.assertEqual(result.wins, 5)
        self.assertEqual(result.losses, 3)

    def test_teamid_setter_updates_value(self):
        result = Result(id=1, team_id=7, wins=0, losses=0)

        result.teamid = 99
        self.assertEqual(result.teamid, 99)

    def test_wins_setter_updates_value(self):
        result = Result(id=1, team_id=7, wins=0, losses=0)

        result.wins = 12
        self.assertEqual(result.wins, 12)

    def test_losses_setter_updates_value(self):
        result = Result(id=1, team_id=7, wins=0, losses=0)

        result.losses = 8
        self.assertEqual(result.losses, 8)


if __name__ == "__main__":
    unittest.main()
