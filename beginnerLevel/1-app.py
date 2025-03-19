import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

# Language selection
language = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

# Set translations based on language
if language == "Türkçe":
    # Turkish translations
    translations = {
        "title": "Kişisel Bütçe Hesaplayıcı",
        "sidebar_header": "Finansal bilgilerinizi girin",
        "income": "Aylık Gelir (₺)",
        "expenses_header": "Aylık Giderler",
        "rent": "Kira/Konut (₺)",
        "bills": "Faturalar (₺)",
        "food": "Gıda (₺)",
        "transport": "Ulaşım (₺)",
        "entertainment": "Eğlence/Sosyal (₺)",
        "other": "Diğer Giderler (₺)",
        "summary_header": "Bütçe Özeti",
        "total_income": "Toplam Gelir",
        "total_expenses": "Toplam Gider",
        "remaining": "Kalan",
        "breakdown_header": "Gider Dağılımı",
        "category": "Kategori",
        "amount": "Tutar",
        "percentage": "Yüzde",
        "recommendations_header": "Bütçe Önerileri",
        "great_saving": "Harika! Gelirinizin %20'sinden fazlasını tasarruf ediyorsunuz. Bu tasarrufları yatırıma yönlendirmeyi düşünebilirsiniz.",
        "good_saving": "İyi! Gelirinizin %10'undan fazlasını tasarruf ediyorsunuz. Tasarruflarınızı artırmak için giderlerinizi gözden geçirebilirsiniz.",
        "low_saving": "Tasarruf oranınız düşük. Bazı giderlerinizi azaltmayı düşünebilirsiniz.",
        "highest_category": "En yüksek gider kategoriniz: {} ({} ₺)",
        "negative_saving": "Uyarı! Giderleriniz gelirinizi aşıyor. Bütçenizi acilen gözden geçirmeniz gerekiyor.",
        "short_amount": "Bu ay {} ₺ açık veriyorsunuz.",
        "health_header": "Bütçe Sağlığı Göstergeleri",
        "housing_cost": "Konut Maliyeti",
        "food_cost": "Gıda Maliyeti",
        "housing_percent": "Konut, gelirinizin %{} (Önerilen: ≤%30)",
        "food_percent": "Gıda, gelirinizin %{} (Önerilen: ≤%15)",
        "projection_header": "Aylık Tasarruf Projeksiyonu",
        "months": "Aylar",
        "savings": "Tasarruf (₺)",
        "projection_title": "12 Aylık Tasarruf Projeksiyonu",
        "annual_savings": "Tahmini yıllık tasarruf: {} ₺",
        "currency": "₺",
        "percent_sign": "%",
        "categories": ['Kira/Konut', 'Faturalar', 'Gıda', 'Ulaşım', 'Eğlence/Sosyal', 'Diğer'],
        "enter_data": "Grafik göstermek için gider değerlerini girin.",
        "enter_data_table": "Tablo göstermek için gider değerlerini girin."
    }
else:
    # English translations
    translations = {
        "title": "Personal Budget Calculator",
        "sidebar_header": "Enter your financial information",
        "income": "Monthly Income ($)",
        "expenses_header": "Monthly Expenses",
        "rent": "Rent/Housing ($)",
        "bills": "Utilities ($)",
        "food": "Food ($)",
        "transport": "Transportation ($)",
        "entertainment": "Entertainment/Social ($)",
        "other": "Other Expenses ($)",
        "summary_header": "Budget Summary",
        "total_income": "Total Income",
        "total_expenses": "Total Expenses",
        "remaining": "Remaining",
        "breakdown_header": "Expense Breakdown",
        "category": "Category",
        "amount": "Amount",
        "percentage": "Percentage",
        "recommendations_header": "Budget Recommendations",
        "great_saving": "Great! You're saving more than 20% of your income. Consider investing these savings.",
        "good_saving": "Good! You're saving more than 10% of your income. You might want to review your expenses to increase your savings.",
        "low_saving": "Your savings rate is low. Consider reducing some expenses.",
        "highest_category": "Your highest expense category: {} (${:.0f})",
        "negative_saving": "Warning! Your expenses exceed your income. You need to review your budget immediately.",
        "short_amount": "This month you're ${:.0f} short.",
        "health_header": "Budget Health Indicators",
        "housing_cost": "Housing Cost",
        "food_cost": "Food Cost",
        "housing_percent": "Housing is {}% of income (Recommended: ≤30%)",
        "food_percent": "Food is {}% of income (Recommended: ≤15%)",
        "projection_header": "Monthly Savings Projection",
        "months": "Months",
        "savings": "Savings ($)",
        "projection_title": "Projected Savings Over 12 Months",
        "annual_savings": "Projected annual savings: ${:.0f}",
        "currency": "$",
        "percent_sign": "%",
        "categories": ['Rent/Housing', 'Utilities', 'Food', 'Transportation', 'Entertainment/Social', 'Other'],
        "enter_data": "Please enter expense values to display the chart.",
        "enter_data_table": "Please enter expense values to display the table."
    }

# App title
st.title(translations["title"])

# Custom format function for currency with thousands separator
def format_currency(value, currency_symbol):
    if language == "Türkçe":
        # Format with Turkish style: 25.000 ₺
        return f"{value:,} {currency_symbol}".replace(",", ".")
    else:
        # Format with English style: $25,000
        return f"{currency_symbol}{value:,}"

# Sidebar for inputs
st.sidebar.header(translations["sidebar_header"])
income = st.sidebar.number_input(translations["income"], min_value=0, step=1000, value=0)

# Expense categories
st.sidebar.subheader(translations["expenses_header"])
rent = st.sidebar.number_input(translations["rent"], min_value=0, step=500, value=0)
bills = st.sidebar.number_input(translations["bills"], min_value=0, step=100, value=0)
food = st.sidebar.number_input(translations["food"], min_value=0, step=100, value=0)
transport = st.sidebar.number_input(translations["transport"], min_value=0, step=100, value=0)
entertainment = st.sidebar.number_input(translations["entertainment"], min_value=0, step=100, value=0)
other = st.sidebar.number_input(translations["other"], min_value=0, step=100, value=0)

# Calculate totals
total_expenses = rent + bills + food + transport + entertainment + other
remaining = income - total_expenses
savings_rate = (remaining / income) * 100 if income > 0 else 0

# Display summary
st.header(translations["summary_header"])
col1, col2, col3 = st.columns(3)
col1.metric(translations["total_income"], format_currency(income, translations["currency"]))
col2.metric(translations["total_expenses"], format_currency(total_expenses, translations["currency"]))
col3.metric(translations["remaining"], format_currency(remaining, translations["currency"]), f"{translations['percent_sign']}{savings_rate:.1f}" if income > 0 else "")

# Create expense dataframe for visualization
expenses_data = {
    translations["category"]: translations["categories"],
    translations["amount"]: [rent, bills, food, transport, entertainment, other],
}
df_expenses = pd.DataFrame(expenses_data)
df_expenses[translations["percentage"]] = df_expenses[translations["amount"]] / income * 100 if income > 0 else 0

# Display expense breakdown
st.header(translations["breakdown_header"])
col1, col2 = st.columns([2, 1])

with col1:
    # Check if we have valid data for pie chart
    if income > 0 and any(df_expenses[translations["amount"]] > 0):
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(df_expenses[translations["amount"]], labels=df_expenses[translations["category"]], autopct='%1.1f%%', 
               startangle=90, shadow=True)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig)
    else:
        st.info(translations["enter_data"])

with col2:
    # Check if we have valid data for table
    if income > 0 and any(df_expenses[translations["amount"]] > 0):
        # Format DataFrame for display
        display_df = df_expenses.copy()
        
        # Format amount column with currency
        if language == "Türkçe":
            display_df[translations["amount"]] = display_df[translations["amount"]].apply(
                lambda x: f"{int(x):,} ₺".replace(",", ".")
            )
            display_df[translations["percentage"]] = display_df[translations["percentage"]].apply(
                lambda x: f"%{x:.1f}"
            )
        else:
            display_df[translations["amount"]] = display_df[translations["amount"]].apply(
                lambda x: f"${int(x):,}"
            )
            display_df[translations["percentage"]] = display_df[translations["percentage"]].apply(
                lambda x: f"{x:.1f}%"
            )
        
        st.dataframe(
            display_df[[translations["category"], translations["amount"], translations["percentage"]]]
            .set_index(translations["category"])
        )
    else:
        st.info(translations["enter_data_table"])

# Recommendations
st.header(translations["recommendations_header"])

if income <= 0:
    st.info("Please enter your income to get recommendations.")
elif savings_rate >= 20:
    st.success(translations["great_saving"])
elif savings_rate >= 10:
    st.info(translations["good_saving"])
elif savings_rate >= 0:
    st.warning(translations["low_saving"])
    if any(df_expenses[translations["amount"]] > 0):
        highest_category = df_expenses.loc[df_expenses[translations["amount"]].idxmax()]
        if language == "Türkçe":
            st.write(translations["highest_category"].format(
                highest_category[translations["category"]], 
                f"{int(highest_category[translations['amount']]):,}".replace(",", ".")
            ))
        else:
            st.write(translations["highest_category"].format(
                highest_category[translations["category"]], 
                int(highest_category[translations["amount"]])
            ))
else:
    st.error(translations["negative_saving"])
    if language == "Türkçe":
        st.write(translations["short_amount"].format(
            f"{int(abs(remaining)):,}".replace(",", ".")
        ))
    else:
        st.write(translations["short_amount"].format(int(abs(remaining))))

# Budget health indicators
if income > 0 and (rent > 0 or food > 0):
    st.header(translations["health_header"])
    housing_percent = (rent / income) * 100 if income > 0 else 0
    food_percent = (food / income) * 100 if income > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(translations["housing_cost"])
        if housing_percent <= 30:
            st.success(translations["housing_percent"].format(f"{housing_percent:.1f}"))
        else:
            st.warning(translations["housing_percent"].format(f"{housing_percent:.1f}"))

    with col2:
        st.subheader(translations["food_cost"])
        if food_percent <= 15:
            st.success(translations["food_percent"].format(f"{food_percent:.1f}"))
        else:
            st.warning(translations["food_percent"].format(f"{food_percent:.1f}"))

# Savings projection
if income > 0 and remaining > 0:
    st.header(translations["projection_header"])
    months = list(range(1, 13))
    savings = [remaining * m for m in months]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, savings, marker='o', linestyle='-', color='green')
    ax.set_xlabel(translations["months"])
    ax.set_ylabel(translations["savings"])
    ax.set_title(translations["projection_title"])
    ax.grid(True)
    
    # Format y-axis with thousands separator
    if language == "Türkçe":
        # Custom format function for Turkish style
        def turkish_format(x, pos):
            return f'{int(x):,}'.replace(',', '.')
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(turkish_format))
    else:
        # Use comma as thousands separator for English
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
    st.pyplot(fig)

    # Add annual projection
    annual_savings = remaining * 12
    if language == "Türkçe":
        st.write(translations["annual_savings"].format(
            f"{int(annual_savings):,}".replace(",", ".")
        ))
    else:
        st.write(translations["annual_savings"].format(int(annual_savings)))