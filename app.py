import streamlit as st
import statistics
from collections import Counter
import math

st.title("📊 Mean, Median, Mode Calculator (Grouped Data with Detailed Steps)")

st.sidebar.header("📝 Instructions")
st.sidebar.write("""
1. Enter class intervals (e.g., 0-10, 10-20) in first box
2. Enter corresponding frequencies in second box
3. Values and frequencies must be separated by commas
4. Both must have same number of entries
""")

# Input data values and frequencies
col1, col2 = st.columns(2)

with col1:
    data_values = st.text_area("Enter class intervals (e.g., 0-10, 10-20):", 
                              value="0-10, 10-20, 20-30, 30-40, 40-50")
with col2:
    data_freq = st.text_area("Enter corresponding frequencies (fᵢ):", 
                            value="5, 8, 12, 7, 3")

calculate_clicked = st.button("🚀 Calculate", type="primary")

def parse_class_interval(interval_str):
    """Parse class interval string and return midpoint"""
    try:
        if '-' in interval_str:
            parts = interval_str.split('-')
            lower = float(parts[0].strip())
            upper = float(parts[1].strip())
            return (lower + upper) / 2, lower, upper, upper - lower
        else:
            # Single value
            val = float(interval_str.strip())
            return val, val, val, 0
    except:
        raise ValueError(f"Invalid class interval: {interval_str}")

# Convert to lists
try:
    intervals = [x.strip() for x in data_values.split(',')]
    freqs = list(map(int, data_freq.split(',')))
    
    if len(intervals) != len(freqs):
        st.error("⚠️ Number of class intervals and frequencies must be equal.")
        st.stop()
    if len(intervals) == 0:
        st.warning("Please enter some data to continue.")
        st.stop()
    
    # Parse class intervals and calculate midpoints
    class_info = []
    for interval in intervals:
        midpoint, lower, upper, width = parse_class_interval(interval)
        class_info.append({
            'midpoint': midpoint,
            'lower': lower,
            'upper': upper,
            'width': width
        })
    
    values = [info['midpoint'] for info in class_info]
    class_widths = [info['width'] for info in class_info]
    
    # Auto-detect class width
    if class_widths:
        # Use the most common class width
        h = max(set(class_widths), key=class_widths.count)
        # If detected width is zero, check if we have any non-zero widths
        if h == 0:
            non_zero_widths = [w for w in class_widths if w > 0]
            h = non_zero_widths[0] if non_zero_widths else 0
    else:
        h = 0
    
except Exception as e:
    st.error(f"⚠️ Error parsing data: {e}")
    st.stop()

# Total observations
N = sum(freqs)

# Display basic information
st.subheader("📊 Basic Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Number of Classes", len(values))
with col2:
    st.metric("Total Observations (N)", N)
with col3:
    st.metric("Sum of fᵢxᵢ", sum(x*f for x, f in zip(values, freqs)))
with col4:
    st.metric("Class Width (h)", f"{h:.1f}" if h > 0 else "0 (Single values)")

# Frequency table with detailed calculations
st.subheader("📋 Frequency Distribution Table")
freq_table_data = []
for i, (interval, x, f, info) in enumerate(zip(intervals, values, freqs, class_info), 1):
    freq_table_data.append({
        "Class": f"Class {i}",
        "Class Interval": interval,
        "Midpoint (xᵢ)": f"{x:.1f}",
        "Frequency (fᵢ)": f,
        "fᵢ × xᵢ": f"{x * f:.1f}"
    })

# Add total row
total_f = sum(freqs)
total_fx = sum(x*f for x, f in zip(values, freqs))
freq_table_data.append({
    "Class": "**Total**",
    "Class Interval": "**-**",
    "Midpoint (xᵢ)": "**-**",
    "Frequency (fᵢ)": f"**{total_f}**",
    "fᵢ × xᵢ": f"**{total_fx:.1f}**"
})

st.table(freq_table_data)

# Select measure
choice = st.radio("Select measure to calculate:", ["Mean", "Median", "Mode"], horizontal=True)

# --- MEAN CALCULATION ---
if choice == "Mean":
    st.header("🎯 Mean Calculation - All Methods")
    
    # Let user choose which method to display
    mean_method = st.radio("Select Mean Calculation Method:", 
                          ["Direct Method", "Assumed Mean Method", "Step Deviation Method", "All Methods"], 
                          horizontal=True)
    
    # Common values
    A = values[len(values)//2]  # Default assumed mean
    
    # DIRECT METHOD (Always shown if selected or "All Methods")
    if mean_method in ["Direct Method", "All Methods"]:
        st.subheader("📌 Method 1: Direct Method")
        st.latex(r"\bar{x} = \frac{\Sigma f_ix_i}{\Sigma f_i} = \frac{\Sigma f_ix_i}{N}")
        
        # Show detailed calculation
        calculation_steps = " + ".join([f"({f}×{x:.1f})" for x, f in zip(values, freqs)])
        st.write(f"**Step 1:** Calculate Σfᵢxᵢ = {calculation_steps} = {total_fx:.1f}")
        st.write(f"**Step 2:** Calculate N = Σfᵢ = {N}")
        st.write(f"**Step 3:** Apply formula:")
        
        mean_direct = total_fx / N
        st.latex(r"\bar{x} = \frac{" + f"{total_fx:.1f}" + "}{" + str(N) + "} = " + f"{mean_direct:.4f}")
        st.success(f"**Mean (Direct Method) = {mean_direct:.4f}**")
    
    # ASSUMED MEAN METHOD
    if mean_method in ["Assumed Mean Method", "All Methods"]:
        st.subheader("📌 Method 2: Assumed Mean Method")
        st.latex(r"\bar{x} = A + \frac{\Sigma f_id_i}{\Sigma f_i}")
        st.latex(r"\text{where } d_i = x_i - A")
        
        # Let user choose assumed mean
        col1, col2 = st.columns(2)
        with col1:
            A_option = st.selectbox("Choose assumed mean (A):", 
                                   ["Auto-select (middle value)", "Custom value"])
            
            if A_option == "Auto-select (middle value)":
                A = values[len(values)//2]
            else:
                A = st.number_input("Enter assumed mean A:", value=float(values[len(values)//2]), step=1.0)
        
        st.write(f"**Step 1:** Assume mean A = {A:.1f}")
        
        # Create table for assumed mean method
        st.write("**Step 2:** Calculate dᵢ = xᵢ - A and fᵢdᵢ")
        assumed_table = []
        sum_fd = 0
        
        for x, f in zip(values, freqs):
            d = x - A
            fd = f * d
            sum_fd += fd
            assumed_table.append({
                "xᵢ": f"{x:.1f}", "fᵢ": f, "dᵢ = xᵢ - A": f"{d:.1f}", "fᵢdᵢ": f"{fd:.1f}"
            })
        
        assumed_table.append({
            "xᵢ": "**Total**", "fᵢ": f"**{N}**", "dᵢ = xᵢ - A": "**-**", "fᵢdᵢ": f"**{sum_fd:.1f}**"
        })
        
        st.table(assumed_table)
        
        st.write(f"**Step 3:** Apply formula:")
        mean_assumed = A + (sum_fd / N)
        st.latex(r"\bar{x} = " + f"{A:.1f}" + " + \\frac{" + f"{sum_fd:.1f}" + "}{" + str(N) + "}")
        st.latex(r"= " + f"{A:.1f}" + " + " + f"{sum_fd/N:.4f} = {mean_assumed:.4f}")
        st.success(f"**Mean (Assumed Mean Method) = {mean_assumed:.4f}**")

    # STEP DEVIATION METHOD
    if mean_method in ["Step Deviation Method", "All Methods"]:
        st.subheader("📌 Method 3: Step Deviation Method")
        st.latex(r"\bar{x} = A + \left(\frac{\Sigma f_id_i}{\Sigma f_i}\right) \times h")
        st.latex(r"\text{where } d_i = \frac{x_i - A}{h}")
        
        # Show auto-detected class width
        st.write(f"**Auto-detected Class Width (h):** {h}")
        
        if h == 0:
            st.error("❌ Step Deviation Method cannot be used when class width (h) is zero.")
            st.write("""
            **Why this happens:**
            - Class width (h) = 0 indicates single values instead of class intervals
            - Step deviation method requires non-zero class width for grouping
            - Division by h would cause mathematical errors
            
            **Recommended alternatives:**
            - Use **Direct Method** or **Assumed Mean Method** instead
            - Or enter proper class intervals (e.g., 0-10, 10-20) instead of single values
            """)
        else:
            # Use auto-detected class width
            A_step = values[len(values)//2]
            st.write(f"**Step 1:** Assume A = {A_step:.1f}, Class width h = {h}")
            
            # Create table for step deviation method
            st.write("**Step 2:** Calculate dᵢ = (xᵢ - A)/h and fᵢdᵢ")
            step_table = []
            sum_fd = 0
            
            for x, f in zip(values, freqs):
                d = (x - A_step) / h
                fd = f * d
                sum_fd += fd
                step_table.append({
                    "xᵢ": f"{x:.1f}", "fᵢ": f, "dᵢ = (xᵢ - A)/h": f"{d:.2f}", "fᵢdᵢ": f"{fd:.2f}"
                })
            
            step_table.append({
                "xᵢ": "**Total**", "fᵢ": f"**{N}**", "dᵢ = (xᵢ - A)/h": "**-**", "fᵢdᵢ": f"**{sum_fd:.2f}**"
            })
            
            st.table(step_table)
            
            st.write(f"**Step 3:** Apply formula:")
            mean_step = A_step + (sum_fd / N) * h
            st.latex(r"\bar{x} = " + f"{A_step:.1f}" + " + \\left(\\frac{" + f"{sum_fd:.2f}" + "}{" + str(N) + "}\\right) \\times " + str(h))
            st.latex(r"= " + f"{A_step:.1f}" + " + " + f"({sum_fd/N:.4f}) × {h} = {mean_step:.4f}")
            st.success(f"**Mean (Step Deviation Method) = {mean_step:.4f}**")

# --- MEDIAN CALCULATION ---
elif choice == "Median":
    st.header("🎯 Median Calculation - Detailed Steps")
    
    # Show auto-detected class width
    st.write(f"**Auto-detected Class Width (h):** {h}")
    
    if h == 0:
        st.error("❌ Median calculation for grouped data cannot be used when class width (h) is zero.")
        st.write("""
        **Why this happens:**
        - Class width (h) = 0 indicates single values instead of proper class intervals
        - Grouped median formula requires non-zero class width
        - The formula involves division and multiplication by h
        
        **Recommended alternatives:**
        - Use **ungrouped data median** calculation instead
        - Or enter proper class intervals (e.g., 0-10, 10-20) instead of single values
        
        **Ungrouped Median Formula:**
        For individual values, median is the middle value when data is sorted
        """)
        
        # Calculate ungrouped median as alternative
        st.subheader("📌 Alternative: Ungrouped Median Calculation")
        
        # Create expanded frequency list
        expanded_data = []
        for value, freq in zip(values, freqs):
            expanded_data.extend([value] * freq)
        
        expanded_data.sort()
        st.write(f"**Sorted data:** {expanded_data}")
        
        if len(expanded_data) % 2 == 1:
            # Odd number of observations
            median_ungrouped = expanded_data[len(expanded_data) // 2]
            st.write(f"**Median position:** (N+1)/2 = ({len(expanded_data)}+1)/2 = {(len(expanded_data)+1)/2}")
        else:
            # Even number of observations
            mid1 = expanded_data[len(expanded_data) // 2 - 1]
            mid2 = expanded_data[len(expanded_data) // 2]
            median_ungrouped = (mid1 + mid2) / 2
            st.write(f"**Median position:** Average of {len(expanded_data)//2}th and {len(expanded_data)//2 + 1}th values")
        
        st.success(f"**Ungrouped Median = {median_ungrouped:.4f}**")
        
    else:
        st.latex(r"\text{Median} = L + \left(\frac{\frac{N}{2} - CF}{f}\right) \times h")
        
        # Create cumulative frequency table
        st.subheader("📌 Step 1: Cumulative Frequency Distribution")
        cum_freq_table = []
        cumulative = 0
        
        for i, (interval, x, f_val, info) in enumerate(zip(intervals, values, freqs, class_info), 1):
            cumulative += f_val
            cum_freq_table.append({
                "Class": f"Class {i}",
                "Class Interval": interval,
                "Midpoint (xᵢ)": f"{x:.1f}",
                "Frequency (fᵢ)": f_val,
                "Cumulative Frequency": cumulative
            })
        
        st.table(cum_freq_table)
        
        # Find median class
        st.subheader("📌 Step 2: Identify Median Class")
        median_pos = N / 2
        st.write(f"Median position = N/2 = {N}/2 = {median_pos}")
        
        median_class_index = None
        cumulative_freqs = [sum(freqs[:i+1]) for i in range(len(freqs))]
        
        for i, cf in enumerate(cumulative_freqs):
            if cf >= median_pos:
                median_class_index = i
                break
        
        if median_class_index is None:
            median_class_index = len(values) - 1
        
        median_class_info = class_info[median_class_index]
        L = median_class_info['lower']  # Lower boundary of median class
        f_median = freqs[median_class_index]  # Frequency of median class
        CF = sum(freqs[:median_class_index])  # Cumulative frequency before median class
        
        st.write(f"**Median Class:** {intervals[median_class_index]}")
        st.write(f"**Lower boundary (L):** {L}")
        st.write(f"**Cumulative frequency before median class (CF):** {CF}")
        st.write(f"**Frequency of median class (f):** {f_median}")
        st.write(f"**Class width (h):** {h}")
        
        # Calculate median
        st.subheader("📌 Step 3: Calculate Median")
        
        # Check if frequency of median class is zero to avoid division by zero
        if f_median == 0:
            st.error("Frequency of median class cannot be zero. Please check your frequency data.")
            st.stop()
        
        median = L + ((median_pos - CF) / f_median) * h
        
        st.latex(r"\text{Median} = " + str(L) + " + \\left(\\frac{" + f"{median_pos}" + " - " + str(CF) + "}{" + str(f_median) + "}\\right) \\times " + str(h))
        st.latex(r"= " + str(L) + " + \\left(\\frac{" + f"{median_pos - CF:.2f}" + "}{" + str(f_median) + "}\\right) \\times " + str(h))
        st.latex(r"= " + str(L) + " + " + f"{(median_pos - CF)/f_median:.4f} × {h}")
        st.latex(r"= " + f"{median:.4f}")
        
        st.success(f"**Median = {median:.4f}**")

# --- MODE CALCULATION ---
elif choice == "Mode":
    st.header("🎯 Mode Calculation - Grouped Data Formula")
    
    # Show auto-detected class width
    st.write(f"**Auto-detected Class Width (h):** {h}")
    
    if h == 0:
        st.error("❌ Mode calculation for grouped data cannot be used when class width (h) is zero.")
        st.write("""
        **Why this happens:**
        - Class width (h) = 0 indicates single values instead of proper class intervals
        - Grouped mode formula requires non-zero class width
        - The formula involves multiplication by h
        
        **Recommended alternatives:**
        - Use **ungrouped data mode** calculation instead
        - Or enter proper class intervals (e.g., 0-10, 10-20) instead of single values
        
        **Ungrouped Mode Formula:**
        For individual values, mode is the value with highest frequency
        """)
        
        # Calculate ungrouped mode as alternative
        st.subheader("📌 Alternative: Ungrouped Mode Calculation")
        
        # Find value with highest frequency
        max_freq = max(freqs)
        modal_values = [values[i] for i, f in enumerate(freqs) if f == max_freq]
        
        if len(modal_values) == 1:
            st.write(f"**Mode:** Value with highest frequency = {modal_values[0]} (appears {max_freq} times)")
            st.success(f"**Ungrouped Mode = {modal_values[0]:.1f}**")
        else:
            st.write(f"**Multiple modes detected:** {modal_values} (each appears {max_freq} times)")
            st.success(f"**Ungrouped Modes = {', '.join([f'{v:.1f}' for v in modal_values])}**")
        
    else:
        st.latex(r"Z = L + \left(\frac{f_1 - f_0}{2f_1 - f_0 - f_2}\right) \times h")
        st.write("Where:")
        st.write("- **Z** = Mode")
        st.write("- **L** = Lower boundary of modal class")
        st.write("- **f₁** = Frequency of modal class")
        st.write("- **f₀** = Frequency of class preceding modal class")
        st.write("- **f₂** = Frequency of class succeeding modal class")
        st.write("- **h** = Class interval width")

        # Find modal class (class with highest frequency)
        max_freq = max(freqs)
        modal_class_index = freqs.index(max_freq)
        modal_class_info = class_info[modal_class_index]
        
        st.subheader("📋 Frequency Distribution")
        freq_table = []
        for i, (interval, x, f) in enumerate(zip(intervals, values, freqs)):
            if i == modal_class_index:
                freq_table.append({
                    "Class": f"Class {i+1}", 
                    "Class Interval": f"**{interval}**", 
                    "Midpoint (xᵢ)": f"**{x:.1f}**",
                    "Frequency (fᵢ)": f"**{f}**", 
                    "Remarks": "**Modal Class**"
                })
            else:
                freq_table.append({
                    "Class": f"Class {i+1}", 
                    "Class Interval": interval, 
                    "Midpoint (xᵢ)": f"{x:.1f}",
                    "Frequency (fᵢ)": f, 
                    "Remarks": ""
                })
        
        st.table(freq_table)

        st.subheader("📌 Step-by-Step Calculation")

        # Step 1: Identify modal class
        st.write("**Step 1: Identify Modal Class**")
        st.write(f"Modal class = Class with highest frequency = {intervals[modal_class_index]} (Frequency = {max_freq})")
        
        # Step 2: Get required values
        L = modal_class_info['lower']  # Lower boundary
        
        f1 = max_freq  # Frequency of modal class
        
        # Frequency of preceding class (f0)
        if modal_class_index > 0:
            f0 = freqs[modal_class_index - 1]
        else:
            f0 = 0  # No preceding class
        
        # Frequency of succeeding class (f2)
        if modal_class_index < len(freqs) - 1:
            f2 = freqs[modal_class_index + 1]
        else:
            f2 = 0  # No succeeding class

        st.write("**Step 2: Identify Required Values**")
        st.write(f"- L (Lower boundary of modal class) = {L}")
        st.write(f"- f₁ (Frequency of modal class) = {f1}")
        st.write(f"- f₀ (Frequency of preceding class) = {f0}")
        st.write(f"- f₂ (Frequency of succeeding class) = {f2}")
        st.write(f"- h (Class interval width) = {h}")

        # Step 3: Apply formula
        st.write("**Step 3: Apply Mode Formula**")
        
        numerator = f1 - f0
        denominator = 2*f1 - f0 - f2
        
        st.latex(r"Z = " + str(L) + r" + \left(\frac{" + str(f1) + " - " + str(f0) + "}{2 \\times " + str(f1) + " - " + str(f0) + " - " + str(f2) + "}\\right) \\times " + str(h))
        st.latex(r"Z = " + str(L) + r" + \left(\frac{" + str(numerator) + "}{" + str(denominator) + "}\\right) \\times " + str(h))

        if denominator != 0:
            mode_value = L + (numerator / denominator) * h
            st.latex(r"Z = " + str(L) + r" + \left(" + f"{numerator/denominator:.4f}" + r"\right) \\times " + str(h))
            st.latex(r"Z = " + str(L) + r" + " + f"{(numerator/denominator)*h:.4f}")
            st.latex(r"Z = " + f"{mode_value:.4f}")
            
            st.success(f"**Mode (Z) = {mode_value:.4f}**")
            
            # Additional explanation
            st.subheader("💡 Interpretation")
            st.write(f"The mode {mode_value:.4f} represents the value that occurs most frequently in the dataset.")
            st.write(f"It lies in the modal class {intervals[modal_class_index]} with midpoint {values[modal_class_index]:.1f} and frequency {f1}.")
            
        else:
            st.error("Cannot calculate mode: Denominator is zero (2f₁ - f₀ - f₂ = 0)")
            st.write("This occurs when the modal class frequency pattern makes the formula undefined.")
            st.write("In such cases, the mode can be approximated as the midpoint of the modal class:")
            st.write(f"**Approximate Mode ≈ {values[modal_class_index]:.1f}**")

        # Frequency analysis
        st.subheader("📊 Frequency Analysis")
        mode_values = [intervals[i] for i, f in enumerate(freqs) if f == max_freq]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Modal Class", intervals[modal_class_index])
        with col2:
            st.metric("Modal Frequency", max_freq)
        with col3:
            st.metric("Class Width", h)
        
        # Additional analysis
        st.subheader("📈 Distribution Analysis")
        st.write(f"**Total number of classes:** {len(intervals)}")
        st.write(f"**Highest frequency:** {max_freq}")
        st.write(f"**Lowest frequency:** {min(freqs)}")
        st.write(f"**Modal class(es):** {', '.join(mode_values)}")
        
        if len(mode_values) == 1:
            st.write("**Distribution type:** Unimodal")
        elif len(mode_values) == 2:
            st.write("**Distribution type:** Bimodal")
        elif len(mode_values) == 3:
            st.write("**Distribution type:** Trimodal")
        else:
            st.write(f"**Distribution type:** Multimodal ({len(mode_values)} modes)")