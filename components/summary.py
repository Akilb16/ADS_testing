import streamlit as st
import streamlit.components.v1 as components

def render_summary(data):
    st.markdown("### Extracted Summary")
    st.markdown(f"**Invoice Number:** {data.get('invoiceNumber', 'N/A')}")
    st.markdown(f"**Vendor Name:** {data.get('vendorName', 'N/A')}")
    st.markdown(f"**Vendor TRN:** {data.get('vendorTRN', 'N/A')}")
    st.markdown(f"**Invoice Date:** {data.get('invoiceDate', 'N/A')}")
    st.markdown(f"**Before Tax:** ₹{data.get('beforeTaxAmount', 0)}")
    st.markdown(f"**Tax:** ₹{data.get('taxAmount', 0)}")
    st.markdown(f"**Total Amount:** ₹{data.get('afterTaxAmount', 0)}")
    st.markdown("**Line Items:**")
    for li in data.get("lineItems", []):
        st.markdown(f"- {li.get('name')} | Qty: {li.get('qty')} | Rate: ₹{li.get('rate')}")

def render_accounting_summary(data):
    item = data

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f"""
            <div style="font-size: 1.1rem;">
                <b>Invoice Number:</b> <span style="color:#1a73e8;">{item['data']['invoiceNumber']}</span><br>
                <b>Invoice Date:</b> {item['data']['invoiceDate']}<br>
                <b>Before Tax Amount:</b> ₹{item['data']['beforeTaxAmount']}<br>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "Invoice Number in accounting software" in item:
            st.markdown(
                f"<b>Invoice Number in accounting software:</b> <span style='color:#34a853;'>{item['Invoice Number in accounting software']}</span>",
                unsafe_allow_html=True,
            )
        st.markdown(
            f"""
            <div style="font-size: 1.1rem;">
                <b>Tax Amount:</b> ₹{item['data']['taxAmount']}<br>
                <b>After Tax Amount:</b> <span style="color:#e37400;">₹{item['data']['afterTaxAmount']}</span><br>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        with st.container():
            

            table_rows = ""
            for li in item['data'].get('lineItems', []):
                qty = li.get('qty', '')
                rate = li.get('rate', '')
                try:
                    amount = float(qty) * float(rate)
                except Exception:
                    amount = 0.0
                table_rows += f"""
                    <tr>
                        <td style="padding: 6px; border: 1px solid #ddd;">{li.get('name', '')}</td>
                        <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{qty}</td>
                        <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{rate}</td>
                        <td style="padding: 6px; border: 1px solid #ddd; text-align: right;">{amount:.2f}</td>
                    </tr>
                """

            table_html = f"""
                <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 10px;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="padding: 6px; border: 1px solid #ddd;">Item</th>
                            <th style="padding: 6px; border: 1px solid #ddd; text-align: right;">Qty</th>
                            <th style="padding: 6px; border: 1px solid #ddd; text-align: right;">Rate</th>
                            <th style="padding: 6px; border: 1px solid #ddd; text-align: right;">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            """

            components.html(table_html, height=300, scrolling=True)


def render_expense_summary(data_list):
    st.markdown("## Submitted Expenses")
    for i, data in enumerate(data_list):
        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"**Title:** {data.get('vendor_name', 'N/A')}")
                st.markdown(f"**Invoice Number:** {data.get('invoice_number', 'N/A')}")
                st.markdown(f"**Date:** {data.get('invoice_date', 'N/A')}")
            with col2:
                st.markdown(f"**Before Tax:** ₹{data.get('before_tax_amount', 0)}")
                st.markdown(f"**Tax:** ₹{data.get('tax_amount', 0)}")
                st.markdown(f"**Total:** ₹{data.get('after_tax_amount', 0)}")
