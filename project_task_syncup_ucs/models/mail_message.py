# -*- coding: utf-8 -*-
from odoo import api, fields, models,_


class Message(models.Model):
    _inherit = 'mail.message'

    child_message_id = fields.Many2one('mail.message', string='Child Message')

    @api.model_create_multi
    def create(self, vals):
        messages = super(Message, self).create(vals)
        task_obj =self.env['project.task']
        for message in messages:
            if message.model == 'project.task':
                task = task_obj.browse(message.res_id)
                if task.project_id:
                    child_task = task_obj.search([('client_task_id', '=', task.id)])
                    if child_task:
                        attachment_ids = []
                        if message.attachment_ids:
                            for attachment in message.attachment_ids:
                                copied_attachment = attachment.copy({
                                    'res_model': 'mail.message',
                                    'res_id': child_task.id
                                })
                                attachment_ids.append(copied_attachment.id)

                        child_message = child_task.with_context(portal_log=True).message_post(
                            body=message.body,
                            attachment_ids=attachment_ids
                        )
                        message.child_message_id = child_message.id
        return message

    def write(self, vals):
        result = super(Message, self).write(vals)
        for message in self:
            if message.model == 'project.task' and message.child_message_id:
                child_message = message.child_message_id
                child_message.write({'body': vals.get('body', child_message.body)})
                if 'attachment_ids' in vals:
                    attachment_commands = vals.get('attachment_ids', [])
                    attachment_ids = [command[1] for command in attachment_commands if command[0] == 4]
                    attachments = self.env['ir.attachment'].browse(attachment_ids)
                    for attachment in attachments:
                        copied_attachment = attachment.copy({
                            'res_model': 'mail.message',
                            'res_id': child_message.id
                        })
                        child_message.write({
                            'attachment_ids': [(4, copied_attachment.id)]
                        })
        return result


