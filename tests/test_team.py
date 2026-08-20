import unittest

from models.team import Team


class TestTeamModel(unittest.TestCase):
    def test_initial_values(self):
        team = Team(id=10, name="Test Team", wins=5, losses=3)

        self.assertEqual(team.id, 10)
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.wins, 5)
        self.assertEqual(team.losses, 3)

    def test_name_setter_updates_value(self):
        team = Team(id=10, name="Test Team", wins=5, losses=3)

        team.name = "Updated Team Name"
        self.assertEqual(team.name, "Updated Team Name")

    def test_wins_setter_updates_value(self):
        team = Team(id=10, name="Test Team", wins=5, losses=3)

        team.wins = 12
        self.assertEqual(team.wins, 12)

    def test_losses_setter_updates_value(self):
        team = Team(id=10, name="Test Team", wins=5, losses=3)

        team.losses = 8
        self.assertEqual(team.losses, 8)


if __name__ == "__main__":
    unittest.main()