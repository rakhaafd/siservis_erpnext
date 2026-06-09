import frappe
from frappe.model.document import Document


class ServiceReport(Document):
    def validate(self):
        self.calculate_totals()
        self.update_service_ticket_status()

    def calculate_totals(self):
        total = 0

        for part in self.parts_used or []:
            part.amount = (part.qty or 0) * (part.rate or 0)
            total += part.amount

        self.grand_total = total

    def update_service_ticket_status(self):
        if not self.service_ticket:
            return

        status_map = {
            "Draft": "Open",
            "In Progress": "In Progress",
            "Waiting Parts": "Waiting Parts",
            "Completed": "Completed",
            "Cancelled": "Cancelled",
        }

        ticket_status = status_map.get(self.status)

        if ticket_status:
            frappe.db.set_value(
                "Service Ticket",
                self.service_ticket,
                {
                    "status": ticket_status,
                    "service_report": self.name,
                }
            )


@frappe.whitelist()
def create_sales_invoice(service_report):
    report = frappe.get_doc("Service Report", service_report)

    if report.sales_invoice:
        return report.sales_invoice

    if report.status != "Completed":
        frappe.throw(
            "Sales Invoice can only be created when Service Report is Completed."
        )

    if not report.parts_used:
        frappe.throw(
            "Please add at least one item in Parts Used before creating Sales Invoice."
        )

    ticket = frappe.get_doc("Service Ticket", report.service_ticket)

    invoice = frappe.new_doc("Sales Invoice")
    invoice.customer = ticket.customer
    invoice.due_date = frappe.utils.today()
    invoice.update_stock = 1

    default_warehouse = "siwarehouse - MS"

    for part in report.parts_used:
        item = frappe.get_doc("Item", part.item)

        row = {
            "item_code": part.item,
            "qty": part.qty,
            "rate": part.rate,
        }

        if item.is_stock_item:
            row["warehouse"] = default_warehouse

        invoice.append("items", row)

    invoice.insert(ignore_permissions=True)

    report.sales_invoice = invoice.name
    report.save(ignore_permissions=True)

    return invoice.name