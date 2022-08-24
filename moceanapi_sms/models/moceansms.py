# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
import requests
import time
import logging

logging.basicConfig(filename="E:/moceansms.log")
_logger = logging.getLogger(__name__)


class SMSConnection (models.Model):
    _name = "moceansms.smsconnection"

    name = fields.Char(string='Connection Name', required=True, size=100)
    api_key = fields.Text(string='API Key', required=True,
                          help='mocean-api-key')
    api_secret = fields.Text(
        string='API Secret', required=True, help='mocean-api-secret')
    sender_name = fields.Char(string='Sender Name',
                              required=True, size=100, help='mocean-from')
    history_id = fields.One2many(
        'moceansms.smshistory', 'connection_id', "History")
    queue_line = fields.One2many(
        "moceansms.smsqueue", "connection_id", readonly=True)


class SMSHistory(models.Model):
    _name = "moceansms.smshistory"
    connection_id = fields.Many2one(
        'moceansms.smsconnection', 'Connection', ondelete='set null')
    recipient = fields.Text(string="Recipient", required=True)
    message = fields.Text(string="Message", required=True)
    state = fields.Char(size=10, string="status")
    sent_time = fields.Datetime(
        'Action Time', readonly=True,  default=fields.Datetime.now())
    user_id = fields.Many2one("res.users", "Username")


class SMSQueue(models.Model):
    _name = "moceansms.smsqueue"
    _description = "SMS Queue"

    action_time = fields.Datetime(
        'Action Time', readonly=True,  default=fields.Datetime.now())
    message = fields.Text(string="Message")
    recipient = fields.Text(string="Recipient",help="Allow send to multiple recipient. Put (,) in between phone number.")
    connection_id = fields.Many2one("moceansms.smsconnection",
                                    "Connection"
                                    )
    state = fields.Selection([
        ('draft', 'Queued'),
        ('sending', 'Waiting'),
        ('send', 'Sent'),
        ('error', 'Error'),
    ],
        'Message Status',
        readonly=True,
        default='draft'
    )

    user_id = fields.Many2one(
        'res.users', string='Username', default=lambda self: self.env.user)
    reserve_key = fields.Char(size=30)
    send_to_all = fields.Boolean(default=False)

    def cron_sms(self):

        unique_key = time.time()
        self.env["moceansms.smsqueue"].search([("state", "=", "draft")]).write(
            {"reserve_key": unique_key, "state": "sending"})

        pending_sms = self.env["moceansms.smsqueue"].search(
            [("reserve_key", "=", unique_key)])


        for sms in pending_sms:

            params = {
                "mocean-api-key": sms.connection_id.api_key,
                "mocean-api-secret": sms.connection_id.api_secret,
                "mocean-from": sms.connection_id.sender_name,
                "mocean-to": sms.recipient,
                "mocean-text": sms.message,
                "mocean-resp-format": "JSON",
                "mocean-medium": "odoo"
            }

            if self.send(params) == True:
                params["state"] = "sent"
            else:
                params["state"] = "error"

            params["connection_id"] = sms.connection_id.id
            params["user_id"] = sms.user_id.id

            self.history(params, sms.connection_id)
            self.env["moceansms.smsqueue"].search(
                [("id", "=", sms.id)]).unlink()

    def send(self, data):
        url = 'https://rest.moceanapi.com/rest/2/sms'

        try:
            res = requests.post(url, data=data)
            res_data = res.json()
            if str(res.status_code) != "202":
                _logger.error("Fail to send sms due to %s" %
                              (res_data.err_msg))
                return False
        except Exception:
            _logger.error("Fail to send sms due to %s" % (e))
            return False
        return True

    def history(self, data, connection_id):
        self.env["moceansms.smshistory"].create({
            "recipient": data["mocean-to"],
            "message": data["mocean-text"],
            "state": data["state"],
            "connection_id": data["connection_id"],
            "user_id": data["user_id"]
        })
        return True

    def cron_mark_sms_expire(self):

        queue_sms = self.env["moceansms.smsqueue"].search(
            [("reserve_key", "!=", "")])
        current_time = time.time()

        for sms in queue_sms:

            expire_time = float(sms.reserve_key) + float("86400")

            if current_time > expire_time:
                self.env["moceansms.smsqueue"].search(
                    ["id", "=", sms.id]).unlink()

                self.history(
                    {
                        "mocean-to": sms.recipient,
                        "mocean-text": sms.message,
                        "user_id": sms.user_id,
                        "connection_id": sms.connction_id,
                        "state": "error"
                    }
                )
