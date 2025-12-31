# -*- coding: utf-8 -*-
import os
from datetime import datetime, timezone, timedelta
from unittest import TestCase
from unittest.mock import AsyncMock, patch

from api.routes.sighting import router
from models.alert import AlertSwitch
from models.sighting import Sighting
from tests.test_database import BaseDBTest



class TestSightingEndpoint(TestCase, BaseDBTest):
    @classmethod
    def setUpClass(cls):
        cls.client = cls.create_test_app(router)

    def setUp(self):
        self.reset_db()

        os.environ['RECENTLY_SIGHTING'] = '300'
        os.environ['TELEGRAM_SIGHTING_MESSAGE'] = 'Sighting detected'
        os.environ['CAMERA_URL'] = 'http://camera.local/stream'

    def _insert_alert(self, enabled: bool):
        db = self.SessionLocal()
        try:
            a = AlertSwitch(enabled=enabled)
            db.add(a)
            db.commit()
            db.refresh(a)
            return a
        finally:
            db.close()

    def _insert_sighting(self, *, message_send: bool, dt):
        db = self.SessionLocal()
        try:
            s = Sighting(message_send=message_send, date=dt)
            db.add(s)
            db.commit()
            db.refresh(s)
            return s
        finally:
            db.close()

    def test_disabled_alerts_no_message(self):
        self._insert_alert(False)

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), ['Alerts are not enabled'])
            smock.assert_not_awaited()

    def test_no_last_sighting_send_message(self):
        self._insert_alert(True)

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            data = r.json()

            self.assertEqual(data, {'received': True, 'message_send': True})

            expected = 'Sighting detected - URL: http://camera.local/stream'
            smock.assert_awaited_once_with(expected)

        db = self._db()
        try:
            last = db.query(Sighting).order_by(Sighting.id.desc()).first()
            self.assertIsNotNone(last)
            self.assertTrue(last.message_send)
        finally:
            db.close()

    def test_recent_sighting_no_message_false_record(self):
        self._insert_alert(True)

        os.environ['RECENTLY_SIGHTING'] = '300'

        now = datetime.now(timezone.utc)
        self._insert_sighting(message_send=True, dt=now - timedelta(seconds=10))

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), {'received': True, 'message_send': False})
            smock.assert_not_awaited()

        db = self._db()
        try:
            last = db.query(Sighting).order_by(Sighting.id.desc()).first()
            self.assertFalse(last.message_send)
        finally:
            db.close()

    def test_old_sighting_send_message(self):
        self._insert_alert(True)
        os.environ['RECENTLY_SIGHTING'] = '300'

        now = datetime.now(timezone.utc)
        self._insert_sighting(message_send=True, dt=now - timedelta(seconds=301))

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), {'received': True, 'message_send': True})

            expected = 'Sighting detected - URL: http://camera.local/stream'
            smock.assert_awaited_once_with(expected)

    def test_naive_sighting_utc(self):
        self._insert_alert(True)
        os.environ['RECENTLY_SIGHTING'] = '300'

        naive_old = (datetime.now(timezone.utc) - timedelta(seconds=301)).replace(tzinfo=None)
        self._insert_sighting(message_send=True, dt=naive_old)

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), {'received': True, 'message_send': True})
            smock.assert_awaited_once()

    def test_message_from_env(self):
        self._insert_alert(True)

        os.environ['TELEGRAM_SIGHTING_MESSAGE'] = 'ALERTA'
        os.environ['CAMERA_URL'] = 'https://example.com/cam'

        with patch('api.routes.sighting.send_message', new=AsyncMock()) as smock:
            r = self.client.get('/sighting_message')
            self.assertEqual(r.status_code, 200)
            self.assertTrue(r.json()['message_send'])

            smock.assert_awaited_once_with('ALERTA - URL: https://example.com/cam')
