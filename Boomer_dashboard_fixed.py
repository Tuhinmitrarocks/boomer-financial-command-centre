
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# BOOMER FINANCIAL COMMAND CENTRE
# Illustrative planning model - INR
# =========================================================

st.set_page_config(
    page_title="BOOMER Financial Command Centre",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM COMMAND-CENTRE THEME ----------------
st.markdown("""
<style>
:root { --boomer-navy:#0b1b32; --boomer-blue:#1769d2; --boomer-bg:#f4f7fb; --boomer-ink:#14243a; }
[data-testid="stAppViewContainer"] { background:var(--boomer-bg); color:var(--boomer-ink); }
[data-testid="stHeader"] { background:rgba(244,247,251,.94); }
[data-testid="stSidebar"] { background:var(--boomer-navy); border-right:1px solid #203957; }
[data-testid="stSidebar"] * { color:#edf4ff !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input { background:#142b49 !important; border-color:#39516e !important; }
.block-container { padding-top:1.7rem; padding-bottom:3rem; max-width:1500px; }
h1,h2,h3 { color:#14243a !important; letter-spacing:-.025em; }
[data-testid="stMetric"] { background:#fff; border:1px solid #d9e3ef; border-radius:13px; padding:17px 18px; box-shadow:0 3px 12px rgba(20,43,74,.06); min-height:112px; }
[data-testid="stMetricLabel"] { color:#53657b !important; font-weight:650; }
[data-testid="stMetricValue"] { color:var(--boomer-blue) !important; font-weight:750; }
[data-testid="stAlert"] { border-radius:11px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { background:#fff; border:1px solid #dce5ef; border-radius:12px; overflow:hidden; }
[data-testid="stPlotlyChart"] { background:#fff; border:1px solid #dce5ef; border-radius:13px; padding:8px; box-shadow:0 3px 12px rgba(20,43,74,.04); }
[data-testid="stDownloadButton"] button, .stButton button { border-radius:9px; font-weight:650; }
hr { border-color:#dce5ef; }
.boomer-hero { background:linear-gradient(115deg,#0b1b32 0%,#173e70 68%,#1769d2 100%); padding:25px 28px; border-radius:16px; margin:0 0 20px 0; box-shadow:0 8px 24px rgba(11,27,50,.16); }
.boomer-hero h1 { color:#fff !important; margin:0 0 6px 0; font-size:2rem; }
.boomer-hero p { color:#d8e7fa; margin:0; font-size:.96rem; }
.boomer-kicker { color:#8fc3ff; font-size:.76rem; font-weight:750; letter-spacing:.13em; text-transform:uppercase; margin-bottom:8px; }
</style>
<div class="boomer-hero">
  <div class="boomer-kicker">FMCG • Financial Planning & Analysis</div>
  <h1>🧴 BOOMER | Financial Command Centre</h1>
  <p>From 3,000-unit market experiment to ₹500 crore annual sales. All figures are planning assumptions, not guaranteed results.</p>
</div>
""", unsafe_allow_html=True)

# Render the HTML brand block separately from Markdown navigation.
# Mixing raw HTML and Markdown in one block can cause Streamlit to display
# the entire sidebar content as literal text.
st.sidebar.markdown(
    """
    <div style="padding:8px 0 16px 0">
      <div style="font-size:1.35rem;font-weight:800;letter-spacing:.04em;color:#ffffff">🧴 BOOMER</div>
      <div style="font-size:.68rem;color:#9eb8d6;letter-spacing:.13em">FINANCIAL COMMAND CENTRE</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    ### NAVIGATION

    - [Executive Dashboard](#business-overview)
    - [Financial Statements](#6-integrated-three-statement-model)
    - [Product Analytics](#8-product-master-and-product-wise-profitability)
    - [Forecasting & Scenarios](#9-forecasting-frequency-and-scenario-comparison)
    - [Working Capital](#working-capital-schedule)
    - [Expansion & CapEx](#12-expansion-factory-export-and-uae-investment-plan)
    - [SQL Database](#10-sql-database)
    - [Power BI & Tableau](#11-power-bi-and-tableau-data-exports)
    - [Excel Export](#7-download-professional-excel-financial-model)
    """
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
opening_retained_earnings = st.sidebar.number_input("Opening retained earnings (₹)", value=0.0, step=50000.0)
opening_ar = st.sidebar.number_input("Opening accounts receivable (₹)", min_value=0.0, value=0.0, step=25000.0)
opening_inventory = st.sidebar.number_input("Opening inventory (₹)", min_value=0.0, value=0.0, step=25000.0)
opening_ap = st.sidebar.number_input("Opening accounts payable (₹)", min_value=0.0, value=0.0, step=25000.0)
opening_ppe = st.sidebar.number_input("Opening net PP&E (₹)", min_value=0.0, value=0.0, step=50000.0)
opening_debt = st.sidebar.number_input("Opening debt (₹)", min_value=0.0, value=0.0, step=50000.0)
receivable_days = st.sidebar.number_input("Receivable days (DSO)", min_value=0.0, max_value=180.0, value=30.0, step=5.0)
inventory_days = st.sidebar.number_input("Inventory days", min_value=0.0, max_value=365.0, value=45.0, step=5.0)
payable_days = st.sidebar.number_input("Payable days (DPO)", min_value=0.0, max_value=180.0, value=30.0, step=5.0)
capex_percent = st.sidebar.number_input("Annual capital expenditure (% of revenue)", min_value=0.0, max_value=50.0, value=3.0, step=0.5) / 100
debt_draw_percent = st.sidebar.number_input("New debt raised (% of revenue)", min_value=0.0, max_value=50.0, value=0.0, step=0.5) / 100
debt_repayment_percent = st.sidebar.number_input("Annual debt repayment (% of opening debt)", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100
equity_raise = st.sidebar.number_input("Additional equity raised each year (₹)", min_value=0.0, value=0.0, step=100000.0)
st.sidebar.caption(
    "Opening balances should reconcile: cash + receivables + inventory + net PP&E "
    "must equal payables + debt + share capital + retained earnings."
)

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

st.subheader("Executive financial overview")

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
        max(1, target_units),
        projection_years
    ).round().astype(int)

forecast_rows = []
forecast_opening_ppe = float(opening_ppe)

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

    planned_capex = net_revenue * capex_percent
    planned_depreciation = net_revenue * depreciation_percent
    # Depreciation cannot exceed the available net asset base (opening PP&E + current-year CapEx).
    depreciation = min(planned_depreciation, max(0.0, forecast_opening_ppe + planned_capex))
    forecast_opening_ppe = max(0.0, forecast_opening_ppe + planned_capex - depreciation)
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

fig.update_layout(
    template="plotly_white",
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Arial, sans-serif", size=13, color="#24364b"),
    title=dict(font=dict(size=18, color="#14243a")),
    legend=dict(font=dict(size=12, color="#24364b"), title_text=""),
    margin=dict(l=35, r=25, t=65, b=45),
    hoverlabel=dict(bgcolor="#142b49", font=dict(color="#ffffff", size=12))
)
fig.update_xaxes(
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155", size=13),
    showgrid=False,
    zeroline=False,
    linecolor="#94a3b8"
)
fig.update_yaxes(
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155", size=13),
    gridcolor="#e5eaf1",
    zerolinecolor="#cbd5e1",
    linecolor="#94a3b8"
)
st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "responsive": True})

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

fig2.update_layout(
    template="plotly_white",
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Arial, sans-serif", size=13, color="#24364b"),
    title=dict(font=dict(size=18, color="#14243a")),
    legend=dict(font=dict(size=12, color="#24364b"), title_text=""),
    margin=dict(l=35, r=25, t=65, b=45),
    hoverlabel=dict(bgcolor="#142b49", font=dict(color="#ffffff", size=12))
)
fig2.update_xaxes(
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155", size=13),
    showgrid=False,
    zeroline=False,
    linecolor="#94a3b8"
)
fig2.update_yaxes(
    tickfont=dict(color="#334155", size=12),
    title_font=dict(color="#334155", size=13),
    gridcolor="#e5eaf1",
    zerolinecolor="#cbd5e1",
    linecolor="#94a3b8"
)
st.plotly_chart(fig2, use_container_width=True, config={"displaylogo": False, "responsive": True})

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

prior_ar = float(opening_ar)
prior_inventory = float(opening_inventory)
prior_ap = float(opening_ap)
prior_ppe = float(opening_ppe)
prior_debt = float(opening_debt)
cash = float(opening_cash)
share_capital = float(opening_share_capital)
retained_earnings = float(opening_retained_earnings)

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
        "Assumption": ["Target type", "Annual target (₹ crore)", "Projection years", "Weighted average MRP / unit", "GST rate", "Retailer margin", "Distributor margin", "Manufacturing cost / unit", "Variable selling cost / unit", "Operating expenses %", "Depreciation %", "Interest %", "Tax rate", "Opening cash", "Opening share capital", "Opening retained earnings", "Opening accounts receivable",
                     "Opening inventory", "Opening accounts payable", "Opening net PP&E", "Opening debt", "Receivable days", "Inventory days", "Payable days", "Capex % revenue", "Debt raised % revenue", "Debt repayment % opening debt", "Annual equity raise"],
        "Value": [target_type, target_sales_cr, projection_years, avg_mrp, gst_rate, retailer_margin, distributor_margin, manufacturing_cost, variable_selling_cost, opex_percent, depreciation_percent, interest_percent, tax_rate, opening_cash, opening_share_capital, opening_retained_earnings, opening_ar, opening_inventory,
                 opening_ap, opening_ppe, opening_debt, receivable_days, inventory_days, payable_days, capex_percent, debt_draw_percent, debt_repayment_percent, equity_raise]
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


    # Formula-driven vertical financial schedules (line items down, years across).
    # Source schedules above remain available for backward compatibility.
    def add_vertical_sheet(title, row_labels, source_sheet, source_columns):
        ws = wb.create_sheet(title)
        ws.sheet_view.showGridLines = False
        ws.cell(1, 1, title.upper()).font = Font(size=16, bold=True, color=white)
        ws.cell(1, 1).fill = PatternFill("solid", fgColor=navy)
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=projection_years + 1)
        ws.cell(3, 1, "Financial line item")
        ws.cell(3, 1).font = Font(bold=True, color=white)
        ws.cell(3, 1).fill = PatternFill("solid", fgColor=blue)
        for yr in range(projection_years):
            c = yr + 2
            ws.cell(3, c, f"Year {yr+1}")
            ws.cell(3, c).font = Font(bold=True, color=white)
            ws.cell(3, c).fill = PatternFill("solid", fgColor=blue)
        for ridx, label in enumerate(row_labels, 4):
            ws.cell(ridx, 1, label).font = Font(bold=True, color=navy)
            source_col = source_columns.get(label)
            for yr in range(projection_years):
                if source_col:
                    # Annual Forecast and statements are exported with headers on row 3 and data from row 4.
                    ws.cell(ridx, yr + 2, f"='{source_sheet}'!{source_col}{yr+4}")
                    ws.cell(ridx, yr + 2).font = Font(color="008000")
                    ws.cell(ridx, yr + 2).number_format = '₹#,##0.00;[Red](₹#,##0.00);-'
        ws.freeze_panes = "B4"
        ws.column_dimensions["A"].width = 34
        for col in range(2, projection_years + 2):
            ws.column_dimensions[get_column_letter(col)].width = 17
        return ws

    vertical_is = add_vertical_sheet(
        "IS Vertical",
        ["Annual units", "Consumer MRP sales", "Company net revenue", "Manufacturing cost",
         "Gross profit", "Variable selling cost", "Operating expenses", "EBITDA",
         "Depreciation", "Interest", "Profit before tax", "Tax", "Net profit"],
        "Annual Forecast",
        {"Annual units":"B", "Consumer MRP sales":"D", "Company net revenue":"E",
         "Manufacturing cost":"F", "Gross profit":"G", "Variable selling cost":"H",
         "Operating expenses":"I", "EBITDA":"J", "Depreciation":"K", "Interest":"L",
         "Profit before tax":"M", "Tax":"N", "Net profit":"O"}
    )

    # Formula-linked balance sheet and cash flow in vertical financial-statement format.
    for sheet_title, labels, source, cols in [
        ("BS Vertical",
         ["Cash", "Accounts receivable", "Inventory", "Net PP&E", "Total assets",
          "Accounts payable", "Debt", "Total liabilities", "Share capital",
          "Retained earnings", "Total equity", "Total liabilities & equity",
          "Balance check"],
         "Balance Sheet",
         {"Cash":"B","Accounts receivable":"C","Inventory":"D","Net PP&E":"E",
          "Total assets":"F","Accounts payable":"G","Debt":"H","Total liabilities":"I",
          "Share capital":"J","Retained earnings":"K","Total equity":"L",
          "Total liabilities & equity":"M","Balance check":"N"}),
        ("CF Vertical",
         ["Net income", "Depreciation & amortisation", "Change in net working capital",
          "Cash flow from operations", "Capital expenditure", "Cash flow from investing",
          "Debt raised", "Debt repayment", "Equity raised", "Cash flow from financing",
          "Net change in cash", "Opening cash", "Closing cash"],
         "Cash Flow",
         {"Net income":"B","Depreciation & amortisation":"C","Change in net working capital":"D",
          "Cash flow from operations":"E","Capital expenditure":"F","Cash flow from investing":"G",
          "Debt raised":"H","Debt repayment":"I","Equity raised":"J","Cash flow from financing":"K",
          "Net change in cash":"L","Opening cash":"M","Closing cash":"N"})
    ]:
        add_vertical_sheet(sheet_title, labels, source, cols)

    # Formula-driven financial ratios.
    ratio_ws = wb.create_sheet("Financial Ratios")
    ratio_ws.sheet_view.showGridLines = False
    ratio_ws["A1"] = "BOOMER | FINANCIAL RATIOS"
    ratio_ws["A1"].font = Font(size=16, bold=True, color=white)
    ratio_ws["A1"].fill = PatternFill("solid", fgColor=navy)
    ratio_ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=projection_years+1)
    ratio_labels = ["Gross margin", "EBITDA margin", "Net profit margin", "Current ratio",
                    "Debt-to-equity", "ROE", "ROA"]
    ratio_ws["A3"] = "Ratio"
    for yr in range(projection_years):
        ratio_ws.cell(3, yr+2, f"Year {yr+1}")
    for c in range(1, projection_years+2):
        ratio_ws.cell(3,c).font = Font(bold=True,color=white)
        ratio_ws.cell(3,c).fill = PatternFill("solid",fgColor=blue)
    for ri, label in enumerate(ratio_labels,4):
        ratio_ws.cell(ri,1,label)
        for yr in range(projection_years):
            col = get_column_letter(yr+2)
            iscol = get_column_letter(yr+2)
            bscol = get_column_letter(yr+2)
            formulas = {
                "Gross margin": f"=IFERROR('IS Vertical'!{iscol}8/'IS Vertical'!{iscol}6,0)",
                "EBITDA margin": f"=IFERROR('IS Vertical'!{iscol}11/'IS Vertical'!{iscol}6,0)",
                "Net profit margin": f"=IFERROR('IS Vertical'!{iscol}16/'IS Vertical'!{iscol}6,0)",
                "Current ratio": f"=IFERROR(('BS Vertical'!{bscol}4+'BS Vertical'!{bscol}5+'BS Vertical'!{bscol}6)/'BS Vertical'!{bscol}9,0)",
                "Debt-to-equity": f"=IFERROR('BS Vertical'!{bscol}10/'BS Vertical'!{bscol}14,0)",
                "ROE": f"=IFERROR('IS Vertical'!{iscol}16/'BS Vertical'!{bscol}14,0)",
                "ROA": f"=IFERROR('IS Vertical'!{iscol}16/'BS Vertical'!{bscol}8,0)"
            }
            ratio_ws.cell(ri,yr+2,formulas[label]).font = Font(color="000000")
            ratio_ws.cell(ri,yr+2).number_format = "0.0%"
            if label in ("Current ratio","Debt-to-equity"):
                ratio_ws.cell(ri,yr+2).number_format = "0.00x"
    ratio_ws.column_dimensions["A"].width=28
    for col in range(2,projection_years+2):
        ratio_ws.column_dimensions[get_column_letter(col)].width=16
    ratio_ws.freeze_panes="B4"

    # Product master and profitability sheets (values are sourced from the live editor).
    product_ws = write_df("Product Master", sku_data, "BOOMER | PRODUCT MASTER")
    product_profit_df = sku_data.copy()
    product_profit_df["Estimated company revenue"] = (
        product_profit_df["Pilot units"] * product_profit_df["MRP per unit"]
        / (1 + gst_rate) * (1-retailer_margin) * (1-distributor_margin)
    )
    product_profit_df["Gross profit"] = (
        product_profit_df["Estimated company revenue"] -
        product_profit_df["Manufacturing expenditure"]
    )
    product_profit_df["Contribution"] = (
        product_profit_df["Gross profit"] -
        product_profit_df["Pilot units"] * variable_selling_cost
    )
    write_df("Product Profitability", product_profit_df, "BOOMER | PRODUCT PROFITABILITY")

    # Embed approved local product renders when present; never insert external image links.
    from pathlib import Path
    from openpyxl.drawing.image import Image as XLImage
    product_asset_dir = Path(__file__).resolve().parent / "assets" / "products"
    for sheet_name in ["Product Master", "Product Profitability"]:
        image_ws = wb[sheet_name]
        image_col = len(sku_data.columns) + 1
        image_ws.cell(3, image_col, "Embedded product image")
        image_ws.cell(3, image_col).font = Font(bold=True, color=white)
        image_ws.cell(3, image_col).fill = PatternFill("solid", fgColor=blue)
        image_ws.column_dimensions[get_column_letter(image_col)].width = 20
        for row_num, product_name in enumerate(sku_data["Product"].astype(str), start=4):
            image_name = product_name.lower().replace(" ", "_") + ".png"
            image_path = product_asset_dir / image_name
            if image_path.exists():
                try:
                    xl_image = XLImage(str(image_path))
                    xl_image.width, xl_image.height = 100, 85
                    image_ws.add_image(xl_image, f"{get_column_letter(image_col)}{row_num}")
                    image_ws.row_dimensions[row_num].height = 68
                except Exception:
                    image_ws.cell(row_num, image_col, "Image could not be embedded")
            else:
                image_ws.cell(row_num, image_col, "Awaiting approved PNG")
    # Optional thumbnails on the executive dashboard.
    for idx, product_name in enumerate(sku_data["Product"].astype(str), start=4):
        image_path = product_asset_dir / (product_name.lower().replace(" ", "_") + ".png")
        if image_path.exists():
            try:
                xl_image = XLImage(str(image_path))
                xl_image.width, xl_image.height = 90, 75
                ws_dash.add_image(xl_image, f"J{idx * 3}")
            except Exception:
                pass
    ws_dash.column_dimensions["J"].width = 18

    scenario_rows = []
    for scenario_name, volume_mult, price_mult, cost_mult in [
        ("Pessimistic", 0.80, 0.97, 1.08),
        ("Base", 1.00, 1.00, 1.00),
        ("Optimistic", 1.20, 1.03, 0.97)
    ]:
        for yr, base_row in forecast.iterrows():
            scenario_rows.append({
                "Scenario": scenario_name, "Year": base_row["Year"],
                "Annual units": int(round(base_row["Annual units"] * volume_mult)),
                "Company net revenue": float(base_row["Company net revenue"] * volume_mult * price_mult),
                "EBITDA": float((base_row["EBITDA"] + base_row["Manufacturing cost"] +
                                  base_row["Variable selling cost"]) * volume_mult * price_mult -
                                 (base_row["Manufacturing cost"] + base_row["Variable selling cost"]) *
                                  volume_mult * cost_mult -
                                 base_row["Operating expenses"] * volume_mult * price_mult)
            })
    scenario_df = pd.DataFrame(scenario_rows)
    write_df("Scenario Analysis", scenario_df, "BOOMER | SCENARIO ANALYSIS")

    debt_df = cash_flow[["Year", "Debt raised", "Debt repayment"]].copy()
    debt_df["Closing debt"] = balance_sheet["Debt"].values
    write_df("Debt Schedule", debt_df, "BOOMER | DEBT SCHEDULE")
    capex_df = cash_flow[["Year", "Capital expenditure"]].copy()
    capex_df["Depreciation"] = forecast["Depreciation"].values
    capex_df["Net PP&E"] = balance_sheet["Net PP&E"].values
    write_df("Depreciation & CapEx", capex_df, "BOOMER | DEPRECIATION AND CAPITAL EXPENDITURE")

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"

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


# =========================================================
# 8. ADVANCED PRODUCT ANALYTICS, SCENARIOS, DATA & BI EXPORTS
# =========================================================
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import uuid

st.divider()
st.header("8. Product master and product-wise profitability")
st.caption("Editable product assumptions. Selling prices and manufacturing costs carry forward from the existing SKU pilot; the 36,000-unit Year 1 mix follows the pilot proportions. New packaging, distribution, marketing, fixed-cost and growth inputs start at zero until you supply actual assumptions. Product imagery remains a placeholder until approved BOOMER pack renders are supplied.")

product_seed = pd.DataFrame({
    "Product": ["Dishwashing Liquid", "Fabric Washing Liquid", "Floor Cleaner", "Toilet Cleaner"],
    "Selling price (₹)": [120.0, 280.0, 90.0, 110.0],
    "Manufacturing cost (₹)": [34.0, 34.0, 34.0, 34.0],
    "Packaging cost (₹)": [0.0, 0.0, 0.0, 0.0],
    "Distribution cost (₹)": [0.0, 0.0, 0.0, 0.0],
    "Marketing cost (₹)": [0.0, 0.0, 0.0, 0.0],
    # Pilot mix scaled to the existing 36,000-unit Year 1 planning input.
    "Annual sales units": [12000, 6000, 9000, 9000],
    "Annual unit growth (%)": [0.0, 0.0, 0.0, 0.0],
    "Annual product fixed costs (₹)": [0.0, 0.0, 0.0, 0.0]
})
product_master = st.data_editor(
    product_seed, num_rows="dynamic", use_container_width=True,
    key="boomer_product_master",
    column_config={
        "Selling price (₹)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        "Manufacturing cost (₹)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        "Packaging cost (₹)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        "Distribution cost (₹)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        "Marketing cost (₹)": st.column_config.NumberColumn(min_value=0.0, step=1.0),
        "Annual sales units": st.column_config.NumberColumn(min_value=0, step=500),
        "Annual unit growth (%)": st.column_config.NumberColumn(min_value=-100.0, max_value=500.0, step=1.0),
        "Annual product fixed costs (₹)": st.column_config.NumberColumn(min_value=0.0, step=10000.0)
    }
)
if not product_master.empty:
    pm = product_master.copy()
    numeric_product_cols = ["Selling price (₹)", "Manufacturing cost (₹)", "Packaging cost (₹)",
                            "Distribution cost (₹)", "Marketing cost (₹)", "Annual sales units",
                            "Annual unit growth (%)", "Annual product fixed costs (₹)"]
    for col in numeric_product_cols:
        pm[col] = pd.to_numeric(pm[col], errors="coerce").fillna(0)
    pm["Company realisation / unit (₹)"] = (
        pm["Selling price (₹)"] / (1 + gst_rate) *
        (1-retailer_margin) * (1-distributor_margin)
    )
    pm["Net revenue (₹)"] = pm["Company realisation / unit (₹)"] * pm["Annual sales units"]
    pm["Total variable cost (₹)"] = (
        pm[["Manufacturing cost (₹)", "Packaging cost (₹)", "Distribution cost (₹)",
            "Marketing cost (₹)"]].sum(axis=1) * pm["Annual sales units"]
    )
    pm["Gross profit (₹)"] = pm["Net revenue (₹)"] - (
        pm["Manufacturing cost (₹)"] + pm["Packaging cost (₹)"]
    ) * pm["Annual sales units"]
    pm["Contribution (₹)"] = pm["Net revenue (₹)"] - pm["Total variable cost (₹)"]
    pm["Contribution margin (%)"] = np.where(
        pm["Net revenue (₹)"] != 0, pm["Contribution (₹)"] / pm["Net revenue (₹)"], 0
    )
    pm["EBITDA (₹)"] = pm["Contribution (₹)"] - pm["Annual product fixed costs (₹)"]
    pm["Depreciation and interest allocation (₹)"] = (
        pm["Net revenue (₹)"] * (depreciation_percent + interest_percent)
    )
    pm["Profit before tax (₹)"] = pm["EBITDA (₹)"] - pm["Depreciation and interest allocation (₹)"]
    pm["Illustrative tax (₹)"] = pm["Profit before tax (₹)"].clip(lower=0) * tax_rate
    pm["Illustrative net profit (₹)"] = pm["Profit before tax (₹)"] - pm["Illustrative tax (₹)"]
    unit_contribution = pm["Company realisation / unit (₹)"] - pm[
        ["Manufacturing cost (₹)", "Packaging cost (₹)", "Distribution cost (₹)", "Marketing cost (₹)"]
    ].sum(axis=1)
    pm["Break-even units"] = np.where(
        unit_contribution > 0,
        np.ceil(pm["Annual product fixed costs (₹)"] / unit_contribution),
        np.nan
    )
    st.dataframe(pm, use_container_width=True, hide_index=True)
    st.caption("Break-even units use product-level annual fixed costs divided by unit contribution. Enter realistic fixed costs before relying on this estimate. Product-level marketing costs are separate from the company operating-expense assumption; do not count the same spend twice.")
    product_growth_rows = []
    for _, product_row in pm.iterrows():
        for year_num in range(1, projection_years + 1):
            projected_units = float(product_row["Annual sales units"]) * (
                1 + float(product_row["Annual unit growth (%)"]) / 100
            ) ** (year_num - 1)
            product_growth_rows.append({
                "Product": product_row["Product"], "Year": f"Year {year_num}",
                "Projected units": round(projected_units),
                "Projected net revenue (₹)": projected_units * float(product_row["Company realisation / unit (₹)"]),
                "Projected contribution (₹)": projected_units * (
                    float(product_row["Company realisation / unit (₹)"]) -
                    float(product_row["Manufacturing cost (₹)"]) -
                    float(product_row["Packaging cost (₹)"]) -
                    float(product_row["Distribution cost (₹)"]) -
                    float(product_row["Marketing cost (₹)"])
                )
            })
    product_growth_df = pd.DataFrame(product_growth_rows)
    st.subheader("Product-wise growth projection")
    st.dataframe(product_growth_df, use_container_width=True, hide_index=True)
    pc1, pc2 = st.columns(2)
    with pc1:
        st.plotly_chart(px.bar(pm, x="Product", y="Net revenue (₹)", title="Product-wise net revenue"), use_container_width=True)
    with pc2:
        st.plotly_chart(px.bar(pm, x="Product", y="Contribution (₹)", title="Product-wise contribution"), use_container_width=True)

st.subheader("BOOMER product packaging assets")
asset_dir = Path(__file__).resolve().parent / "assets" / "products" if "__file__" in globals() else Path("assets/products")
asset_specs = [
    ("Dishwashing Liquid", "Green packaging"),
    ("Fabric Washing Liquid", "Distinctive premium packaging"),
    ("Floor Cleaner", "Distinctive premium packaging"),
    ("Toilet Cleaner", "Red angled-neck bottle")
]
asset_cols = st.columns(4)
for col, (product_name, visual_note) in zip(asset_cols, asset_specs):
    with col:
        st.markdown(f"**{product_name}**")
        image_path = asset_dir / (product_name.lower().replace(" ", "_") + ".png")
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.info(f"Image placeholder\n\n{visual_note}\n\nAdd approved transparent PNG at:\n`assets/products/{image_path.name}`")

st.divider()
st.header("9. Forecasting frequency and scenario comparison")
frequency = st.selectbox("Reporting frequency", ["Annual", "Quarterly", "Monthly"], index=0)
historical_upload = st.file_uploader("Optional historical financials CSV", type=["csv"], key="historical_financials")
if historical_upload is not None:
    try:
        historical_df = pd.read_csv(historical_upload)
        st.caption("Historical data supplied by the user; it is kept separate from the illustrative forecast.")
        st.dataframe(historical_df, use_container_width=True)
        st.download_button("Download normalized historical CSV", historical_df.to_csv(index=False).encode("utf-8"),
                           "boomer_historical_financials.csv", "text/csv")
    except Exception as history_error:
        st.error(f"Could not read historical CSV: {history_error}")
scenario_choice = st.selectbox("Scenario to inspect", ["Base Case", "Optimistic Case", "Pessimistic Case"])
scenario_settings = {
    "Base Case": (1.00, 1.00, 1.00),
    "Optimistic Case": (1.20, 1.03, 0.97),
    "Pessimistic Case": (0.80, 0.97, 1.08)
}
volume_factor, price_factor, cost_factor = scenario_settings[scenario_choice]
scenario_output = forecast.copy()
scenario_output["Annual units"] = (scenario_output["Annual units"] * volume_factor).round().astype(int)
scenario_output["Company net revenue"] = scenario_output["Company net revenue"] * volume_factor * price_factor
scenario_output["Consumer MRP sales"] = scenario_output["Consumer MRP sales"] * volume_factor * price_factor
scenario_output["Manufacturing cost"] = scenario_output["Manufacturing cost"] * volume_factor * cost_factor
scenario_output["Variable selling cost"] = scenario_output["Variable selling cost"] * volume_factor * cost_factor
scenario_output["Gross profit"] = scenario_output["Company net revenue"] - scenario_output["Manufacturing cost"]
scenario_output["EBITDA"] = (
    scenario_output["Gross profit"] - scenario_output["Variable selling cost"] -
    scenario_output["Company net revenue"] * opex_percent
)
scenario_output["Depreciation"] = scenario_output["Company net revenue"] * depreciation_percent
scenario_output["Interest"] = scenario_output["Company net revenue"] * interest_percent
scenario_output["Profit before tax"] = scenario_output["EBITDA"] - scenario_output["Depreciation"] - scenario_output["Interest"]
scenario_output["Tax"] = scenario_output["Profit before tax"].clip(lower=0) * tax_rate
scenario_output["Net profit"] = scenario_output["Profit before tax"] - scenario_output["Tax"]
scenario_output["Scenario"] = scenario_choice

if frequency == "Annual":
    frequency_view = scenario_output.copy()
elif frequency == "Quarterly":
    frequency_view = scenario_output.loc[scenario_output.index.repeat(4)].copy()
    frequency_view["Period"] = [f"{y} Q{q}" for y in scenario_output["Year"] for q in range(1, 5)]
    for metric in ["Annual units", "Consumer MRP sales", "Company net revenue", "Manufacturing cost",
                   "Gross profit", "Variable selling cost", "Operating expenses", "EBITDA",
                   "Depreciation", "Interest", "Profit before tax", "Tax", "Net profit"]:
        frequency_view[metric] = frequency_view[metric] / 4
else:
    frequency_view = scenario_output.loc[scenario_output.index.repeat(12)].copy()
    frequency_view["Period"] = [f"{y} M{m:02d}" for y in scenario_output["Year"] for m in range(1, 13)]
    for metric in ["Annual units", "Consumer MRP sales", "Company net revenue", "Manufacturing cost",
                   "Gross profit", "Variable selling cost", "Operating expenses", "EBITDA",
                   "Depreciation", "Interest", "Profit before tax", "Tax", "Net profit"]:
        frequency_view[metric] = frequency_view[metric] / 12
st.caption("Quarterly and monthly views evenly allocate annual projections; no seasonality or monthly ramp has been assumed.")
st.dataframe(frequency_view, use_container_width=True, hide_index=True)
scenario_comparison_rows = []
for name, (vf, pf, cf) in scenario_settings.items():
    rev = float(forecast.iloc[-1]["Company net revenue"]) * vf * pf
    cogs = float(forecast.iloc[-1]["Manufacturing cost"]) * vf * cf
    variable = float(forecast.iloc[-1]["Variable selling cost"]) * vf * cf
    opex = rev * opex_percent
    ebitda_s = rev - cogs - variable - opex
    pbt_s = ebitda_s - rev * (depreciation_percent + interest_percent)
    np_s = pbt_s - max(0, pbt_s * tax_rate)
    scenario_comparison_rows.append({"Scenario": name, "Revenue": rev, "EBITDA": ebitda_s, "Net profit": np_s})
scenario_comparison = pd.DataFrame(scenario_comparison_rows)
st.plotly_chart(px.bar(scenario_comparison, x="Scenario", y=["Revenue", "EBITDA", "Net profit"],
                       barmode="group", title="Scenario comparison — final forecast year"), use_container_width=True)

st.divider()
st.header("10. SQL database")
st.caption("PostgreSQL is optional. Without DATABASE_URL or Streamlit secrets, the application remains in demo mode and does not attempt a network connection.")
database_url = os.getenv("DATABASE_URL", "")
try:
    if not database_url and hasattr(st, "secrets"):
        database_url = st.secrets.get("DATABASE_URL", "")
        if not database_url:
            database_url = st.secrets.get("database", {}).get("url", "")
except Exception:
    database_url = database_url or ""

if database_url.startswith("postgres://"):
    database_url = "postgresql+psycopg://" + database_url[len("postgres://"):]
elif database_url.startswith("postgresql://"):
    database_url = "postgresql+psycopg://" + database_url[len("postgresql://"):]

db_engine = None
if database_url:
    try:
        from sqlalchemy import create_engine, text as sql_text
        db_engine = create_engine(database_url, pool_pre_ping=True, future=True)
        with db_engine.begin() as conn:
            conn.execute(sql_text("""
                CREATE TABLE IF NOT EXISTS boomer_model_runs (
                    run_id VARCHAR(36) PRIMARY KEY,
                    model_version VARCHAR(30) NOT NULL,
                    scenario VARCHAR(40) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL,
                    assumptions JSONB NOT NULL,
                    kpis JSONB NOT NULL
                )
            """))
            conn.execute(sql_text("""
                CREATE TABLE IF NOT EXISTS boomer_products (
                    product_id BIGSERIAL PRIMARY KEY,
                    product_name TEXT UNIQUE NOT NULL,
                    product_data JSONB NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """))
            conn.execute(sql_text("""
                CREATE TABLE IF NOT EXISTS boomer_period_financials (
                    run_id VARCHAR(36) NOT NULL REFERENCES boomer_model_runs(run_id),
                    period_label TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    amount NUMERIC(20,2) NOT NULL,
                    PRIMARY KEY (run_id, period_label, frequency, metric_name)
                )
            """))
        st.success("PostgreSQL connection successful; core tables are available.")
    except Exception as db_error:
        st.error(f"Database connection failed ({type(db_error).__name__}). The app remains usable in demo mode. Check the server-side connection configuration.")
        db_engine = None
else:
    st.info("Demo mode: configure DATABASE_URL or [database].url in Streamlit secrets to enable PostgreSQL.")

if st.button("Save current model run to PostgreSQL", disabled=(db_engine is None or forecast.empty)):
    try:
        from sqlalchemy import text as sql_text
        run_id = str(uuid.uuid4())
        assumptions_payload = {
            "target_type": target_type, "target_sales_cr": target_sales_cr,
            "projection_years": projection_years, "avg_mrp": avg_mrp,
            "gst_rate": gst_rate, "retailer_margin": retailer_margin,
            "distributor_margin": distributor_margin, "manufacturing_cost": manufacturing_cost,
            "variable_selling_cost": variable_selling_cost, "opex_percent": opex_percent,
            "tax_rate": tax_rate, "opening_ppe": opening_ppe, "opening_debt": opening_debt,
            "opening_retained_earnings": opening_retained_earnings, "opening_ar": opening_ar,
            "opening_inventory": opening_inventory, "opening_ap": opening_ap,
            "receivable_days": receivable_days,
            "inventory_days": inventory_days, "payable_days": payable_days
        }
        kpis_payload = {
            "latest_revenue": float(forecast.iloc[-1]["Company net revenue"]),
            "latest_ebitda": float(forecast.iloc[-1]["EBITDA"]),
            "latest_net_profit": float(forecast.iloc[-1]["Net profit"])
        }
        with db_engine.begin() as conn:
            conn.execute(sql_text("""
                INSERT INTO boomer_model_runs
                (run_id, model_version, scenario, created_at, assumptions, kpis)
                VALUES (:run_id, :version, :scenario, :created_at, CAST(:assumptions AS JSONB), CAST(:kpis AS JSONB))
            """), {"run_id": run_id, "version": "2.0.0", "scenario": scenario_choice,
                  "created_at": datetime.now(timezone.utc),
                  "assumptions": json.dumps(assumptions_payload), "kpis": json.dumps(kpis_payload)})
            schedule_frames = {
                "Forecast": forecast, "Income Statement": income_statement,
                "Balance Sheet": balance_sheet, "Cash Flow": cash_flow,
                "Working Capital": working_capital, "Selected Scenario": scenario_output,
                "Selected frequency": frequency_view
            }
            for schedule_name, schedule_df in schedule_frames.items():
                for _, schedule_row in schedule_df.iterrows():
                    period_label = str(schedule_row.get("Period", schedule_row.get("Year", "Unlabelled period")))
                    period_frequency = frequency if schedule_name == "Selected frequency" else "Annual"
                    for metric_name, metric_value in schedule_row.items():
                        if metric_name == "Year" or pd.isna(metric_value):
                            continue
                        if isinstance(metric_value, (int, float, np.number)):
                            conn.execute(sql_text("""
                                INSERT INTO boomer_period_financials
                                (run_id, period_label, frequency, metric_name, amount)
                                VALUES (:run_id, :period, :frequency, :metric, :amount)
                            """), {"run_id": run_id, "period": period_label,
                                  "frequency": period_frequency,
                                  "metric": f"{schedule_name} | {metric_name}",
                                  "amount": float(metric_value)})
            if not product_master.empty:
                for _, row in product_master.iterrows():
                    conn.execute(sql_text("""
                        INSERT INTO boomer_products (product_name, product_data, updated_at)
                        VALUES (:name, CAST(:data AS JSONB), NOW())
                        ON CONFLICT (product_name) DO UPDATE
                        SET product_data = EXCLUDED.product_data, updated_at = NOW()
                    """), {"name": str(row["Product"]), "data": json.dumps(row.to_dict(), default=str)})
        st.success(f"Saved model run {run_id}.")
    except Exception as db_error:
        st.error(f"Could not save model run ({type(db_error).__name__}). Check database configuration and server logs.")

if db_engine is not None and st.button("Load recent saved model runs"):
    try:
        from sqlalchemy import text as sql_text
        with db_engine.connect() as conn:
            recent_runs = pd.read_sql(
                sql_text("""
                    SELECT run_id, model_version, scenario, created_at, kpis
                    FROM boomer_model_runs
                    ORDER BY created_at DESC
                    LIMIT 25
                """), conn
            )
        st.dataframe(recent_runs, use_container_width=True, hide_index=True)
    except Exception as db_error:
        st.error(f"Could not retrieve saved runs ({type(db_error).__name__}). Check database configuration and server logs.")

st.divider()
st.header("11. Power BI and Tableau data exports")
bi_financial = forecast.copy()
bi_financial.insert(0, "Model version", "2.0.0")
bi_financial.insert(1, "Scenario", "Base Case")
bi_product = pm.copy() if "pm" in locals() else product_master.copy()
bi_scenario = scenario_comparison.copy()
bi_kpis = pd.DataFrame([
    {"KPI": "Latest company net revenue", "Value": float(forecast.iloc[-1]["Company net revenue"]), "Unit": "INR"},
    {"KPI": "Latest EBITDA", "Value": float(forecast.iloc[-1]["EBITDA"]), "Unit": "INR"},
    {"KPI": "Latest net profit", "Value": float(forecast.iloc[-1]["Net profit"]), "Unit": "INR"},
    {"KPI": "Target annual units", "Value": int(target_units), "Unit": "Units"}
])
export_a, export_b, export_c, export_d = st.columns(4)
with export_a:
    st.download_button("Power BI dataset (CSV)", bi_financial.to_csv(index=False).encode("utf-8"),
                       "boomer_powerbi_financials.csv", "text/csv", use_container_width=True)
with export_b:
    st.download_button("Tableau dataset (CSV)", bi_product.to_csv(index=False).encode("utf-8"),
                       "boomer_tableau_products.csv", "text/csv", use_container_width=True)
with export_c:
    st.download_button("KPI dataset (CSV)", bi_kpis.to_csv(index=False).encode("utf-8"),
                       "boomer_kpis.csv", "text/csv", use_container_width=True)
with export_d:
    st.download_button("Scenario dataset (CSV)", bi_scenario.to_csv(index=False).encode("utf-8"),
                       "boomer_scenarios.csv", "text/csv", use_container_width=True)

schema_path = Path(__file__).resolve().parent / "boomer_schema.sql"
if schema_path.exists():
    st.download_button("Download SQL schema and BI views", schema_path.read_bytes(),
                       "boomer_schema.sql", "application/sql")
st.caption("These are BI-ready datasets, not generated Power BI PBIX or Tableau workbook files. Tableau Hyper export is not enabled; install the Tableau Hyper API and add an approved deployment workflow if a .hyper extract is required.")

st.divider()
st.header("12. Expansion, factory, export and UAE investment plan")
st.caption("Editable strategic investment model. Returns are simple pre-tax planning estimates, not a discounted cash-flow valuation or investment recommendation.")
expansion_years = st.number_input("Expansion evaluation horizon (years)", min_value=1, max_value=30, value=10, step=1)
exp_capacity_units = st.number_input("Planned annual manufacturing capacity (units)", min_value=0, value=int(annual_factory_volume), step=100000)
e1, e2, e3 = st.columns(3)
with e1:
    exp_factory = st.number_input("Factory setup cost (₹ crore)", min_value=0.0, value=float(factory_capex / 1e7), step=0.25)
    exp_machinery = st.number_input("Machinery and equipment (₹ crore)", min_value=0.0, value=0.0, step=0.25)
with e2:
    exp_land = st.number_input("Land and infrastructure (₹ crore)", min_value=0.0, value=0.0, step=0.25)
    exp_export_setup = st.number_input("Export market setup (₹ crore)", min_value=0.0, value=0.0, step=0.10)
with e3:
    exp_uae_setup = st.number_input("UAE setup expenses (₹ crore)", min_value=0.0, value=0.0, step=0.10)
    exp_working_capital = st.number_input("Initial expansion working capital (₹ crore)", min_value=0.0, value=0.0, step=0.10)

st.subheader("Annual operating impact")
b1, b2, b3, b4 = st.columns(4)
with b1:
    exp_operating_benefit = st.number_input(
        "Annual incremental operating benefit (₹ crore)", min_value=0.0,
        value=float(annual_saving / 1e7), step=0.10
    )
with b2:
    exp_employee_cost = st.number_input("Annual employee costs (₹ crore)", min_value=0.0, value=0.0, step=0.10)
with b3:
    exp_export_cost = st.number_input("Annual export operating costs (₹ crore)", min_value=0.0, value=0.0, step=0.10)
with b4:
    exp_uae_cost = st.number_input("Annual UAE operating costs (₹ crore)", min_value=0.0, value=0.0, step=0.10)

exp_total_capex = exp_factory + exp_machinery + exp_land + exp_export_setup + exp_uae_setup
exp_total_investment = exp_total_capex + exp_working_capital
exp_annual_net_benefit = exp_operating_benefit - exp_employee_cost - exp_export_cost - exp_uae_cost
exp_total_benefit = exp_annual_net_benefit * expansion_years
exp_roi = ((exp_total_benefit + exp_working_capital - exp_total_investment) / exp_total_investment
           if exp_total_investment > 0 else None)
exp_payback = (exp_total_investment / exp_annual_net_benefit
               if exp_annual_net_benefit > 0 else None)

# Bisection IRR for one initial investment, equal annual cash benefits and working-capital recovery at exit.
exp_cashflows = [-exp_total_investment] + [exp_annual_net_benefit] * expansion_years
if expansion_years > 0 and exp_working_capital > 0:
    exp_cashflows[-1] += exp_working_capital

def _npv_for_rate(rate, cashflows):
    return sum(cf / ((1 + rate) ** period) for period, cf in enumerate(cashflows))

exp_irr = None
if exp_total_investment > 0 and any(cf > 0 for cf in exp_cashflows[1:]):
    low_rate, high_rate = -0.99, 5.0
    low_npv, high_npv = _npv_for_rate(low_rate, exp_cashflows), _npv_for_rate(high_rate, exp_cashflows)
    if low_npv * high_npv <= 0:
        for _ in range(200):
            mid_rate = (low_rate + high_rate) / 2
            mid_npv = _npv_for_rate(mid_rate, exp_cashflows)
            if abs(mid_npv) < 1e-10:
                break
            if low_npv * mid_npv > 0:
                low_rate, low_npv = mid_rate, mid_npv
            else:
                high_rate, high_npv = mid_rate, mid_npv
        exp_irr = mid_rate

funding_cash = st.number_input("Available internal funding (₹ crore)", min_value=0.0,
                               value=float(opening_cash / 1e7), step=0.10)
funding_debt = st.number_input("Planned debt funding (₹ crore)", min_value=0.0, value=0.0, step=0.10)
funding_equity = st.number_input("Planned equity funding (₹ crore)", min_value=0.0, value=0.0, step=0.10)
funding_gap = max(0.0, exp_total_investment - funding_cash - funding_debt - funding_equity)

ex1, ex2, ex3, ex4 = st.columns(4)
ex1.metric("Total expansion investment", f"₹{exp_total_investment:,.2f} Cr")
ex2.metric("Annual net operating benefit", f"₹{exp_annual_net_benefit:,.2f} Cr")
ex3.metric("Simple payback", f"{exp_payback:.1f} years" if exp_payback is not None else "Not calculable")
ex4.metric("Funding gap", f"₹{funding_gap:,.2f} Cr")
ex5, ex6 = st.columns(2)
ex5.metric("Simple cumulative ROI", f"{exp_roi*100:,.1f}%" if exp_roi is not None else "Not calculable")
ex6.metric("Illustrative IRR", f"{exp_irr*100:,.1f}%" if exp_irr is not None else "Not calculable")

expansion_plan = pd.DataFrame([
    {"Investment component": "Factory setup", "Amount (₹ crore)": exp_factory},
    {"Investment component": "Machinery and equipment", "Amount (₹ crore)": exp_machinery},
    {"Investment component": "Land and infrastructure", "Amount (₹ crore)": exp_land},
    {"Investment component": "Export market setup", "Amount (₹ crore)": exp_export_setup},
    {"Investment component": "UAE setup", "Amount (₹ crore)": exp_uae_setup},
    {"Investment component": "Initial working capital", "Amount (₹ crore)": exp_working_capital},
    {"Investment component": "Total investment", "Amount (₹ crore)": exp_total_investment},
])
st.dataframe(expansion_plan, use_container_width=True, hide_index=True)
st.subheader("Strategic workstream tracking")
sw1, sw2, sw3 = st.columns(3)
with sw1:
    formulation_status = st.selectbox("Proprietary formulation development",
        ["Not started", "Research", "Pilot", "Commercialized"])
with sw2:
    ip_status = st.selectbox("IP / patent assessment",
        ["Not started", "Prior-art review", "Counsel review", "Filed", "Granted"])
with sw3:
    uae_status = st.selectbox("UAE market entry",
        ["Not started", "Market research", "Regulatory review", "Distributor onboarding", "Launched"])
st.caption(f"Capacity: {exp_capacity_units:,.0f} units/year. IRR uses equal annual net operating benefits and assumes initial working capital is recovered at the end of the evaluation horizon. It excludes tax, inflation, ramp-up, terminal value, financing costs and changes in working capital.")


# Extended workbook includes the interactive product and expansion inputs added below the legacy export section.
from openpyxl import load_workbook
extended_output = BytesIO()
extended_wb = load_workbook(BytesIO(build_excel_workbook()))
def add_extended_dataframe(sheet_name, frame):
    if sheet_name in extended_wb.sheetnames:
        del extended_wb[sheet_name]
    ws = extended_wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False
    for col_idx, col_name in enumerate(frame.columns, 1):
        cell = ws.cell(1, col_idx, str(col_name))
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
    for row_idx, row in enumerate(frame.itertuples(index=False, name=None), 2):
        for col_idx, value in enumerate(row, 1):
            if pd.isna(value):
                value = None
            ws.cell(row_idx, col_idx, value.item() if hasattr(value, "item") else value)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for col_idx, col_name in enumerate(frame.columns, 1):
        sample = [len(str(col_name))] + [len(str(v)) for v in frame[col_name].head(80)]
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max(max(sample)+3, 14), 34)
    return ws

if "pm" in locals():
    extended_product_frame = pm.copy()
else:
    extended_product_frame = product_master.copy()
add_extended_dataframe("Product Analytics", extended_product_frame)
if "product_growth_df" in locals():
    add_extended_dataframe("Product Growth", product_growth_df)
add_extended_dataframe("Scenario Summary", scenario_comparison)
extended_expansion_frame = pd.DataFrame([
    {"Item": "Factory setup", "Value": exp_factory, "Unit": "₹ crore"},
    {"Item": "Machinery and equipment", "Value": exp_machinery, "Unit": "₹ crore"},
    {"Item": "Land and infrastructure", "Value": exp_land, "Unit": "₹ crore"},
    {"Item": "Export market setup", "Value": exp_export_setup, "Unit": "₹ crore"},
    {"Item": "UAE setup", "Value": exp_uae_setup, "Unit": "₹ crore"},
    {"Item": "Initial working capital", "Value": exp_working_capital, "Unit": "₹ crore"},
    {"Item": "Total investment", "Value": exp_total_investment, "Unit": "₹ crore"},
    {"Item": "Annual net operating benefit", "Value": exp_annual_net_benefit, "Unit": "₹ crore"},
    {"Item": "Simple payback", "Value": exp_payback, "Unit": "Years"},
    {"Item": "Simple cumulative ROI", "Value": exp_roi, "Unit": "Ratio"},
    {"Item": "Illustrative IRR", "Value": exp_irr, "Unit": "Ratio"},
    {"Item": "Funding gap", "Value": funding_gap, "Unit": "₹ crore"},
    {"Item": "Annual manufacturing capacity", "Value": exp_capacity_units, "Unit": "Units/year"},
    {"Item": "Proprietary formulation development", "Value": formulation_status, "Unit": "Status"},
    {"Item": "IP / patent assessment", "Value": ip_status, "Unit": "Status"},
    {"Item": "UAE market entry", "Value": uae_status, "Unit": "Status"}
])
add_extended_dataframe("Expansion Plan", extended_expansion_frame)
extended_wb.calculation.fullCalcOnLoad = True
extended_wb.calculation.forceFullCalc = True
extended_wb.calculation.calcMode = "auto"
extended_wb.save(extended_output)
extended_output.seek(0)
st.download_button(
    "⬇ Download extended Excel model (products + expansion)",
    data=extended_output.getvalue(),
    file_name="BOOMER_Extended_Financial_Model.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)
