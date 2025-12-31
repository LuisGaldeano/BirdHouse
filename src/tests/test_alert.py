# -*- coding: utf-8 -*-
from unittest import TestCase
from api.routes.alert import router
from models.alert import AlertSwitch
from tests.test_database import BaseDBTest


class TestAlertSwitchEndpoints(TestCase, BaseDBTest):
    @classmethod
    def setUpClass(cls):
        cls.client = cls.create_test_app(router)

    def setUp(self):
        self.reset_db()

    def _insert_alert(self, enabled: bool):
        db = self.SessionLocal()
        try:
            ev = AlertSwitch(enabled=enabled)
            db.add(ev)
            db.commit()
            db.refresh(ev)
            return ev
        finally:
            db.close()

    def test_alert_on_creates_event_if_no_records(self):
        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_alert_on_no_event_if_last_on(self):
        last = self._insert_alert(True)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_alert_id'], last.id)

    def test_alert_on_creates_event_if_last_off(self):
        self._insert_alert(False)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_alert_off_creates_event_if_empty(self):
        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_alert_off_no_event_if_last_off(self):
        last = self._insert_alert(False)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_alert_id'], last.id)

    def test_alert_off_creates_event_if_last_on(self):
        self._insert_alert(True)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_alert_status_error_if_empty(self):
        r = self.client.get('/alert_status')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'error': 'There are no records'})

    def test_alert_status_returns_last_state(self):
        self._insert_alert(True)

        r = self.client.get('/alert_status')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'alert_status': True})
