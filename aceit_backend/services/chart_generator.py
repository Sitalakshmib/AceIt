"""
Chart Generator Service for Data Interpretation Questions

Generates precise, probability-distribution-aware charts for DI questions using QuickChart.io API.

Chart Types:
1. Bar Chart (PMF) - Shows probability mass with exact heights summing to 1
2. Line Chart (PDF/CDF) - Shows continuous distributions with area annotations
3. Pie Chart - Shows composition with exact percentages and angles

Key Features:
- Precise probability labels on each data point
- Percentage annotations for easy calculation
- Grid lines with exact measurement markers
- Clear axis labels with units
- Data tables embedded when needed
"""

import json
import random
import urllib.parse
from typing import Dict, List, Optional, Tuple


class ChartGenerator:
    """
    Generates QuickChart.io URLs for Data Interpretation questions
    with precise probability distribution formatting.
    """
    
    BASE_URL = "https://quickchart.io/chart"
    
    # Color palettes for probability distributions
    COLORS = {
        "bar": [
            "rgba(54, 162, 235, 0.85)",   # Blue
            "rgba(255, 99, 132, 0.85)",   # Red
            "rgba(75, 192, 192, 0.85)",   # Teal
            "rgba(255, 206, 86, 0.85)",   # Yellow
            "rgba(153, 102, 255, 0.85)",  # Purple
            "rgba(255, 159, 64, 0.85)",   # Orange
        ],
        "line": "rgba(75, 192, 192, 1)",
        "pie": [
            "#FF6384", "#36A2EB", "#FFCE56", 
            "#4BC0C0", "#9966FF", "#FF9F40", "#7CFC00"
        ]
    }
    
    # ==========================
    # BAR CHART (Probability Mass Function)
    # ==========================
    @classmethod
    def generate_bar_chart(
        cls,
        labels: List[str],
        values: List[float],
        title: str = "Probability Distribution",
        y_label: str = "Probability P(X=x)",
        show_percentages: bool = True,
        show_values: bool = True,
        normalize_to_probability: bool = False
    ) -> str:
        """
        Generate a bar chart suitable for discrete probability distributions.
        
        Args:
            labels: Category labels (X-axis)
            values: Values for each category
            title: Chart title
            y_label: Y-axis label
            show_percentages: Display percentage on each bar
            show_values: Display exact value on each bar
            normalize_to_probability: If True, normalize values to sum to 1
        
        Returns:
            QuickChart URL string
        """
        # Normalize if requested (for probability distributions)
        if normalize_to_probability:
            total = sum(values)
            values = [round(v / total, 4) for v in values]
        
        # Calculate percentages
        total = sum(values)
        percentages = [round((v / total) * 100, 1) for v in values]
        
        # Create data labels showing value + percentage
        data_labels = []
        for i, (v, p) in enumerate(zip(values, percentages)):
            if show_values and show_percentages:
                data_labels.append(f"{v} ({p}%)")
            elif show_percentages:
                data_labels.append(f"{p}%")
            elif show_values:
                data_labels.append(str(v))
            else:
                data_labels.append("")
        
        chart_config = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": title,
                    "data": values,
                    "backgroundColor": cls.COLORS["bar"][:len(values)],
                    "borderColor": "white",
                    "borderWidth": 2,
                    "borderRadius": 4
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title,
                        "font": {"size": 16, "weight": "bold"},
                        "color": "#333",
                        "padding": 15
                    },
                    "legend": {"display": False},
                    "datalabels": {
                        "display": True,
                        "anchor": "end",
                        "align": "top",
                        "color": "#333",
                        "font": {"size": 11, "weight": "bold"},
                        "formatter": "function(value, context) { return '" + "', '".join(data_labels) + "'.split(', ')[context.dataIndex]; }"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": y_label,
                            "font": {"size": 12}
                        },
                        "grid": {
                            "color": "rgba(0,0,0,0.1)",
                            "lineWidth": 1
                        },
                        "ticks": {
                            "font": {"size": 11},
                            "stepSize": max(values) / 5 if max(values) > 0 else 1
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Categories",
                            "font": {"size": 12}
                        },
                        "grid": {"display": False},
                        "ticks": {"font": {"size": 11}}
                    }
                },
                "layout": {"padding": 20}
            }
        }
        
        return cls._build_url(chart_config, width=650, height=450)
    
    # ==========================
    # LINE CHART (PDF / CDF / Trend)
    # ==========================
    @classmethod
    def generate_line_chart(
        cls,
        x_values: List,
        y_values: List[float],
        title: str = "Trend Analysis",
        x_label: str = "X",
        y_label: str = "Y",
        show_area: bool = False,
        show_points: bool = True,
        show_values: bool = True
    ) -> str:
        """
        Generate a line chart for continuous data or trends.
        
        Args:
            x_values: X-axis values (can be strings or numbers)
            y_values: Y-axis values
            title: Chart title
            x_label: X-axis label
            y_label: Y-axis label
            show_area: Fill area under the curve (for PDF visualization)
            show_points: Show data points
            show_values: Show value labels on points
        
        Returns:
            QuickChart URL string
        """
        chart_config = {
            "type": "line",
            "data": {
                "labels": x_values,
                "datasets": [{
                    "label": title,
                    "data": y_values,
                    "borderColor": cls.COLORS["line"],
                    "backgroundColor": "rgba(75, 192, 192, 0.3)" if show_area else "transparent",
                    "fill": show_area,
                    "tension": 0.3,
                    "pointRadius": 5 if show_points else 0,
                    "pointBackgroundColor": cls.COLORS["line"],
                    "pointBorderColor": "white",
                    "pointBorderWidth": 2
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title,
                        "font": {"size": 16, "weight": "bold"},
                        "color": "#333",
                        "padding": 15
                    },
                    "legend": {"display": True, "position": "bottom"},
                    "datalabels": {
                        "display": show_values,
                        "anchor": "end",
                        "align": "top",
                        "color": "#333",
                        "font": {"size": 10}
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": y_label,
                            "font": {"size": 12}
                        },
                        "grid": {
                            "color": "rgba(0,0,0,0.1)",
                            "lineWidth": 1
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": x_label,
                            "font": {"size": 12}
                        },
                        "grid": {
                            "color": "rgba(0,0,0,0.05)"
                        }
                    }
                },
                "layout": {"padding": 20}
            }
        }
        
        return cls._build_url(chart_config, width=700, height=450)
    
    # ==========================
    # PIE CHART (Composition)
    # ==========================
    @classmethod
    def generate_pie_chart(
        cls,
        labels: List[str],
        values: List[float],
        title: str = "Distribution",
        show_percentages: bool = False,
        show_angles: bool = False
    ) -> str:
        """
        Generate a pie chart showing composition/probability distribution.
        
        Args:
            labels: Category labels
            values: Values for each slice
            title: Chart title
            show_percentages: Show percentage on each slice
            show_angles: Show degree angles for competitive exam calculations
        
        Returns:
            QuickChart URL string
        """
        total = sum(values)
        percentages = [round((v / total) * 100, 1) for v in values]
        angles = [round((v / total) * 360, 1) for v in values]
        
        # Create enhanced labels with percentage and optionally angle
        enhanced_labels = []
        for i, (label, pct, angle) in enumerate(zip(labels, percentages, angles)):
            if show_percentages and show_angles:
                enhanced_labels.append(f"{label}: {pct}% ({angle}°)")
            elif show_percentages:
                enhanced_labels.append(f"{label}: {pct}%")
            else:
                enhanced_labels.append(label)
        
        chart_config = {
            "type": "pie",
            "data": {
                "labels": enhanced_labels,
                "datasets": [{
                    "data": values,
                    "backgroundColor": cls.COLORS["pie"][:len(values)],
                    "borderColor": "white",
                    "borderWidth": 3
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": [title, f"Total: {total}"],
                        "font": {"size": 16, "weight": "bold"},
                        "color": "#333",
                        "padding": 15
                    },
                    "legend": {
                        "display": True,
                        "position": "right",
                        "labels": {
                            "font": {"size": 11},
                            "padding": 15,
                            "usePointStyle": True
                        }
                    },
                    "datalabels": {
                        "display": True,
                        "color": "#fff",
                        "font": {"size": 12, "weight": "bold"},
                        "textShadowBlur": 4,
                        "textShadowColor": "rgba(0,0,0,0.5)"
                    }
                },
                "layout": {"padding": 10}
            }
        }
        
        return cls._build_url(chart_config, width=600, height=450)
    
    # ==========================
    # SPECIALIZED CHART GENERATORS
    # ==========================
    @classmethod
    def generate_probability_bar(
        cls,
        outcomes: List[str],
        probabilities: List[float],
        title: str = "Probability Mass Function P(X=x)"
    ) -> str:
        """
        Generate a proper PMF bar chart where heights sum to 1.
        """
        # Ensure probabilities sum to 1
        total = sum(probabilities)
        if abs(total - 1.0) > 0.01:
            probabilities = [p / total for p in probabilities]
        
        return cls.generate_bar_chart(
            labels=outcomes,
            values=probabilities,
            title=title,
            y_label="P(X=x)",
            show_percentages=True,
            show_values=True,
            normalize_to_probability=False
        )
    
    @classmethod
    def generate_comparative_bar(
        cls,
        labels: List[str],
        datasets: List[Dict],
        title: str = "Comparative Analysis"
    ) -> str:
        """
        Generate grouped bar chart for comparing multiple datasets.
        
        Args:
            labels: X-axis labels
            datasets: List of {"name": str, "values": List[float]}
        """
        chart_datasets = []
        for i, ds in enumerate(datasets):
            # Calculate percentages for each dataset
            total = sum(ds["values"])
            pct = [round((v/total)*100, 1) for v in ds["values"]]
            
            chart_datasets.append({
                "label": ds["name"],
                "data": ds["values"],
                "backgroundColor": cls.COLORS["bar"][i % len(cls.COLORS["bar"])],
                "borderColor": "white",
                "borderWidth": 1
            })
        
        chart_config = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": chart_datasets
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title,
                        "font": {"size": 16, "weight": "bold"}
                    },
                    "legend": {
                        "display": True,
                        "position": "bottom"
                    },
                    "datalabels": {
                        "display": True,
                        "anchor": "end",
                        "align": "top",
                        "font": {"size": 9}
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "grid": {"color": "rgba(0,0,0,0.1)"}
                    },
                    "x": {
                        "grid": {"display": False}
                    }
                }
            }
        }
        
        return cls._build_url(chart_config, width=700, height=450)
    
    # ==========================
    # HELPER: Build URL
    # ==========================
    @classmethod
    def _build_url(cls, chart_config: Dict, width: int = 600, height: int = 400) -> str:
        """
        Build the QuickChart URL from config.
        """
        json_str = json.dumps(chart_config, separators=(',', ':'))
        encoded = urllib.parse.quote(json_str, safe='')
        return f"{cls.BASE_URL}?c={encoded}&w={width}&h={height}&bkg=white&devicePixelRatio=2"


# ==========================
# DI QUESTION DATA GENERATORS
# ==========================
class DIDataGenerator:
    """
    Generates realistic data scenarios for Data Interpretation questions.
    """
    
    # Scenario templates for probability-based questions
    SCENARIOS = {
        "bar": [
            {
                "context": "Survey Results",
                "labels": ["Agree", "Disagree", "Neutral", "No Opinion"],
                "unit": "Respondents",
                "generate": lambda: [random.randint(50, 200) for _ in range(4)]
            },
            {
                "context": "Product Sales Distribution",
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "unit": "Units (thousands)",
                "generate": lambda: [random.randint(100, 500) for _ in range(4)]
            },
            {
                "context": "Defect Rate by Factory",
                "labels": ["Factory A", "Factory B", "Factory C", "Factory D"],
                "unit": "Defects per 1000 units",
                "generate": lambda: [round(random.uniform(2, 15), 1) for _ in range(4)]
            },
            {
                "context": "Student Grade Distribution",
                "labels": ["A", "B", "C", "D", "F"],
                "unit": "Number of Students",
                "generate": lambda: [random.randint(10, 80) for _ in range(5)]
            },
            {
                "context": "Budget Allocation (₹ Lakhs)",
                "labels": ["R&D", "Marketing", "Operations", "HR", "IT"],
                "unit": "₹ Lakhs",
                "generate": lambda: [random.randint(50, 300) for _ in range(5)]
            }
        ],
        "line": [
            {
                "context": "Monthly Revenue Trend",
                "x_values": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "unit": "₹ Lakhs",
                "generate": lambda: [random.randint(100, 300) for _ in range(6)]
            },
            {
                "context": "Temperature Variation",
                "x_values": ["6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"],
                "unit": "°C",
                "generate": lambda: [round(random.uniform(20, 40), 1) for _ in range(6)]
            },
            {
                "context": "Stock Price Movement",
                "x_values": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                "unit": "₹",
                "generate": lambda: [round(random.uniform(100, 200), 2) for _ in range(5)]
            },
            {
                "context": "Population Growth",
                "x_values": ["2018", "2019", "2020", "2021", "2022", "2023"],
                "unit": "Millions",
                "generate": lambda: [round(random.uniform(1.2, 1.5), 2) for _ in range(6)]
            }
        ],
        "pie": [
            {
                "context": "Market Share Distribution",
                "labels": ["Company A", "Company B", "Company C", "Others"],
                "unit": "%",
                "generate": lambda: DIDataGenerator._generate_pie_data(4)
            },
            {
                "context": "Household Expenditure",
                "labels": ["Food", "Rent", "Transport", "Education", "Others"],
                "unit": "%",
                "generate": lambda: DIDataGenerator._generate_pie_data(5)
            },
            {
                "context": "Time Allocation (24 hours)",
                "labels": ["Sleep", "Work", "Commute", "Leisure", "Meals"],
                "unit": "hours",
                "generate": lambda: [random.randint(4, 9), random.randint(7, 10), random.randint(1, 3), random.randint(2, 5), random.randint(1, 3)]
            },
            {
                "context": "Energy Source Distribution",
                "labels": ["Coal", "Solar", "Wind", "Hydro", "Nuclear"],
                "unit": "%",
                "generate": lambda: DIDataGenerator._generate_pie_data(5)
            }
        ]
    }
    
    @staticmethod
    def _generate_pie_data(n: int) -> List[int]:
        """Generate n values that sum to approximately 100."""
        values = [random.randint(10, 40) for _ in range(n-1)]
        values.append(100 - sum(values))
        if values[-1] < 5:
            values[-1] = random.randint(5, 15)
        return values
    
    @classmethod
    def generate_bar_question_data(cls) -> Dict:
        """Generate complete data for a bar chart DI question."""
        scenario = random.choice(cls.SCENARIOS["bar"])
        values = scenario["generate"]()
        
        chart_url = ChartGenerator.generate_bar_chart(
            labels=scenario["labels"],
            values=values,
            title=scenario["context"],
            y_label=scenario["unit"],
            show_percentages=True,
            show_values=True
        )
        
        total = sum(values)
        percentages = [round((v/total)*100, 1) for v in values]
        
        return {
            "context": scenario["context"],
            "labels": scenario["labels"],
            "values": values,
            "percentages": percentages,
            "total": total,
            "unit": scenario["unit"],
            "chart_url": chart_url
        }
    
    @classmethod
    def generate_line_question_data(cls) -> Dict:
        """Generate complete data for a line chart DI question."""
        scenario = random.choice(cls.SCENARIOS["line"])
        values = scenario["generate"]()
        
        chart_url = ChartGenerator.generate_line_chart(
            x_values=scenario["x_values"],
            y_values=values,
            title=scenario["context"],
            x_label="Time Period",
            y_label=scenario["unit"],
            show_area=False,
            show_points=True,
            show_values=True
        )
        
        return {
            "context": scenario["context"],
            "x_values": scenario["x_values"],
            "values": values,
            "unit": scenario["unit"],
            "max_value": max(values),
            "min_value": min(values),
            "avg_value": round(sum(values)/len(values), 2),
            "chart_url": chart_url
        }
    
    @classmethod
    def generate_pie_question_data(cls) -> Dict:
        """Generate complete data for a pie chart DI question."""
        scenario = random.choice(cls.SCENARIOS["pie"])
        values = scenario["generate"]()
        
        chart_url = ChartGenerator.generate_pie_chart(
            labels=scenario["labels"],
            values=values,
            title=scenario["context"]
        )
        
        total = sum(values)
        percentages = [round((v/total)*100, 1) for v in values]
        angles = [round((v/total)*360, 1) for v in values]
        
        return {
            "context": scenario["context"],
            "labels": scenario["labels"],
            "values": values,
            "percentages": percentages,
            "angles": angles,
            "total": total,
            "unit": scenario["unit"],
            "chart_url": chart_url
        }


# Quick test
if __name__ == "__main__":
    print("=== Testing Chart Generator ===\n")
    
    # Test Bar Chart
    bar_data = DIDataGenerator.generate_bar_question_data()
    print(f"Bar Chart Context: {bar_data['context']}")
    print(f"Labels: {bar_data['labels']}")
    print(f"Values: {bar_data['values']}")
    print(f"Percentages: {bar_data['percentages']}")
    print(f"URL: {bar_data['chart_url'][:100]}...")
    print()
    
    # Test Line Chart
    line_data = DIDataGenerator.generate_line_question_data()
    print(f"Line Chart Context: {line_data['context']}")
    print(f"X Values: {line_data['x_values']}")
    print(f"Y Values: {line_data['values']}")
    print(f"URL: {line_data['chart_url'][:100]}...")
    print()
    
    # Test Pie Chart
    pie_data = DIDataGenerator.generate_pie_question_data()
    print(f"Pie Chart Context: {pie_data['context']}")
    print(f"Labels: {pie_data['labels']}")
    print(f"Values: {pie_data['values']}")
    print(f"Angles: {pie_data['angles']}")
    print(f"URL: {pie_data['chart_url'][:100]}...")
