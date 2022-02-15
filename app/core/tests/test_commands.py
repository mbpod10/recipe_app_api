from unittest.mock import patch

"""To call a management command from code use call_command."""
from django.core.management import call_command

from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]

            """app/core/management/commands/wait_for_db.py"""

            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

    def test_figure_out_how_it_works(self):
        """See is its possible to get it to print"""
        call_command('print_to_screen')
