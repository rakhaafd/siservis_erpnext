import frappe


@frappe.whitelist()
def get_my_tickets():
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    customer = frappe.db.get_value(
        "Customer", {"email_id": frappe.session.user}, "name"
    )

    if not customer:
        return []

    return frappe.get_all(
        "Service Ticket",
        filters={"customer": customer},
        fields=[
            "name",
            "customer",
            "device_type",
            "brand",
            "model",
            "serial_number",
            "problem_description",
            "service_report",
            "status",
            "creation",
        ],
        order_by="creation desc",
    )


@frappe.whitelist()
def get_my_invoices():
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    customer = frappe.db.get_value(
        "Customer", {"email_id": frappe.session.user}, "name"
    )

    if not customer:
        return []

    return frappe.get_all(
        "Sales Invoice",
        filters={"customer": customer},
        fields=[
            "name",
            "posting_date",
            "status",
            "grand_total",
            "outstanding_amount",
            "currency",
            "docstatus",
        ],
        order_by="creation desc",
    )


@frappe.whitelist()
def get_invoice_detail(invoice_name):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    customer = frappe.db.get_value(
        "Customer", {"email_id": frappe.session.user}, "name"
    )

    invoice = frappe.get_doc("Sales Invoice", invoice_name)

    if invoice.customer != customer:
        frappe.throw("Not permitted")

    return invoice.as_dict()
