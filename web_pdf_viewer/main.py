# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-
import ast
import base64
import csv
import glob
import itertools
import operator
import datetime
import hashlib
import os
import re
import simplejson
import time
import urllib
import urllib2
import urlparse
import xmlrpclib
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
from openerp.tools.translate import _
from ..web import controllers
from ..web import http
openerpweb = http


def content_disposition(filename, req):
    filename = filename.encode('utf8')
    escaped = urllib2.quote(filename)
    browser = req.httprequest.user_agent.browser
    version = int((req.httprequest.user_agent.version or '0').split('.')[0])
    if browser == 'msie' and version < 9:
        return "attachment; filename=%s" % escaped
    elif browser == 'safari':
        return "attachment; filename=%s" % filename
    else:
        return "attachment; filename*=UTF-8''%s" % escaped



class Reports(controllers.main.Reports):
    _cp_path = "/web/report"
    POLLING_DELAY = 0.25
    TYPES_MAPPING = {
        'doc': 'application/vnd.ms-word',
        'html': 'text/html',
        'odt': 'application/vnd.oasis.opendocument.text',
        'pdf': 'application/pdf',
        'sxw': 'application/vnd.sun.xml.writer',
        'xls': 'application/vnd.ms-excel',
    }

    @openerpweb.httprequest
    def index(self, req, action, token):
        action = simplejson.loads(action)
        report_srv = req.session.proxy("report")
        context = dict(req.context)
        context.update(action["context"])

        report_data = {}
        report_ids = context["active_ids"]
        if 'report_type' in action:
            report_data['report_type'] = action['report_type']
        if 'datas' in action:
            if 'ids' in action['datas']:
                report_ids = action['datas'].pop('ids')
            report_data.update(action['datas'])

        report_id = report_srv.report(
            req.session._db, req.session._uid, req.session._password,
            action["report_name"], report_ids,
            report_data, context)

        report_struct = None
        while True:
            report_struct = report_srv.report_get(
                req.session._db, req.session._uid, req.session._password, report_id)
            if report_struct["state"]:
                break

            time.sleep(self.POLLING_DELAY)

        report = base64.b64decode(report_struct['result'])
        if report_struct.get('code') == 'zlib':
            report = zlib.decompress(report)
        report_mimetype = self.TYPES_MAPPING.get(
            report_struct['format'], 'application/x-google-chrome-print-preview-pdf')
        file_name = action.get('name', 'report')
        if 'name' not in action:
            reports = req.session.model('ir.actions.report.xml')
            res_id = reports.search([('report_name', '=', action['report_name']),],
                                    0, False, False, context)
            if len(res_id) > 0:
                file_name = reports.read(res_id[0], ['name'], context)['name']
            else:
                file_name = action['report_name']
        file_name = '%s.%s' % (file_name, report_struct['format'])
        if action.get('report_type') and action.get('report_type') == 'pdf':
            return req.make_response(report,
             headers=[
                 ('Content-Type', report_mimetype),
                 ('Content-Length', len(report))],
             cookies={'fileToken': int(token)})
        
        return req.make_response(report,
             headers=[
                 ('Content-Disposition', content_disposition(file_name, req)),
                 ('Content-Type', report_mimetype),
                 ('Content-Length', len(report))],
             cookies={'fileToken': int(token)})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
