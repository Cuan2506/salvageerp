# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (c) 2010-2012 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'PDF Viewer',
    'version': '1.1',
    'category': 'Tools',
    'description': """
PDF Viewer
==========

If you not getting proper output Download Plugin from below sites

For Firefox
----------- 
https://addons.mozilla.org/En-us/firefox/addon/pdfjs/

For Chrome
----------
https://chrome.google.com/webstore/detail/chrome-office-viewer/gbkeegbaiigmenfmjfclcdgdpimamgkj?utm_source=chrome-ntp-icon
    """,
    "author": "OpenERP SA",
    "website": "http://www.openerp.com",
    'depends': ["web", ],
    'init_xml': [],

    'css':[
        'static/src/css/close_button.css',
    ],
    "js" : [
        "static/src/js/web_pdf_viewer.js",
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
