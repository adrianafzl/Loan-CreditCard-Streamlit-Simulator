import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Loan & Credit Card Simulator",
    page_icon="💳",
    layout="wide"
)


# -----------------------------------
# Application Title
# -----------------------------------

st.title("💳 Loan & Credit Card Payment Simulator")

st.write(
    """
    This application simulates how different payment behaviours
    affect loan and credit card repayment outcomes.
    """
)


# -----------------------------------
# Sidebar Input Section
# -----------------------------------

st.sidebar.header("📌 Input Parameters")


# -----------------------------------
# Financial Product Selection
# -----------------------------------

product_type = st.sidebar.selectbox(
    "Financial Product",
    [
        "🏠 House Loan",
        "🚗 Car Loan",
        "💳 Credit Card"
    ]
)



# -----------------------------------
# Default Values
# -----------------------------------

if product_type == "🏠 House Loan":

    default_amount = 300000
    default_interest = 4.0
    default_term = 240
    default_payment = 2000


elif product_type == "🚗 Car Loan":

    default_amount = 80000
    default_interest = 3.0
    default_term = 60
    default_payment = 1500


else:

    default_amount = 10000
    default_interest = 18.0
    default_term = 36
    default_payment = 500



# Dynamic Label

if product_type == "💳 Credit Card":

    amount_label = "Credit Card Balance (RM)"

else:

    amount_label = "Loan Amount (RM)"



amount = st.sidebar.number_input(
    amount_label,
    min_value=1000,
    max_value=1000000,
    value=default_amount,
    step=1000
)



interest_rate = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=default_interest,
    step=0.1
)



loan_term = st.sidebar.number_input(
    "Loan Term (Months)",
    min_value=1,
    max_value=360,
    value=default_term
)



monthly_payment = st.sidebar.number_input(
    "Monthly Payment (RM)",
    min_value=100,
    value=default_payment,
    step=100
)



payment_behavior = st.sidebar.selectbox(
    "Payment Behaviour",
    [
        "On-time",
        "Early",
        "Late"
    ]
)



# -----------------------------------
# Payment Simulation Function
# -----------------------------------

def simulate_payment(
        amount,
        interest_rate,
        monthly_payment,
        behavior
):

    balance = amount

    monthly_interest_rate = interest_rate / 100 / 12

    total_interest = 0
    total_payment = 0

    month = 0

    payment_history = []


    if behavior == "Early":

        actual_payment = monthly_payment * 1.3


    elif behavior == "Late":

        actual_payment = monthly_payment * 0.7


    else:

        actual_payment = monthly_payment



    while balance > 0 and month < 600:

        month += 1


        interest = balance * monthly_interest_rate


        balance += interest


        payment = min(actual_payment, balance)


        balance -= payment


        total_interest += interest

        total_payment += payment



        payment_history.append(
            {
                "Month": month,
                "Payment": payment,
                "Interest": interest,
                "Remaining Balance": balance
            }
        )


    return (
        pd.DataFrame(payment_history),
        total_interest,
        total_payment,
        month
    )



# -----------------------------------
# Run Simulation
# -----------------------------------

payment_data, total_interest, total_paid, payoff_months = simulate_payment(
    amount,
    interest_rate,
    monthly_payment,
    payment_behavior
)



# -----------------------------------
# Comparison Simulation
# -----------------------------------

comparison_results = []


for behaviour in ["Early", "On-time", "Late"]:

    _, interest, total_payment_compare, months_compare = simulate_payment(
        amount,
        interest_rate,
        monthly_payment,
        behaviour
    )


    comparison_results.append(
        {
            "Payment Behaviour": behaviour,
            "Total Interest": interest,
            "Total Payment": total_payment_compare,
            "Months": months_compare,
            "Extra Cost": total_payment_compare - amount
        }
    )


comparison_df = pd.DataFrame(comparison_results)

# -----------------------------------
# Dashboard Tabs
# -----------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "📌 Summary Dashboard",
        "📋 Payment Schedule",
        "📊 Visualizations"
    ]
)



# ===================================
# TAB 1 : SUMMARY DASHBOARD
# ===================================

with tab1:


    st.subheader("Selected Scenario")


    st.write(
        f"**Financial Product:** {product_type}"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            f"**{amount_label}:** RM {amount:,.2f}"
        )


        st.write(
            f"**Annual Interest Rate:** {interest_rate}%"
        )


        st.write(
            f"**Loan Term:** {loan_term} months"
        )



    with col2:

        st.write(
            f"**Monthly Payment:** RM {monthly_payment:,.2f}"
        )


        st.write(
            f"**Payment Behaviour:** {payment_behavior}"
        )



    st.divider()



    st.subheader("📊 Simulation Results")


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(
            "Total Interest Paid",
            f"RM {total_interest:,.2f}"
        )



    with col2:

        st.metric(
            "Total Amount Repaid",
            f"RM {total_paid:,.2f}"
        )



    with col3:

        st.metric(
            "Time to Payoff",
            f"{payoff_months} months"
        )



    st.divider()



    st.subheader("Comparison Summary")


    display_df = comparison_df.copy()


    display_df["Total Interest"] = (
        display_df["Total Interest"]
        .apply(lambda x: f"RM {x:,.2f}")
    )


    display_df["Total Payment"] = (
        display_df["Total Payment"]
        .apply(lambda x: f"RM {x:,.2f}")
    )


    display_df["Extra Cost"] = (
        display_df["Extra Cost"]
        .apply(lambda x: f"RM {x:,.2f}")
    )


    st.dataframe(
        display_df,
        use_container_width=True
    )



    # -----------------------------------
    # About This App
    # -----------------------------------

    st.divider()


    st.subheader("ℹ️ About This Simulator")


    st.write(
        """
        This application demonstrates how different repayment 
        behaviours affect loan and credit card repayment outcomes.

        **Early Payment**
        - Higher monthly payment
        - Faster repayment period
        - Lower total interest cost


        **On-time Payment**
        - Regular repayment schedule
        - Standard interest cost


        **Late Payment**
        - Lower payment amount
        - Longer repayment period
        - Higher overall repayment cost
        """
    )



# ===================================
# TAB 2 : PAYMENT SCHEDULE
# ===================================

with tab2:


    st.subheader("📋 Payment Schedule")


    formatted_payment_data = payment_data.style.format(
        {
            "Payment": "RM {:.2f}",
            "Interest": "RM {:.2f}",
            "Remaining Balance": "RM {:.2f}"
        }
    )


    st.dataframe(
        formatted_payment_data,
        use_container_width=True
    )



    # -----------------------------------
    # Download CSV Button
    # -----------------------------------

    csv = payment_data.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="⬇ Download Payment Schedule CSV",
        data=csv,
        file_name="payment_schedule.csv",
        mime="text/csv"
    )



# ===================================
# TAB 3 : VISUALIZATIONS
# ===================================

with tab3:


    # -----------------------------------
    # View 1
    # -----------------------------------

    st.subheader("📈 Remaining Balance Over Time")


    balance_chart = px.line(
        payment_data,
        x="Month",
        y="Remaining Balance",
        title=f"{product_type} Balance Reduction"
    )


    balance_chart.update_layout(
        xaxis_title="Month",
        yaxis_title="Remaining Balance (RM)"
    )


    st.plotly_chart(
        balance_chart,
        use_container_width=True
    )



    # -----------------------------------
    # View 2
    # -----------------------------------

    st.subheader("📊 Total Interest Comparison")


    interest_chart = px.bar(
        comparison_df,
        x="Payment Behaviour",
        y="Total Interest",
        text_auto=".2s",
        title="Interest Cost Comparison Between Payment Strategies"
    )


    interest_chart.update_layout(
        xaxis_title="Payment Behaviour",
        yaxis_title="Total Interest Paid (RM)"
    )


    st.plotly_chart(
        interest_chart,
        use_container_width=True
    )



    # -----------------------------------
    # View 3
    # -----------------------------------

    st.subheader("📉 Profit / Loss Analysis")


    profit_chart = px.bar(
        comparison_df,
        x="Payment Behaviour",
        y="Extra Cost",
        text_auto=".2s",
        title="Additional Cost Compared to Original Amount"
    )


    profit_chart.update_layout(
        xaxis_title="Payment Behaviour",
        yaxis_title="Extra Cost (RM)"
    )


    st.plotly_chart(
        profit_chart,
        use_container_width=True
    )