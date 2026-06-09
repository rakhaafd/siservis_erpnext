import frappe


@frappe.whitelist(allow_guest=True)
def register_customer(full_name, email, password, mobile_no=None):

    if frappe.db.exists("User", email):

        frappe.throw("Email already registered")

    user = frappe.get_doc(
        {
            "doctype": "User",
            "email": email,
            "first_name": full_name,
            "enabled": 1,
            "new_password": password,
            "send_welcome_email": 0,
            "desk_access": 0,
            "roles": [{"role": "Customer"}],
        }
    )

    user.insert(ignore_permissions=True)

    customer = frappe.get_doc(
        {
            "doctype": "Customer",
            "customer_name": full_name,
            "customer_type": "Individual",
            "mobile_no": mobile_no,
            "email_id": email,
        }
    )

    customer.insert(ignore_permissions=True)

    return {
        "message": "Customer registered successfully",
        "user": user.name,
        "customer": customer.name,
    }
