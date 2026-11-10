# 🌱 Eco E-Commerce Store

An eco-friendly e-commerce web application built with **Python (Flask)**, featuring material-based **Eco Scoring**, sustainable product catalog, dynamic cart management, and seamless checkout.

---

## 🚀 Features

- **Eco Scoring System**: Automatically evaluates environmental sustainability based on product materials (Bamboo, Recycled Plastic, Organic Cotton, Steel, Glass) and assigns an **Eco Grade (A–D)**.
- **Product Catalog & Search**: Browse 30 sustainable products with dynamic search filtering by product name and eco-friendly material.
- **Visual Product Imagery**: Dedicated product illustrations with material badges and eco-score tags.
- **Cart Management**: Add products to cart, update quantities dynamically, and view real-time totals.
- **Dummy Checkout & Feedback**: Seamless checkout workflow with payment processing and customer feedback capture.
- **User Authentication**: Secure session-based register, login, and logout.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Jinja2
- **Frontend**: HTML5, CSS3 (Responsive Flexbox Layout)
- **Image Generation / Assets**: Pillow (PIL)
- **Modeling**: PlantUML (Activity, Architecture, Class, and Use Case Diagrams)

---

## 📁 Project Structure

```text
ecommerce-application/
├── app.py                 # Core Flask application and routing logic
├── generate_images.py     # Procedural eco product image generator
├── static/
│   ├── images/            # 30 product images (product1.jpg - product30.jpg)
│   └── style.css          # Application styles, cards, and animations
├── templates/
│   ├── base.html          # Global layout template with navigation
│   ├── index.html         # Product catalog with search and eco badges
│   ├── login.html         # User login form
│   ├── register.html      # User registration form
│   ├── cart.html          # Shopping cart with quantity management
│   ├── payment.html       # Checkout payment simulation and feedback
│   └── thankyou.html      # Order confirmation and feedback review
└── uml/
    ├── activitydigram.puml
    ├── architecturediagram.puml
    ├── classdigram.puml
    └── usecasediagram.puml
```

---

## 🌿 Eco Score Ratings

| Material | Eco Score | Grade | Environmental Benefit |
| :--- | :---: | :---: | :--- |
| **Bamboo** | **90** | **Grade A** | Fast-growing, biodegradable, renewable |
| **Organic Cotton** | **85** | **Grade A** | Pesticide-free, low chemical impact |
| **Recycled Plastic** | **80** | **Grade B** | Diverts plastic waste from landfills |
| **Glass** | **75** | **Grade B** | 100% recyclable and non-toxic |
| **Steel** | **70** | **Grade C** | Highly durable, infinitely recyclable |
| **Virgin Plastic** | **40** | **Grade D** | High fossil fuel footprint |

---

## ⚙️ Installation & Running Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bhuvanasreesiddi/ecommerce-application.git
   cd ecommerce-application
   ```

2. **Install required dependencies**:
   ```bash
   pip install flask pillow
   ```

3. **Start the Flask server**:
   ```bash
   python app.py
   ```

4. **Open in your browser**:
   Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 👤 Author

- **Bhuvanasree Siddi** - [@bhuvanasreesiddi](https://github.com/bhuvanasreesiddi)
