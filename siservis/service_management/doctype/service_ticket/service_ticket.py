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

@frappe.whitelist()
def delete_service_ticket(ticket):
    if not frappe.db.exists("Service Ticket", ticket):
        frappe.throw("Service Ticket not found.")

    reports = frappe.get_all(
        "Service Report",
        filters={"service_ticket": ticket},
        pluck="name"
    )

    frappe.db.set_value(
        "Service Ticket",
        ticket,
        "service_report",
        None
    )

    for report in reports:
        frappe.delete_doc(
            "Service Report",
            report,
            force=True
        )

    frappe.delete_doc(
        "Service Ticket",
        ticket,
        force=True
    )

    frappe.db.commit()

    return {
        "message": "Service Ticket and linked Service Report deleted successfully.",
        "deleted_ticket": ticket,
        "deleted_reports": reports
    }