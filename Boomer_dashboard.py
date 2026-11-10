
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

# ---------------------- EXPORT / DOWNLOAD -----------------

st.header("6. Download your financial model")

csv = forecast.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download annual financial forecast (CSV)",
    data=csv,
    file_name="BOOMER_Financial_Forecast.csv",
    mime="text/csv"
)

pilot_csv = sku_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download pilot SKU economics (CSV)",
    data=pilot_csv,
    file_name="BOOMER_Pilot_SKU_Economics.csv",
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
