# 🚗 Germany EV Charging Infrastructure Dashboard

An interactive web application and exploratory data analysis (EDA) project analyzing the distribution, operators, and capacity of Electric Vehicle (EV) charging stations across Germany. This project is built using **Python**, **Streamlit**, **Plotly Express**, and **Pandas**.

---

## 🌟 Key Features

1. **Interactive Spatial Map**: Fully interactive map of Germany displaying all 61,000+ charging stations. Points are color-coded by charging type (Normal vs. Fast) and sized by the number of charging points. Built-in point clustering enables smooth loading and seamless zooming.
2. **Key Metric Metrics**: Displays essential KPIs including the total number of stations, total charging points, total combined charging capacity in megawatts (MW), and the percentage share of fast DC chargers.
3. **Interactive Side Filters**: Drill down into the dataset by:
   - **Operator (Betreiber)**: Select specific energy companies (e.g., EnBW, E.ON, local utilities).
   - **Regional Districts (Landkreise)**: Filter by district or city.
   - **Power Output (kW)**: Slide to filter stations by minimum/maximum charging capacity.
   - **Charging Class**: Toggle Normal AC vs. Fast DC chargers.
4. **Analytical Visualizations**: Interactive bar charts of top operators and log-scaled histograms showing the power capacity distribution.
5. **Interactive Data Table**: Search and review the filtered dataset in a responsive grid, with an option to download the filtered subset as a CSV file.

---

## 📈 Key Insights from the Data

- **Normal vs. Fast Chargers**: Normal AC chargers (typically up to 22 kW) make up approximately **80%** of the infrastructure, while high-power DC fast chargers (50 kW to 300+ kW) comprise the remaining **20%**.
- **Market Dominance**: The infrastructure deployment is heavily driven by key operators like **EnBW mobility+**, **E.ON**, and regional municipal utilities (*Stadtwerke*).
- **Urban Concentration**: Geographical analysis shows high spatial concentrations in major metropolitan centers like Berlin, Munich, Hamburg, and the Rhine-Ruhr industrial region.

---

## 📁 Repository Structure

```text
├── app.py                                        # Streamlit dashboard application
├── EV_Charging_Analysis.ipynb                    # Structured Jupyter EDA notebook
├── rhein-kreis-neuss-ladesaulen-in-deutschland.csv # Raw German EV charging station dataset
├── requirements.txt                              # Required Python libraries
└── .gitignore                                    # Git ignore patterns
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Install Dependencies
Create a virtual environment, activate it, and install the required packages:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard
Launch the web application locally:

```bash
streamlit run app.py
```
This will automatically open the dashboard in your default browser at `http://localhost:8501`.

### 4. Run the Jupyter Notebook
To review the step-by-step exploratory analysis, launch Jupyter Lab or Notebook:

```bash
pip install jupyterlab
jupyter lab
```
Open `EV_Charging_Analysis.ipynb` to view the data loading, coordinate extraction, and static Plotly visualizations.

---

## 📊 Data Source
The dataset used in this analysis is official public registry data from Germany's Federal Grid Agency (*Bundesnetzagentur*), documenting EV charging facilities deployed across all German states and municipal districts.
