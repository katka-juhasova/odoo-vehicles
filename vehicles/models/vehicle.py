# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Vehicle(models.Model):
    _name = 'vehicles.vehicle'
    _description = 'Vehicle'
    _order = 'license_plate asc, model_id asc'

    @api.depends('brand_id.name', 'model_id.name', 'license_plate')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = ('/'.join([record.brand_id.name or '',
                                     record.model_id.name or '',
                                     record.license_plate or 'No Plate']))

    def _get_default_state(self):
        state = self.env.ref('vehicles.vehicle_state_registered', raise_if_not_found=False)
        return state if state and state.id else False

    name = fields.Char(compute='_compute_vehicle_name', store=True)
    license_plate = fields.Char('License Plate', copy=False,
                                help='License plate number of the vehicle (i = plate number for a car)', required=True)
    vin_sn = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)',
                         copy=False)
    brand_id = fields.Many2one('fleet.vehicle.model.brand', 'Brand', related="model_id.brand_id", store=True)
    model_id = fields.Many2one('fleet.vehicle.model', 'Model', required=True, help='Model of the vehicle')
    model_year = fields.Char('Model Year', help='Year of the model')
    state_id = fields.Many2one('vehicles.vehicle.state', 'Status', default=_get_default_state, tracking=True,
                               help='Current state of the vehicle', ondelete='set null',
                               group_expand='_read_group_stage_ids',)
    employee_id = fields.Many2one('hr.employee', 'Employee', help='Employee to whom is the vehicle assigned',
                                  copy=False, tracking=True, ondelete='set null')

    description = fields.Text('Vehicle Description')
    image_128 = fields.Image(related='model_id.image_128', readonly=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['vehicles.vehicle.state'].search([], order=order)

    _sql_constraints = [('vehicle_license_plate_unique', 'unique(license_plate)', 'License plate already exists'),
                        ('vehicle_vin_sn_unique', 'unique(vin_sn)', 'Chassis number already exists')]


class VehicleState(models.Model):
    _name = 'vehicles.vehicle.state'
    _order = 'sequence asc'
    _description = 'Vehicle Status'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(help="Used to order the note stages")

    _sql_constraints = [('vehicle_state_name_unique', 'unique(name)', 'State name already exists')]
