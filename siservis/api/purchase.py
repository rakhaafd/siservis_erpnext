import frappe


@frappe.whitelist()
def submit_purchase_order(name):
    doc = frappe.get_doc("Purchase Order", name)

    if doc.docstatus != 0:
        frappe.throw("Purchase Order is already submitted or cancelled.")

    doc.submit()
    frappe.db.commit()

    return {
        "message": "Purchase Order submitted successfully",
        "purchase_order": doc.name
    }


@frappe.whitelist()
def submit_purchase_receipt(name):
    doc = frappe.get_doc("Purchase Receipt", name)

    if doc.docstatus != 0:
        frappe.throw("Purchase Receipt is already submitted or cancelled.")

    doc.submit()
    frappe.db.commit()

    return {
        "message": "Purchase Receipt submitted successfully",
        "purchase_receipt": doc.name
    }


@frappe.whitelist()
def submit_purchase_invoice(name):
    doc = frappe.get_doc("Purchase Invoice", name)

    if doc.docstatus != 0:
        frappe.throw("Purchase Invoice is already submitted or cancelled.")

    doc.submit()
    frappe.db.commit()

    return {
        "message": "Purchase Invoice submitted successfully",
        "purchase_invoice": doc.name
    }


@frappe.whitelist()
def submit_payment_entry(name):
    doc = frappe.get_doc("Payment Entry", name)

    if doc.docstatus != 0:
        frappe.throw("Payment Entry is already submitted or cancelled.")

    doc.submit()
    frappe.db.commit()

    return {
        "message": "Payment Entry submitted successfully",
        "payment_entry": doc.name
    }