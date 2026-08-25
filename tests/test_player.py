import unittest

from models.player import Player


class TestPlayerModel(unittest.TestCase):
    def test_initial_values(self):
        player = Player(id=10, team_id=42, first_name='John', last_name='Doe', position='Pitcher', jersey_number=7)

        self.assertEqual(player.id, 10)
        self.assertEqual(player.teamid, 42)
        self.assertEqual(player.first_name, 'John')
        self.assertEqual(player.last_name, 'Doe')
        self.assertEqual(player.position, 'Pitcher')
        self.assertEqual(player.jersey_number, 7)

    def test_teamid_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith', position='Catcher', jersey_number=12)

        player.teamid = 99
        self.assertEqual(player.teamid, 99)

    def test_first_name_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith', position='Catcher', jersey_number=12)

        player.first_name = 'Anna'
        self.assertEqual(player.first_name, 'Anna')

    def test_last_name_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith', position='Catcher', jersey_number=12)

        player.last_name = 'Johnson'
        self.assertEqual(player.last_name, 'Johnson')

    def test_position_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith', position='Catcher', jersey_number=12)

        player.position = 'Shortstop'
        self.assertEqual(player.position, 'Shortstop')

    def test_jersey_number_setter_updates_value(self):
        player = Player(id=1, team_id=2, first_name='Jane', last_name='Smith', position='Catcher', jersey_number=12)

        player.jersey_number = 15
        self.assertEqual(player.jersey_number, 15)


if __name__ == "__main__":
    unittest.main()
