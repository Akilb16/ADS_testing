import streamlit as st
from datetime import datetime

def render_form(i, data, file):
    with st.form(f"form_{i}"):
        vendor_name = st.text_input("Vendor Name", value=data.get("vendorName", ""), key=f"vn_{i}")
        invoice_number = st.text_input("Invoice Number", value=data.get("invoiceNumber", ""), key=f"inv_{i}")
        vendor_trn = st.text_input("Vendor TRN", value=data.get("vendorTRN", ""), key=f"trn_{i}")

        try:
            parsed_date = datetime.strptime(data.get("invoiceDate", ""), "%Y-%m-%d")
        except:
            parsed_date = datetime.today()
        invoice_date = st.date_input("Invoice Date", value=parsed_date, key=f"dt_{i}")

        before_tax = st.number_input("Before Tax Amount", value=float(data.get("beforeTaxAmount") or 0.0), key=f"bt_{i}")
        tax_amount = st.number_input("Tax Amount", value=float(data.get("taxAmount") or 0.0), key=f"ta_{i}")
        after_tax = st.number_input("Total (After Tax)", value=float(data.get("afterTaxAmount") or 0.0), key=f"at_{i}")

        st.markdown("### Line Items")
        edited_line_items = []

        for idx, li in enumerate(data.get("lineItems", [])):
            st.markdown(f"**Item {idx + 1}**")
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                name = st.text_input(f"Item Name {i}_{idx}", value=li.get("name", ""), key=f"name_{i}_{idx}")
            with c2:
                qty = st.number_input(f"Qty {i}_{idx}", value=int(li.get("qty", 0)), min_value=0, key=f"qty_{i}_{idx}")
            with c3:
                rate = st.number_input(f"Rate {i}_{idx}", value=float(li.get("rate", 0)), min_value=0.0, key=f"rate_{i}_{idx}")
            edited_line_items.append({"name": name, "qty": qty, "rate": rate})

        submit = st.form_submit_button("Submit Invoice")

        if submit:
            return {
                "vendor_name": vendor_name,
                "invoice_number": invoice_number,
                "vendor_trn": vendor_trn,
                "invoice_date": invoice_date.strftime("%Y-%m-%d"),
                "before_tax_amount": before_tax,
                "tax_amount": tax_amount,
                "after_tax_amount": after_tax,
                "line_items": edited_line_items,
                "file_name": file.name,
            }

    return None

def render_expense_form(i, data, file):
    with st.form(f"expense_form_{i}"):
        vendor_name = st.text_input("Expense Title", value=data.get("vendorName", ""), key=f"e_vn_{i}")
        invoice_number = st.text_input("Reference Number", value=data.get("invoiceNumber", ""), key=f"e_inv_{i}")

        try:
            parsed_date = datetime.strptime(data.get("invoiceDate", ""), "%Y-%m-%d")
        except:
            parsed_date = datetime.today()
        invoice_date = st.date_input("Date", value=parsed_date, key=f"e_dt_{i}")

        before_tax = st.number_input("Amount Before Tax", value=float(data.get("beforeTaxAmount") or 0.0), key=f"e_bt_{i}")
        tax_amount = st.number_input("Tax Amount", value=float(data.get("taxAmount") or 0.0), key=f"e_ta_{i}")
        after_tax = st.number_input("Total Amount", value=float(data.get("afterTaxAmount") or 0.0), key=f"e_at_{i}")

        st.markdown("### Line Items")
        edited_line_items = []

        for idx, li in enumerate(data.get("lineItems", [])):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                name = st.text_input(f"Expense Item Name {i}_{idx}", value=li.get("name", ""), key=f"e_name_{i}_{idx}")
            with c2:
                qty = st.number_input(f"Qty {i}_{idx}", value=int(li.get("qty", 0)), min_value=0, key=f"e_qty_{i}_{idx}")
            with c3:
                rate = st.number_input(f"Rate {i}_{idx}", value=float(li.get("rate", 0)), min_value=0.0, key=f"e_rate_{i}_{idx}")
            edited_line_items.append({"name": name, "qty": qty, "rate": rate})

        submit = st.form_submit_button("Submit Expense")

        if submit:
            return {
                "vendor_name": vendor_name,
                "invoice_number": invoice_number,
                "invoice_date": invoice_date.strftime("%Y-%m-%d"),
                "before_tax_amount": before_tax,
                "tax_amount": tax_amount,
                "after_tax_amount": after_tax,
                "line_items": edited_line_items,
                "file_name": file.name,
            }, True

    return None, False
