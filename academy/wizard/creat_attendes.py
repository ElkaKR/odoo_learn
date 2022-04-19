# -*- coding: utf-8 -*-
from odoo import models, fields

class CreatAttendesWizard(models.TransientModel):
    _name = "creat.attendes.wizard"
    _description = "Creat attendes wizard"

    def default_session(self):
        return self.env['academy.session'].browse(self._context.get('active_id'))

    session_idw = fields.Many2many('academy.session', string="Session", required=True, default=default_session)
    attendee_idw = fields.Many2many('res.partner')

    def add_attendees_to_sessions(self):
        for session in self.session_idw:
            for at in self.attendee_idw:
                session.attendee_id = [(4, at.id)]

