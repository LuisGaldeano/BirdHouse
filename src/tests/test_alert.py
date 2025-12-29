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

    def test_alert_on_crea_evento_si_no_hay_registros(self):
        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_alert_on_no_crea_evento_si_ultimo_ya_esta_on(self):
        last = self._insert_alert(True)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_alert_id'], last.id)

    def test_alert_on_crea_evento_si_ultimo_esta_off(self):
        self._insert_alert(False)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_alert_off_crea_evento_si_no_hay_registros(self):
        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_alert_off_no_crea_evento_si_ultimo_ya_esta_off(self):
        last = self._insert_alert(False)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_alert_id'], last.id)

    def test_alert_off_crea_evento_si_ultimo_esta_on(self):
        self._insert_alert(True)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['enabled'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_alert_status_devuelve_error_si_no_hay_registros(self):
        r = self.client.get('/alert_status')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'error': 'There are no records'})

    def test_alert_status_devuelve_estado_del_ultimo_registro(self):
        self._insert_alert(True)

        r = self.client.get('/alert_status')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'alert_status': True})
