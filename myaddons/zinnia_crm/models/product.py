# -*- coding: utf-8 -*-

import base64
import hashlib
import threading
import urllib2

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.modules import get_module_resource


class Product(models.Model):
    _name = "crm.product"
    name=fields.Char(string="Name",required=True )
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized image of this contact. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
                                help="Small-sized image of this contact. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field anywhere a small image is required.")

    category_id=fields.Many2one('crm.product_category', string="Category",required=True)
    type=fields.Selection([
        ('product_store','Product can be stored'),
        ('product_consumed',"Product can be consumed"),
        ('service',"Service")
    ])
    price=fields.Integer(string="Price")

    @api.model
    def _get_default_image(self, partner_type, is_company, parent_id):
        if getattr(threading.currentThread(), 'testing', False) or self._context.get('install_mode'):
            return False

        colorize, img_path, image = False, False, False

        if partner_type in ['other'] and parent_id:
            parent_image = self.browse(parent_id).image
            image = parent_image and parent_image.decode('base64') or None

        if not image and partner_type == 'invoice':
            img_path = get_module_resource('base', 'static/src/img', 'money.png')
        elif not image and partner_type == 'delivery':
            img_path = get_module_resource('base', 'static/src/img', 'truck.png')
        elif not image and is_company:
            img_path = get_module_resource('base', 'static/src/img', 'company_image.png')
        elif not image:
            img_path = get_module_resource('base', 'static/src/img', 'avatar.png')
            colorize = True

        if img_path:
            with open(img_path, 'rb') as f:
                image = f.read()
        if image and colorize:
            image = tools.image_colorize(image)

        return tools.image_resize_image_big(image.encode('base64'))

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)

        result = True

        result = result and super(Product, self).write(vals)
        return result
    @api.model
    def create(self, vals):
        if vals.get('website'):
            vals['website'] = self._clean_website(vals['website'])
        if vals.get('parent_id'):
            vals['company_name'] = False
        # compute default image in create, because computing gravatar in the onchange
        # cannot be easily performed if default images are in the way
        if not vals.get('image'):
            vals['image'] = self._get_default_image(vals.get('type'), vals.get('is_company'), vals.get('parent_id'))
        tools.image_resize_images(vals)
        partner = super(Product, self).create(vals)
        # partner._fields_sync(vals)
        # partner._handle_first_contact_creation()
        return partner

    def _get_gravatar_image(self, email):
        gravatar_image = False
        email_hash = hashlib.md5(email.lower()).hexdigest()
        url = "https://www.gravatar.com/avatar/" + email_hash
        try:
            image_content = urllib2.urlopen(url + "?d=404&s=128", timeout=5).read()
            gravatar_image = base64.b64encode(image_content)
        except Exception:
            pass
        return gravatar_image

