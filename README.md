# ETL Fashion Studio

## ℹ️ About

## 🛠️ Technologies Used

- 🌐 **Programming Language:** Python.
- ⚛️ **Libraries:** pandas, Requests, Beautiful Soup 4, lxml, gspread, google-auth, SQLAlchemy, psycopg2, pytest, pytest-cov, and python-dotenv.
- 🗄️ **Database:** PostgreSQL.
- 💻 **Software:** Visual Studio Code.

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Fikri-Rouzan/etl-fashion-studio.git

# Navigate to the project directory
cd etl-fashion-studio

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the program
python main.py

# Run the test program
python -m pytest tests

# Run the test program with coverage reports
python -m pytest --cov=utils tests/
```
