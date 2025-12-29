# -*- coding: utf-8 -*-
from unittest import TestCase
from api.routes.light import router
from models.light import Light
from tests.test_database import BaseDBTest


class TestLightEndpoints(TestCase, BaseDBTest):
    @classmethod
    def setUpClass(cls):
        cls.client = cls.create_test_app(router)

    def setUp(self):
        self.reset_db()

    def _insert_light(self, status: bool):
        db = self.SessionLocal()
        try:
            ev = Light(light_status=status)
            db.add(ev)
            db.commit()
            db.refresh(ev)
            return ev
        finally:
            db.close()

    def test_light_on_crea_evento_si_no_hay_registros(self):
        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['light_status'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_light_on_no_crea_evento_si_ultimo_ya_esta_on(self):
        last = self._insert_light(True)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['light_status'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_id'], last.id)

    def test_light_on_crea_evento_si_ultimo_esta_off(self):
        self._insert_light(False)

        r = self.client.post('/on')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertTrue(data['light_status'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_light_off_crea_evento_si_no_hay_registros(self):
        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['light_status'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_light_off_no_crea_evento_si_ultimo_ya_esta_off(self):
        last = self._insert_light(False)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['light_status'])
        self.assertFalse(data['created'])
        self.assertEqual(data['last_id'], last.id)

    def test_light_off_crea_evento_si_ultimo_esta_on(self):
        self._insert_light(True)

        r = self.client.post('/off')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertFalse(data['light_status'])
        self.assertTrue(data['created'])
        self.assertIn('id', data)

    def test_light_status_devuelve_error_si_no_hay_registros(self):
        r = self.client.get('/light_status')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertEqual(data, {'error': 'There are no records'})

    def test_light_status_devuelve_estado_del_ultimo_registro(self):
        self._insert_light(True)

        r = self.client.get('/light_status')
        self.assertEqual(r.status_code, 200)
        data = r.json()

        self.assertEqual(data, {'light_status': True})
