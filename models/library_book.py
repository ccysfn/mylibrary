# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many(
        'res.partner',
        string='Authors'
    )
    state = fields.Selection([
         ('draft', 'Unavailable'),
         ('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
         'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
         ('available', 'borrowed'),
         ('borrowed', 'available'),
         ('available', 'lost'),
         ('borrowed', 'lost'),
         ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue

    @api.model
    def make_available(self):
        self.change_state('available')

    @api.model
    def make_borrowed(self):
        self.change_state('borrowed')

    @api.model
    def make_lost(self):
        self.change_state('lost')

