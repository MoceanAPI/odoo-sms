{
    "name": "MoceanAPI SMS",
    "version": "18.0.0.0",
    "summary": "SMS integration with MoceanAPI",
    "description": """
        To get started, go to our website https://moceanapi.com to register a new account to claim 20 free credits.
    """,
    "author": "MoceanAPI Developer",
    "website": "https://moceanapi.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base", "mail", "web"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "view/moceansms.xml",
        "moceansms_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "moceanapi_sms/static/src/css/main.css",
            "moceanapi_sms/static/src/css/cookieconsent.min.css",
            "moceanapi_sms/static/src/js/cookieconsent.min.js",
            "moceanapi_sms/static/src/js/yandex.js",
        ],
        'web.assets_qweb': [
            'moceanapi_sms/static/src/xml/*.xml',
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
