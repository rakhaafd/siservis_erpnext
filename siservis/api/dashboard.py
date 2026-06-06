import frappe
from frappe.utils import today, get_first_day, get_last_day


def format_idr(value):
    value = float(value or 0)
    return "Rp {:,.0f}".format(value).replace(",", ".")

@frappe.whitelist()
def low_stock_alert():
    return get_low_stock_items()

@frappe.whitelist()
def dashboard_summary():
    today_date = today()
    month_start = get_first_day(today_date)
    month_end = get_last_day(today_date)

    revenue_today = get_revenue(today_date, today_date)
    revenue_this_month = get_revenue(month_start, month_end)

    return {
    "revenue_today": format_idr(revenue_today),
    "revenue_this_month": format_idr(revenue_this_month),

    "revenue_services": format_idr(
        get_revenue_by_item_group("Services", month_start, month_end)
    ),

    "revenue_spareparts": format_idr(
        get_revenue_by_item_group("Products", month_start, month_end)
    ),

    "revenue_by_technician": get_revenue_by_technician(month_start, month_end),

    "open_tickets": get_ticket_count("Open"),
    "in_progress_tickets": get_ticket_count("In Progress"),
    "completed_tickets": get_ticket_count("Completed"),

    "total_customers": frappe.db.count("Customer"),
    "total_technicians": frappe.db.count("Employee"),

    "low_stock_items": get_low_stock_items()
}

def get_revenue(from_date, to_date):
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(base_grand_total), 0)
        FROM `tabSales Invoice`
        WHERE docstatus = 1
        AND posting_date BETWEEN %s AND %s
    """, (from_date, to_date))

    return result[0][0] or 0

def get_revenue_by_technician(from_date, to_date):
    rows = frappe.db.sql("""
        SELECT
            sr.technician,
            emp.employee_name,
            COALESCE(SUM(si.base_grand_total), 0) AS revenue
        FROM `tabService Report` sr
        JOIN `tabSales Invoice` si ON si.name = sr.sales_invoice
        LEFT JOIN `tabEmployee` emp ON emp.name = sr.technician
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        GROUP BY sr.technician
        ORDER BY revenue DESC
    """, (from_date, to_date), as_dict=True)

    for row in rows:
        row["revenue"] = format_idr(row.revenue)

    return rows

def get_revenue_by_item_group(
    item_group,
    from_date,
    to_date
):
    result = frappe.db.sql("""
        SELECT COALESCE(SUM(sii.base_amount), 0)
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si
            ON si.name = sii.parent
        JOIN `tabItem` item
            ON item.name = sii.item_code
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND item.item_group = %s
    """, (from_date, to_date, item_group))

    return result[0][0] or 0


def get_ticket_count(status):
    return frappe.db.count(
        "Service Ticket",
        {"status": status}
    )


def get_low_stock_items():
    return frappe.db.sql("""
        SELECT
            bin.item_code,
            item.item_name,
            bin.warehouse,
            bin.actual_qty
        FROM `tabBin` bin
        JOIN `tabItem` item
            ON item.name = bin.item_code
        WHERE
            item.is_stock_item = 1
            AND bin.actual_qty <= 5
        ORDER BY bin.actual_qty ASC
        LIMIT 5
    """, as_dict=True)