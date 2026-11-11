
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# BOOMER FINANCIAL COMMAND CENTRE
# Illustrative planning model - INR
# =========================================================

st.set_page_config(
    page_title="BOOMER Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🧴 BOOMER | Financial Command Centre")
st.caption(
    "From 3,000-unit market experiment to ₹500 crore annual sales. "
    "All figures are planning assumptions, not guaranteed results."
)

# ---------------------- HELPERS ---------------------------

def inr(value):
    return f"₹{value:,.0f}"

def crore(value):
    return f"₹{value / 1e7:,.2f} Cr"

def lakh(value):
    return f"₹{value / 1e5:,.2f} L"

def metric_card(label, value, help_text=None):
    st.metric(label, value, help=help_text)

# ---------------------- SIDEBAR ---------------------------

st.sidebar.header("Business assumptions")

target_type = st.sidebar.selectbox(
    "₹500 crore target means",
    ["Company net revenue", "Consumer MRP sales"]
)

target_sales_cr = st.sidebar.number_input(
    "Annual sales target (₹ crore)",
    min_value=1.0,
    max_value=10000.0,
    value=500.0,
    step=25.0
)

projection_years = st.sidebar.slider(
    "Years to reach target",
    min_value=3,
    max_value=20,
    value=10
)

st.sidebar.subheader("Pricing and channel economics")

avg_mrp = st.sidebar.number_input(
    "Weighted average MRP per unit (₹)",
    min_value=1.0,
    value=136.67,
    step=1.0
)

gst_rate = st.sidebar.number_input(
    "Illustrative GST rate (%)",
    min_value=0.0,
    max_value=40.0,
    value=18.0,
    step=0.5
) / 100

retailer_margin = st.sidebar.number_input(
    "Retailer margin (%)",
    min_value=0.0,
    max_value=80.0,
    value=15.0,
    step=1.0
) / 100

distributor_margin = st.sidebar.number_input(
    "Distributor margin (%)",
    min_value=0.0,
    max_value=80.0,
    value=8.0,
    step=1.0
) / 100

manufacturing_cost = st.sidebar.number_input(
    "Manufacturing cost per unit (₹)",
    min_value=0.0,
    value=34.0,
    step=1.0
)

variable_selling_cost = st.sidebar.number_input(
    "Other variable selling cost per unit (₹)",
    min_value=0.0,
    value=10.0,
    step=1.0
)

st.sidebar.subheader("Operating assumptions")

opex_percent = st.sidebar.slider(
    "Operating expenses (% of net revenue)",
    min_value=0,
    max_value=50,
    value=15
) / 100

depreciation_percent = st.sidebar.slider(
    "Depreciation (% of net revenue)",
    min_value=0,
    max_value=15,
    value=2
) / 100

interest_percent = st.sidebar.slider(
    "Interest (% of net revenue)",
    min_value=0,
    max_value=15,
    value=1
) / 100

tax_rate = st.sidebar.slider(
    "Illustrative tax rate (%)",
    min_value=0,
    max_value=40,
    value=25
) / 100

marketing_percent = st.sidebar.slider(
    "Marketing included in operating expenses (%)",
    min_value=0,
    max_value=30,
    value=5
)

st.sidebar.caption(
    "Marketing is shown as a planning sub-allocation of operating "
    "expenses. Do not deduct it twice."
)


st.sidebar.subheader("Three-statement & cash-flow assumptions")
opening_cash = st.sidebar.number_input("Opening cash balance (₹)", min_value=0.0, value=500000.0, step=50000.0)
opening_share_capital = st.sidebar.number_input("Opening share capital (₹)", min_value=0.0, value=500000.0, step=50000.0)
receivable_days = st.sidebar.number_input("Receivable days (DSO)", min_value=0.0, max_value=180.0, value=30.0, step=5.0)
inventory_days = st.sidebar.number_input("Inventory days", min_value=0.0, max_value=365.0, value=45.0, step=5.0)
payable_days = st.sidebar.number_input("Payable days (DPO)", min_value=0.0, max_value=180.0, value=30.0, step=5.0)
capex_percent = st.sidebar.number_input("Annual capital expenditure (% of revenue)", min_value=0.0, max_value=50.0, value=3.0, step=0.5) / 100
debt_draw_percent = st.sidebar.number_input("New debt raised (% of revenue)", min_value=0.0, max_value=50.0, value=0.0, step=0.5) / 100
debt_repayment_percent = st.sidebar.number_input("Annual debt repayment (% of opening debt)", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100
equity_raise = st.sidebar.number_input("Additional equity raised each year (₹)", min_value=0.0, value=0.0, step=100000.0)

# ---------------------- CALCULATIONS ----------------------

# Simplified channel model:
# MRP includes GST; retailer and distributor margins are
# applied sequentially to the ex-GST selling value.
ex_gst_price = avg_mrp / (1 + gst_rate)

company_realisation = (
    ex_gst_price
    * (1 - retailer_margin)
    * (1 - distributor_margin)
)

if target_type == "Company net revenue":
    target_units = (
        target_sales_cr * 1e7 / company_realisation
        if company_realisation > 0 else 0
    )
else:
    target_units = (
        target_sales_cr * 1e7 / avg_mrp
        if avg_mrp > 0 else 0
    )

target_units = int(target_units)

# ---------------------- TOP KPIs --------------------------

st.subheader("Business overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Pilot batch", "3,000 units")
c2.metric("MRP per unit", inr(avg_mrp))
c3.metric("Company realisation / unit", inr(company_realisation))
c4.metric("Units needed for target", f"{target_units:,.0f}")

st.info(
    f"To achieve ₹{target_sales_cr:.0f} crore in "
    f"{target_type.lower()}, BOOMER needs approximately "
    f"{target_units:,.0f} units annually, or "
    f"{target_units / 12:,.0f} units per month."
)

# ---------------------- PILOT EXPERIMENT ------------------

st.header("1. Initial 3,000-unit experiment")

st.write(
    "Edit the quantities and MRPs below to test your first production batch."
)

default_skus = pd.DataFrame({
    "Product": [
        "Dishwashing liquid",
        "Fabric washing liquid",
        "Floor cleaner",
        "Toilet cleaner"
    ],
    "Pilot units": [1000, 500, 750, 750],
    "MRP per unit": [120, 280, 90, 110],
    "Manufacturing cost per unit": [34, 34, 34, 34]
})

sku_data = st.data_editor(
    default_skus,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Pilot units": st.column_config.NumberColumn(
            min_value=0, step=50
        ),
        "MRP per unit": st.column_config.NumberColumn(
            min_value=0, step=5
        ),
        "Manufacturing cost per unit":
            st.column_config.NumberColumn(min_value=0, step=1)
    },
    key="sku_editor"
)

sku_data["Pilot MRP value"] = (
    sku_data["Pilot units"] * sku_data["MRP per unit"]
)

sku_data["Manufacturing expenditure"] = (
    sku_data["Pilot units"]
    * sku_data["Manufacturing cost per unit"]
)

pilot_units = int(sku_data["Pilot units"].sum())
pilot_mrp_value = sku_data["Pilot MRP value"].sum()
pilot_manufacturing = sku_data["Manufacturing expenditure"].sum()

pilot_ex_gst = pilot_mrp_value / (1 + gst_rate)

pilot_company_revenue = (
    pilot_ex_gst
    * (1 - retailer_margin)
    * (1 - distributor_margin)
)

pilot_variable_cost = pilot_units * variable_selling_cost

pilot_opex = st.number_input(
    "One-time pilot launch and operating expenses (₹)",
    min_value=0,
    value=50000,
    step=5000
)

pilot_gross_profit = pilot_company_revenue - pilot_manufacturing

pilot_ebitda = (
    pilot_gross_profit
    - pilot_variable_cost
    - pilot_opex
)

pilot_tax = max(0, pilot_ebitda * tax_rate)
pilot_net_profit = pilot_ebitda - pilot_tax

p1, p2, p3, p4 = st.columns(4)

p1.metric("Pilot units", f"{pilot_units:,}")
p2.metric("Total MRP value", inr(pilot_mrp_value))
p3.metric("Estimated company revenue", inr(pilot_company_revenue))
p4.metric("Manufacturing cost", inr(pilot_manufacturing))

p5, p6, p7 = st.columns(3)

p5.metric("Gross profit", inr(pilot_gross_profit))
p6.metric("EBITDA", inr(pilot_ebitda))
p7.metric("Illustrative net profit", inr(pilot_net_profit))

st.dataframe(
    sku_data,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Pilot calculations are simplified. Actual SKU-level GST, "
    "channel margins, schemes, freight, returns, input tax credit "
    "and other costs need professional validation."
)

# ---------------------- UNIT ECONOMICS --------------------

st.header("2. Unit economics")

unit_table = pd.DataFrame({
    "Particulars": [
        "Consumer MRP",
        "MRP excluding assumed GST",
        "Retailer and distributor deductions",
        "Estimated company realisation",
        "Manufacturing cost",
        "Variable selling cost",
        "Contribution before fixed operating expenses"
    ],
    "Amount per unit (₹)": [
        avg_mrp,
        ex_gst_price,
        ex_gst_price - company_realisation,
        company_realisation,
        manufacturing_cost,
        variable_selling_cost,
        company_realisation
        - manufacturing_cost
        - variable_selling_cost
    ]
})

st.dataframe(
    unit_table.style.format({"Amount per unit (₹)": "₹{:,.2f}"}),
    use_container_width=True,
    hide_index=True
)

contribution = (
    company_realisation
    - manufacturing_cost
    - variable_selling_cost
)

if contribution <= 0:
    st.error(
        "Your current unit economics are negative before fixed "
        "expenses. Review pricing, manufacturing cost or channel margins."
    )
else:
    st.success(
        f"Contribution before fixed expenses: ₹{contribution:,.2f} per unit."
    )

# ---------------------- FIVE / TEN YEAR FORECAST ----------

st.header("3. Growth from pilot to ₹500 crore")

st.write(
    "The pilot is treated as a one-time experiment. The forecast "
    "starts with a separate Year 1 annual sales assumption."
)

year1_units = st.number_input(
    "Year 1 annual units sold",
    min_value=1000,
    value=36000,
    step=1000
)

# Smooth geometric path from Year 1 to target annual volume.
if projection_years == 1:
    annual_units = np.array([target_units])
else:
    annual_units = np.geomspace(
        max(1, year1_units),
        max(year1_units, target_units),
        projection_years
    ).round().astype(int)

forecast_rows = []

for index, quantity in enumerate(annual_units):
    year = index + 1

    net_revenue = quantity * company_realisation
    mrp_sales = quantity * avg_mrp
    cogs = quantity * manufacturing_cost
    gross_profit = net_revenue - cogs

    variable_cost = quantity * variable_selling_cost
    operating_expenses = net_revenue * opex_percent

    ebitda = (
        gross_profit
        - variable_cost
        - operating_expenses
    )

    depreciation = net_revenue * depreciation_percent
    interest = net_revenue * interest_percent

    pbt = ebitda - depreciation - interest
    tax = max(0, pbt * tax_rate)
    net_profit = pbt - tax

    forecast_rows.append({
        "Year": f"Year {year}",
        "Annual units": quantity,
        "Monthly average units": quantity / 12,
        "Consumer MRP sales": mrp_sales,
        "Company net revenue": net_revenue,
        "Manufacturing cost": cogs,
        "Gross profit": gross_profit,
        "Variable selling cost": variable_cost,
        "Operating expenses": operating_expenses,
        "EBITDA": ebitda,
        "Depreciation": depreciation,
        "Interest": interest,
        "Profit before tax": pbt,
        "Tax": tax,
        "Net profit": net_profit
    })

forecast = pd.DataFrame(forecast_rows)

st.dataframe(
    forecast.style.format({
        "Annual units": "{:,.0f}",
        "Monthly average units": "{:,.0f}",
        "Consumer MRP sales": "₹{:,.0f}",
        "Company net revenue": "₹{:,.0f}",
        "Manufacturing cost": "₹{:,.0f}",
        "Gross profit": "₹{:,.0f}",
        "Variable selling cost": "₹{:,.0f}",
        "Operating expenses": "₹{:,.0f}",
        "EBITDA": "₹{:,.0f}",
        "Depreciation": "₹{:,.0f}",
        "Interest": "₹{:,.0f}",
        "Profit before tax": "₹{:,.0f}",
        "Tax": "₹{:,.0f}",
        "Net profit": "₹{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ---------------------- CHARTS ----------------------------

st.subheader("Revenue growth")

chart_data = forecast.melt(
    id_vars="Year",
    value_vars=[
        "Consumer MRP sales",
        "Company net revenue"
    ],
    var_name="Sales category",
    value_name="Amount"
)

fig = px.bar(
    chart_data,
    x="Year",
    y="Amount",
    color="Sales category",
    barmode="group",
    title="Consumer MRP sales vs company net revenue"
)

st.plotly_chart(fig, use_container_width=True)

profit_data = forecast.melt(
    id_vars="Year",
    value_vars=[
        "Gross profit",
        "EBITDA",
        "Net profit"
    ],
    var_name="Profit measure",
    value_name="Amount"
)

fig2 = px.line(
    profit_data,
    x="Year",
    y="Amount",
    color="Profit measure",
    markers=True,
    title="Profit progression"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------- MILESTONES ------------------------

st.header("4. Business expansion milestones")

milestones = [
    ("Pilot", 3000),
    ("Local validation", 36000),
    ("Regional distribution", 300000),
    ("North India scale", 1200000),
    ("National distribution", 5000000),
    ("Large-scale national business", 15000000),
    ("₹500 Cr target", target_units)
]

milestone_df = pd.DataFrame(
    milestones,
    columns=["Business stage", "Annual units"]
)

milestone_df["Monthly units"] = (
    milestone_df["Annual units"] / 12
)

milestone_df["Estimated company revenue"] = (
    milestone_df["Annual units"] * company_realisation
)

st.dataframe(
    milestone_df.style.format({
        "Annual units": "{:,.0f}",
        "Monthly units": "{:,.0f}",
        "Estimated company revenue": "₹{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ---------------------- FACTORY CALCULATOR ----------------

st.header("5. Own factory investment calculator")

factory_capex = st.number_input(
    "Estimated factory investment (₹ crore)",
    min_value=0.0,
    value=2.0,
    step=0.25
) * 1e7

factory_saving = st.number_input(
    "Estimated manufacturing saving per unit (₹)",
    min_value=0.0,
    value=5.0,
    step=0.5
)

annual_factory_volume = st.number_input(
    "Annual units manufactured in own factory",
    min_value=0,
    value=1200000,
    step=100000
)

annual_saving = factory_saving * annual_factory_volume

payback_years = (
    factory_capex / annual_saving
    if annual_saving > 0 else None
)

f1, f2, f3 = st.columns(3)

f1.metric("Factory investment", crore(factory_capex))
f2.metric("Potential annual savings", lakh(annual_saving))

if payback_years is not None:
    f3.metric("Simple payback period", f"{payback_years:.1f} years")
else:
    f3.metric("Simple payback period", "Not calculable")

st.caption(
    "This is a simple payback illustration, not an investment "
    "recommendation. Include labour, utilities, maintenance, "
    "quality, compliance, finance and working capital in a full model."
)


# ---------------- THREE-STATEMENT MODEL --------------------

st.header("6. Integrated three-statement model")
st.caption("Annual integrated forecast: income statement, balance sheet and cash flow. Working-capital balances are calculated from DSO, inventory days and DPO.")

statement_rows = []
balance_rows = []
cashflow_rows = []
working_capital_rows = []

prior_ar = prior_inventory = prior_ap = 0.0
prior_ppe = 0.0
prior_debt = 0.0
cash = float(opening_cash)
share_capital = float(opening_share_capital)
retained_earnings = 0.0

for _, r in forecast.iterrows():
    revenue = float(r["Company net revenue"])
    cogs = float(r["Manufacturing cost"])
    depreciation = float(r["Depreciation"])
    net_income = float(r["Net profit"])
    ebitda_value = float(r["EBITDA"])
    interest_value = float(r["Interest"])
    tax_value = float(r["Tax"])

    ar = revenue * receivable_days / 365
    inventory = cogs * inventory_days / 365
    ap = cogs * payable_days / 365
    nwc = ar + inventory - ap
    prior_nwc = prior_ar + prior_inventory - prior_ap
    change_nwc = nwc - prior_nwc

    capex = revenue * capex_percent
    closing_ppe = prior_ppe + capex - depreciation
    closing_ppe = max(0.0, closing_ppe)

    debt_draw = revenue * debt_draw_percent
    debt_repayment = min(prior_debt, prior_debt * debt_repayment_percent)
    closing_debt = prior_debt + debt_draw - debt_repayment

    equity_injection = float(equity_raise)
    cfo = net_income + depreciation - change_nwc
    cfi = -capex
    cff = debt_draw - debt_repayment + equity_injection
    opening_cash_for_year = cash
    net_change_cash = cfo + cfi + cff
    closing_cash = opening_cash_for_year + net_change_cash

    share_capital += equity_injection
    retained_earnings += net_income
    total_assets = closing_cash + ar + inventory + closing_ppe
    total_liabilities = ap + closing_debt
    total_equity = share_capital + retained_earnings
    balance_check = total_assets - total_liabilities - total_equity

    year_label = r["Year"]
    statement_rows.append({
        "Year": year_label, "Revenue": revenue, "COGS": cogs,
        "Gross profit": float(r["Gross profit"]), "Operating expenses": float(r["Operating expenses"]),
        "EBITDA": ebitda_value, "Depreciation": depreciation, "EBIT": ebitda_value - depreciation,
        "Interest": interest_value, "Profit before tax": float(r["Profit before tax"]),
        "Tax": tax_value, "Net income": net_income
    })
    cashflow_rows.append({
        "Year": year_label, "Net income": net_income, "Depreciation & amortisation": depreciation,
        "Change in net working capital": -change_nwc, "Cash flow from operations": cfo,
        "Capital expenditure": -capex, "Cash flow from investing": cfi,
        "Debt raised": debt_draw, "Debt repayment": -debt_repayment,
        "Equity raised": equity_injection, "Cash flow from financing": cff,
        "Net change in cash": net_change_cash, "Opening cash": opening_cash_for_year,
        "Closing cash": closing_cash
    })
    working_capital_rows.append({
        "Year": year_label, "Accounts receivable": ar, "Inventory": inventory,
        "Accounts payable": ap, "Net working capital": nwc,
        "Change in net working capital": change_nwc,
        "DSO": receivable_days, "Inventory days": inventory_days, "DPO": payable_days
    })

    # Balance sheet values are saved after the cash-flow bridge is calculated.
    balance_rows.append({
        "Year": year_label, "Cash": closing_cash, "Accounts receivable": ar,
        "Inventory": inventory, "Net PP&E": closing_ppe, "Total assets": total_assets,
        "Accounts payable": ap, "Debt": closing_debt, "Total liabilities": total_liabilities,
        "Share capital": share_capital, "Retained earnings": retained_earnings,
        "Total equity": total_equity, "Total liabilities & equity": total_liabilities + total_equity,
        "Balance check (should be 0)": balance_check
    })

    cash, prior_ar, prior_inventory, prior_ap = closing_cash, ar, inventory, ap
    prior_ppe, prior_debt = closing_ppe, closing_debt

income_statement = pd.DataFrame(statement_rows)
balance_sheet = pd.DataFrame(balance_rows)
cash_flow = pd.DataFrame(cashflow_rows)
working_capital = pd.DataFrame(working_capital_rows)

st.subheader("Income statement")
st.dataframe(income_statement.style.format({c: "₹{:,.0f}" for c in income_statement.columns if c != "Year"}), use_container_width=True, hide_index=True)
st.subheader("Balance sheet")
st.dataframe(balance_sheet.style.format({c: "₹{:,.0f}" for c in balance_sheet.columns if c != "Year"}), use_container_width=True, hide_index=True)
st.subheader("Advanced cash flow statement")
st.dataframe(cash_flow.style.format({c: "₹{:,.0f}" for c in cash_flow.columns if c != "Year"}), use_container_width=True, hide_index=True)
st.subheader("Working-capital schedule")
st.dataframe(working_capital.style.format({c: ("{:,.1f}" if c in ["DSO", "Inventory days", "DPO"] else "₹{:,.0f}") for c in working_capital.columns if c != "Year"}), use_container_width=True, hide_index=True)

latest_bs = balance_sheet.iloc[-1]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Forecast closing cash", inr(latest_bs["Cash"]))
k2.metric("Forecast debt", inr(latest_bs["Debt"]))
k3.metric("Net working capital", inr(latest_bs["Accounts receivable"] + latest_bs["Inventory"] - latest_bs["Accounts payable"]))
k4.metric("Balance-sheet check", inr(latest_bs["Balance check (should be 0)"]))

if (balance_sheet["Balance check (should be 0)"].abs() > 1).any():
    st.warning("The balance sheet does not balance. Review opening balances and assumptions.")
else:
    st.success("Balance sheet balances across all forecast years under the model assumptions.")

st.subheader("Cash-flow analysis")
cash_chart = px.bar(cash_flow, x="Year", y=["Cash flow from operations", "Cash flow from investing", "Cash flow from financing"], barmode="group", title="Cash flow by activity")
st.plotly_chart(cash_chart, use_container_width=True)
cash_balance_chart = px.line(cash_flow, x="Year", y=["Opening cash", "Closing cash"], markers=True, title="Cash balance movement")
st.plotly_chart(cash_balance_chart, use_container_width=True)

# ---------------------- PROFESSIONAL EXCEL EXPORT ----------------------

st.header("7. Download professional Excel financial model")
st.caption("Workbook includes formatted schedules, KPI dashboard, and native Excel charts. Figures are exported as values so the workbook opens without external dependencies.")

from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter

def build_excel_workbook():
    wb = Workbook()
    ws_dash = wb.active
    ws_dash.title = "Dashboard"

    navy = "142B4A"
    blue = "1F4E78"
    teal = "00A6A6"
    light_blue = "D9EAF7"
    light_grey = "F2F5F8"
    white = "FFFFFF"
    green = "E2F0D9"
    red = "FCE4D6"
    thin_grey = Side(style="thin", color="D9E1F2")

    def write_df(sheet_name, df, title):
        ws = wb.create_sheet(sheet_name)
        ws.sheet_view.showGridLines = False
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(1, len(df.columns)))
        cell = ws.cell(1, 1, title)
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.font = Font(name="Aptos Display", size=16, bold=True, color=white)
        cell.alignment = Alignment(vertical="center")
        ws.row_dimensions[1].height = 28
        for j, col in enumerate(df.columns, 1):
            c = ws.cell(3, j, str(col))
            c.fill = PatternFill("solid", fgColor=blue)
            c.font = Font(bold=True, color=white)
            c.alignment = Alignment(wrap_text=True, vertical="center")
        for i, row in enumerate(df.itertuples(index=False, name=None), 4):
            for j, val in enumerate(row, 1):
                if pd.isna(val):
                    val = None
                c = ws.cell(i, j, val.item() if hasattr(val, "item") else val)
                c.border = Border(bottom=thin_grey)
                if isinstance(val, (int, float, np.number)) and j > 1:
                    c.number_format = '₹#,##0.00;[Red](₹#,##0.00);-'
                if i % 2 == 0:
                    c.fill = PatternFill("solid", fgColor=light_grey)
        ws.freeze_panes = "A4"
        ws.auto_filter.ref = f"A3:{get_column_letter(len(df.columns))}{len(df)+3}"
        for j, col in enumerate(df.columns, 1):
            values = [len(str(col))] + [len(str(x)) for x in df[col].head(100)]
            ws.column_dimensions[get_column_letter(j)].width = min(max(max(values) + 3, 14), 32)
        return ws

    # Dashboard front page
    ws_dash.sheet_view.showGridLines = False
    ws_dash.merge_cells("A1:H1")
    ws_dash["A1"] = "BOOMER | FINANCIAL COMMAND CENTRE"
    ws_dash["A1"].font = Font(name="Aptos Display", size=20, bold=True, color=white)
    ws_dash["A1"].fill = PatternFill("solid", fgColor=navy)
    ws_dash["A1"].alignment = Alignment(vertical="center")
    ws_dash.row_dimensions[1].height = 36
    ws_dash.merge_cells("A2:H2")
    ws_dash["A2"] = "Integrated three-statement model • Advanced cash flow • INR"
    ws_dash["A2"].font = Font(italic=True, color="64748B")
    kpis = [
        ("Target annual units", target_units),
        ("Pilot units", pilot_units),
        ("Latest forecast revenue", float(forecast.iloc[-1]["Company net revenue"])),
        ("Latest EBITDA", float(forecast.iloc[-1]["EBITDA"])),
        ("Latest net profit", float(forecast.iloc[-1]["Net profit"])),
        ("Latest closing cash", float(balance_sheet.iloc[-1]["Cash"])),
        ("Latest debt", float(balance_sheet.iloc[-1]["Debt"])),
        ("Balance sheet check", float(balance_sheet.iloc[-1]["Balance check (should be 0)"]))
    ]
    for idx, (label, value) in enumerate(kpis):
        row = 4 + (idx // 4) * 3
        col = 1 + (idx % 4) * 2
        ws_dash.cell(row, col, label).font = Font(bold=True, color=white)
        ws_dash.cell(row, col).fill = PatternFill("solid", fgColor=blue)
        ws_dash.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
        ws_dash.cell(row+1, col, value)
        ws_dash.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+1)
        ws_dash.cell(row+1, col).font = Font(size=14, bold=True, color=navy)
        ws_dash.cell(row+1, col).number_format = '#,##0.00;[Red](#,##0.00);-'
        ws_dash.cell(row+1, col).fill = PatternFill("solid", fgColor=green if label != "Balance sheet check" else light_blue)
    ws_dash.column_dimensions["A"].width = 24
    for col in "BCDEFGH":
        ws_dash.column_dimensions[col].width = 16
    ws_dash.freeze_panes = "A4"

    # Assumptions schedule
    assumptions_df = pd.DataFrame({
        "Assumption": ["Target type", "Annual target (₹ crore)", "Projection years", "Weighted average MRP / unit", "GST rate", "Retailer margin", "Distributor margin", "Manufacturing cost / unit", "Variable selling cost / unit", "Operating expenses %", "Depreciation %", "Interest %", "Tax rate", "Opening cash", "Opening share capital", "Receivable days", "Inventory days", "Payable days", "Capex % revenue", "Debt raised % revenue", "Debt repayment % opening debt", "Annual equity raise"],
        "Value": [target_type, target_sales_cr, projection_years, avg_mrp, gst_rate, retailer_margin, distributor_margin, manufacturing_cost, variable_selling_cost, opex_percent, depreciation_percent, interest_percent, tax_rate, opening_cash, opening_share_capital, receivable_days, inventory_days, payable_days, capex_percent, debt_draw_percent, debt_repayment_percent, equity_raise]
    })
    write_df("Assumptions", assumptions_df, "BOOMER | MODEL ASSUMPTIONS")
    write_df("Income Statement", income_statement, "BOOMER | INCOME STATEMENT")
    write_df("Balance Sheet", balance_sheet, "BOOMER | BALANCE SHEET")
    write_df("Cash Flow", cash_flow, "BOOMER | CASH FLOW STATEMENT")
    write_df("Working Capital", working_capital, "BOOMER | WORKING CAPITAL")
    write_df("Annual Forecast", forecast, "BOOMER | ANNUAL OPERATING FORECAST")
    write_df("Pilot SKU", sku_data, "BOOMER | PILOT SKU ECONOMICS")
    write_df("Milestones", milestone_df, "BOOMER | EXPANSION MILESTONES")

    # Native Excel charts on a dedicated chart page.
    ws_charts = wb.create_sheet("Charts")
    ws_charts.sheet_view.showGridLines = False
    ws_charts["A1"] = "BOOMER | FINANCIAL CHARTS"
    ws_charts["A1"].font = Font(size=18, bold=True, color=white)
    ws_charts["A1"].fill = PatternFill("solid", fgColor=navy)

    def add_chart_data(sheet_name, categories_col, data_cols, title, anchor, chart_type="line"):
        data_ws = wb[sheet_name]
        chart = LineChart() if chart_type == "line" else BarChart()
        chart.title = title
        chart.style = 13
        chart.height = 8
        chart.width = 16
        chart.y_axis.title = "INR"
        chart.x_axis.title = "Year"
        for col_idx in data_cols:
            data = Reference(data_ws, min_col=col_idx, max_col=col_idx, min_row=3, max_row=len(forecast)+3)
            chart.add_data(data, titles_from_data=True)
        cats = Reference(data_ws, min_col=categories_col, min_row=4, max_row=len(forecast)+3)
        chart.set_categories(cats)
        chart.legend.position = "b"
        ws_charts.add_chart(chart, anchor)

    add_chart_data("Annual Forecast", 1, [5, 10, 15], "Revenue, EBITDA & Net Profit", "A3", "line")
    add_chart_data("Cash Flow", 1, [5, 7, 11], "Operating, Investing & Financing Cash Flow", "A20", "bar")
    add_chart_data("Balance Sheet", 1, [2, 6, 13], "Cash, Total Assets & Total Liabilities and Equity", "J3", "line")

    # Add model notes to dashboard.
    ws_dash["A11"] = "MODEL NOTES"
    ws_dash["A11"].font = Font(bold=True, color=white)
    ws_dash["A11"].fill = PatternFill("solid", fgColor=blue)
    ws_dash.merge_cells("A11:H11")
    ws_dash.merge_cells("A12:H14")
    ws_dash["A12"] = ("Illustrative management forecast only. Revenue, channel deductions, GST, tax, working capital, "
                      "debt, capex and financing are driven by editable assumptions in the Streamlit app. "
                      "The exported workbook contains schedules and charts; update assumptions in the app and re-export.")
    ws_dash["A12"].alignment = Alignment(wrap_text=True, vertical="top")
    ws_dash["A12"].fill = PatternFill("solid", fgColor=light_grey)
    ws_dash["A12"].font = Font(color="334155")

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()

excel_file = build_excel_workbook()
st.download_button(
    label="⬇ Download complete BOOMER financial model (Excel)",
    data=excel_file,
    file_name="BOOMER_Integrated_Three_Statement_Model.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.download_button(
    label="⬇ Download annual forecast (CSV)",
    data=forecast.to_csv(index=False).encode("utf-8"),
    file_name="BOOMER_Annual_Forecast.csv",
    mime="text/csv"
)

# ---------------------- NOTES -----------------------------

st.divider()

st.subheader("Important financial notes")

st.markdown("""
- This is a planning dashboard, not audited accounting software.
- GST and channel deductions are simplified assumptions.
- Net revenue is not the same as consumer MRP sales.
- EBITDA is not cash flow or net profit.
- The forecast does not automatically fund inventory or expansion.
- The factory calculator excludes many operating and financing costs.
- Validate tax, GST, legal, product and export requirements with
  qualified professionals before making business decisions.
""")

st.caption("BOOMER | Build demand first. Scale supply second.")
