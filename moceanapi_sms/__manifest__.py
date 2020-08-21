# -*- coding: utf-8 -*-
{
    "name": "MoceanAPI SMS",
    "version": "13.0.0.0",
    "depends": ["base","mail"],
    "author": "MoceanAPI Developer",
    "license" : "LGPL-3",
    "images": [
        "images/connection_list.png",
        "images/connection_create.png",
        "images/sms_queue_list.png",
        "images/sms_create.png",
        "images/sms_history.png"
    ],
    "description": """
        To get started, go to our website https://moceanapi.com to register a new account to claim 20 free credit.

    """,
    "website": "https://moceanapi.com",
    "category": "Tools",
    "demo": [],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "view/moceansms.xml",
        "moceansms_data.xml"            
    ],
    "active": False,
    "installable": True,
    "application": True,
    "images": ["images/icon.png"]
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
