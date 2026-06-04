frappe.ui.form.on("Service Report", {
	refresh(frm) {
		calculate_grand_total(frm);

		if (
			!frm.is_new() &&
			frm.doc.status === "Completed" &&
			!frm.doc.sales_invoice
		) {
			frm.add_custom_button("Create Sales Invoice", () => {
				frappe.call({
					method: "siservis.service_management.doctype.service_report.service_report.create_sales_invoice",
					args: {
						service_report: frm.doc.name
					},
					callback(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.set_route("Form", "Sales Invoice", r.message);
						}
					}
				});
			});
		}
	}
});

frappe.ui.form.on("Service Part Used", {
	item(frm, cdt, cdn) {
		let row = locals[cdt][cdn];

		if (!row.item) return;

		frappe.db.get_value(
			"Item Price",
			{
				item_code: row.item,
				price_list: "Standard Selling"
			},
			"price_list_rate"
		).then(r => {
			let rate = 0;

			if (r.message && r.message.price_list_rate) {
				rate = r.message.price_list_rate;
			}

			frappe.model.set_value(cdt, cdn, "rate", rate);

			if (!row.qty) {
				frappe.model.set_value(cdt, cdn, "qty", 1);
			}

			frappe.model.set_value(
				cdt,
				cdn,
				"amount",
				(row.qty || 1) * rate
			);

			setTimeout(() => {
				calculate_grand_total(frm);
			}, 200);
		});
	},

	qty(frm, cdt, cdn) {
		calculate_part_amount(frm, cdt, cdn);
	},

	rate(frm, cdt, cdn) {
		calculate_part_amount(frm, cdt, cdn);
	},

	parts_used_remove(frm) {
		calculate_grand_total(frm);
	}
});

function calculate_part_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];

	let qty = row.qty || 0;
	let rate = row.rate || 0;

	frappe.model.set_value(cdt, cdn, "amount", qty * rate);

	setTimeout(() => {
		calculate_grand_total(frm);
	}, 100);
}

function calculate_grand_total(frm) {
	let total = 0;

	(frm.doc.parts_used || []).forEach(row => {
		total += row.amount || 0;
	});

	frm.set_value("grand_total", total);
}