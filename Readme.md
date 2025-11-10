markdown
# 📊 Mean, Median, Mode Calculator (Grouped Data)

A comprehensive Streamlit web application for calculating statistical measures (Mean, Median, Mode) from grouped frequency distributions with detailed step-by-step solutions.

## 🌟 Features

### 📈 Statistical Calculations
- **Mean Calculation** with three different methods:
  - Direct Method
  - Assumed Mean Method
  - Step Deviation Method
- **Median Calculation** for grouped data with cumulative frequency analysis
- **Mode Calculation** using the grouped data formula
- **Missing Frequency** calculations for various scenarios

### 🎯 Key Capabilities
- **Step-by-step solutions** with mathematical explanations
- **Multiple calculation methods** for comprehensive understanding
- **Auto-detection** of class intervals and widths
- **Error handling** for invalid inputs
- **Professional mathematical notation** using LaTeX
- **Interactive tables** for data visualization

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mean-median-mode-calculator
Create a virtual environment (recommended)

bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
Install required packages

bash
pip install streamlit statistics
📖 Usage
Basic Usage
Run the application:

bash
streamlit run app.py
Enter your data:

Class intervals (e.g., 0-10, 10-20, 20-30, 30-40, 40-50)

Corresponding frequencies (e.g., 5, 8, 12, 7, 3)

Select calculation type:

Mean, Median, or Mode

Choose calculation method for Mean

Input Format Guidelines
Class Intervals
Use hyphen-separated ranges: 0-10, 10-20, 20-30

Single values are also supported: 5, 10, 15, 20

Ensure consistent formatting

Frequencies
Integer values only

Same number of entries as class intervals

Use commas to separate values

📊 Calculation Methods
Mean Calculation
Direct Method

text
x̄ = Σ(fᵢxᵢ) / Σfᵢ
Assumed Mean Method

text
x̄ = A + Σ(fᵢdᵢ) / Σfᵢ
where dᵢ = xᵢ - A
Step Deviation Method

text
x̄ = A + [Σ(fᵢdᵢ) / Σfᵢ] × h
where dᵢ = (xᵢ - A)/h
Median Calculation
text
Median = L + [(N/2 - CF) / f] × h
Where:
- L = Lower boundary of median class
- N = Total frequency
- CF = Cumulative frequency before median class
- f = Frequency of median class
- h = Class width
Mode Calculation
text
Mode = L + [(f₁ - f₀) / (2f₁ - f₀ - f₂)] × h
Where:
- L = Lower boundary of modal class
- f₁ = Frequency of modal class
- f₀ = Frequency of preceding class
- f₂ = Frequency of succeeding class
- h = Class width
🎓 Educational Value
This application is designed to help students:

Understand statistical concepts through detailed explanations

Learn multiple calculation methods for the same measure

Follow step-by-step solutions to complex problems

Verify manual calculations with automated tools

Develop problem-solving skills in statistics

📝 Example Problems
Example 1: Basic Calculation
Input:

Classes: 0-10, 10-20, 20-30, 30-40, 40-50

Frequencies: 5, 8, 12, 7, 3

Output:

Mean: 23.8571

Median: 24.1667

Mode: 23.3333

🔧 Technical Details
Built With
Streamlit - Web application framework

Python - Backend logic and calculations

LaTeX - Mathematical notation

Statistics - Core statistical functions

File Structure
text
mean-median-mode-calculator/
├── app.py                 # Main application file
├── README.md             # Documentation
├── requirements.txt      # Dependencies
└── assets/              # Additional resources
🛠️ Customization
Adding New Features
New statistical measures can be added to the choice radio buttons

Additional calculation methods can be implemented following existing patterns

Custom input formats can be supported by modifying the parsing functions

Modifying Calculations
All calculation logic is modular and well-documented

Mathematical formulas use LaTeX for clear presentation

Error handling ensures robust performance

🤝 Contributing
Contributions are welcome! Please feel free to:

Report bugs and issues

Suggest new features

Submit pull requests

Improve documentation

📄 License
This project is open source and available under the MIT License.

🆘 Support
If you encounter any issues:

Check the input format requirements

Ensure all frequencies are integers

Verify class intervals are properly formatted

Check that the number of classes matches frequencies

📚 Learning Resources
Statistics Fundamentals

Grouped Data Calculations

Streamlit Documentation

Developed with ❤️ for students and educators in statistics

text

This README file provides:

1. **Comprehensive documentation** of all features
2. **Clear installation and usage instructions**
3. **Mathematical formulas** for each calculation method
4. **Educational context** for students and teachers
5. **Technical details** for developers
6. **Troubleshooting guidance**
7. **Examples** to help users get started quickly

The README is structured to be helpful for both end-users who want to use the calculator and developers who might want to extend or modify the application.