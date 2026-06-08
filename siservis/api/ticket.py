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
