frappe.ui.form.on("Service Part Used", {
	qty(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},

	rate(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	}
});

function calculate_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];

	row.amount = (row.qty || 0) * (row.rate || 0);

	frm.refresh_field("parts_used");

	calculate_total_parts(frm);
}

function calculate_total_parts(frm) {
	let total = 0;

	(frm.doc.parts_used || []).forEach(row => {
		total += row.amount || 0;
	});

	frm.set_value("total_parts_cost", total);

	let service_cost = frm.doc.service_cost || 0;

	frm.set_value(
		"grand_total",
		service_cost + total
	);
}