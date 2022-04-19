# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class TestCourseModel(models.Model):
    _name = "academy.course"
    _description = "Description courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Char(string="Description")
    respons_user_id = fields.Many2one('res.users', string="responsible")
    session_id = fields.One2many('academy.session', 'course')

    _sql_constraints = [
        ('name_descr',
         'CHECK(name != description)',
         "The name of the course matches description!"),

        ('name_mustbe_uniq',
         "UNIQUE(name)",
         "You already have course with such name!")]

    def copy(self, default=None):
        new_name = 'Copy of ' + self.name
        default = dict(default or {}, name=new_name)
        return super(TestCourseModel, self).copy(default)


class SessionsModel(models.Model):
    _name = "academy.session"
    _description = "Session of courses"

    name = fields.Char(string="Title", required=True)
    start_date = fields.Date(string="Start date", required=True, default=fields.Date.today())
    duration = fields.Integer(string="Duration", required=True)
    end_date = fields.Date(compute='_compute_end_date', store=True)
    number_of_seats = fields.Integer(string="Number of seat")
    instructor_id = fields.Many2one('res.partner', string="instructor", domain=['|', ('instructor', '=', True),
                                                                                '|', ('teacher', '=', "teacher_level1"),
                                                                                ('teacher', '=', "teacher_level2")])
    course = fields.Many2one('academy.course', required=True)
    attendee_id = fields.Many2many('res.partner', string="Attendees")
    percent_taken_seats = fields.Float(compute='_compute_percent_taken_seats')
    active = fields.Boolean(default=True, string="Active")
    attendes_count = fields.Integer(compute='_compute_attendes_count', store=True)

    @api.depends('attendee_id')
    def _compute_attendes_count(self):
        for rec in self:
            rec.attendes_count = len(rec.attendee_id)

    @api.depends('attendee_id', 'number_of_seats')
    def _compute_percent_taken_seats(self):

        for rec in self:
            if not rec.number_of_seats:
                rec.percent_taken_seats = 0
            else:
                rec.percent_taken_seats = len(rec.attendee_id) * 100 / rec.number_of_seats

    @api.onchange('number_of_seats')
    def _message_error_seats(self):
        if self.number_of_seats < 0:
            self.number_of_seats = 0
            return {'warning': {'title': 'Некорректное значение', 'message': 'You set negative count of seats!'}}

    @api.onchange('number_of_seats', 'attendee_id')
    def _message_error_seats(self):
        if self.number_of_seats >= 0 and len(self.attendee_id) > self.number_of_seats:
            return {
                'warning': {'title': 'Некорректное значение', 'message': 'Count of attendes more then count of seats!'}}

    @api.constrains('instructor_id', 'attendee_id')
    def _check_instructor(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id in rec.attendee_id:
                raise ValidationError("Your instructor is in list of attendes")

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if not rec.start_date:
                rec.end_date = datetime.date.today()
            else:
                rec.end_date = rec.start_date + timedelta(days=rec.duration)


class PartnerModel(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    teacher = fields.Selection([('teacher_level1', "teacher level 1"), ('teacher_level2', "teacher level 2")])
    session = fields.Many2many('academy.session', readonly=True)
