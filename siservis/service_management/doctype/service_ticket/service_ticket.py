import frappe
from frappe.model.document import Document


class ServiceTicket(Document):
    def validate(self):
        self.set_default_status()

    def after_insert(self):
        self.create_service_report()

    def set_default_status(self):
        if not self.status:
            self.status = "Open"

    def create_service_report(self):
        if self.service_report:
            return

        report = frappe.new_doc("Service Report")
        report.service_ticket = self.name
        report.status = "Draft"

        report.insert(ignore_permissions=True)

        self.db_set("service_report", report.name)