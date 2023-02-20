# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date 

class cliente(models.Model):
	_name = 'gestion_clientes.cliente'
	_description = 'Cliente'

	name = fields.Char('DNI', required=True)
	nombre = fields.Char(string='Nombre', required=True)
	apellidos = fields.Char(string='Apellidos', required=False)
	telefono = fields.Integer('Teléfono')
	email = fields.Char(string='Email', required=False)
	fecha_nacimiento = fields.Date(string='Fecha de nacimiento',required=True)
	edad = fields.Integer("Años", compute="_get_annos")
	
	#Relaciones
	ids_facturas=fields.One2many('gestion_clientes.factura', 'id_factura', string='factura')
	
	#Autocalculo de la fecha de nacimiento	
	@api.depends('fecha_nacimiento')
	def _get_annos(self):
		for cliente in self:
			hoy = date.today()
			cliente.edad = relativedelta(hoy, cliente.fecha_nacimiento).years

class factura(models.Model):
	_name = 'gestion_clientes.factura'
	_description = 'Factura del cliente'
	
	name = fields.Char('ID Factura', required=True)
	importe_total = fields.Integer('Importe total')
		
	#Relaciones		
	id_factura=fields.Many2one('gestion_clientes.cliente', string='cliente')
	ids_lineas=fields.One2many('gestion_clientes.linea', 'id_linea', string='linea')
	

class linea(models.Model):
	_name = 'gestion_clientes.linea'
	_description = 'Linea de una factura'
	
	name = fields.Char('ID Linea', required=True)
	cantidad = fields.Integer('Cantidad de productos')
	precio = fields.Integer('Precio')
	subtotal = fields.Integer("Subtotal", compute="_get_subtotal")
	
	#Relaciones	
	id_linea = fields.Many2one('gestion_clientes.factura', string='factura')	
	ids_productos = fields.One2many('gestion_clientes.producto', 'id_producto', string='producto')	

	#Autocalculo del subtotal
	@api.depends('subtotal')
	def _get_subtotal(self):
		for linea in self:
			total = linea.cantidad * linea.precio
			linea.subtotal = total	

	
class producto(models.Model):
	_name = 'gestion_clientes.producto'
	_description = 'Productos de la linea de la factura'
	
	name = fields.Char('ID Producto', required=True)
	stock = fields.Integer('Stock')
	descripcion = fields.Char('Descripcion', required=True)

	#Relaciones
	id_producto = fields.Many2one('gestion_clientes.linea', string='linea')

	
