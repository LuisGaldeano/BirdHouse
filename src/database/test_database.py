import settings

from datetime import datetime, timedelta
from unittest import TestCase
from database.database import Sighting


class SightingTest(TestCase):
    def test_recently_sighting(self):
        sighting = Sighting(date=datetime.now())
        self.assertTrue(sighting.recently_sighting)
        sighting = Sighting(date=datetime.now() - timedelta(seconds=2 * settings.RECENTLY_SIGHTING))
        self.assertFalse(sighting.recently_sighting)

    def test_str(self):
        sighting = Sighting(
            id=0,
            date=datetime.now(),
            message_send=True
        )
        self.assertEqual(str(sighting), f'{sighting.id} - {sighting.date} - {sighting.message_send}')
