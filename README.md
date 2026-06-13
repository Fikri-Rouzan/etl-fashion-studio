# ETL Fashion Studio

## 📌 Description

---

## 🛠️ Tech Stack

| Category                    | Technologies Used                                                                                                                        |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 **Programming Language** | `Python`                                                                                                                                 |
| ⚛️ **Libraries**            | `pandas`, `Requests`, `Beautiful Soup 4`, `gspread`, `google-auth`,<br>`SQLAlchemy`, `psycopg2`, `pytest`, `pytest-cov`, `python-dotenv` |
| 🗄️ **Database**             | `PostgreSQL`                                                                                                                             |

---

## ⚙️ Setup Instructions

1. **Prerequisites**
   - Python 3.11 or higher.
   - Git installed on your system.
   - PostgreSQL installed and running on your system.
   - A valid `google-sheets-api.json` credentials file from the Google Cloud Console.

2. **Clone the Repository**

```bash
git clone https://github.com/Fikri-Rouzan/etl-fashion-studio.git
cd etl-fashion-studio
```

3. **Create a Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. **Install Dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure Environment Variables**

```bash
cp .env.example .env
```

- Open the `.env` file and configure the following variables

  ```toml
   SHEET_ID=

   DB_HOST=localhost
   DB_PORT=5432
   DB_DATABASE=
   DB_USERNAME=postgres
   DB_PASSWORD=
  ```

6. **Run the Program**

```bash
python main.py
```

## 🧪 Running Tests

```bash
# Run basic tests
python -m pytest tests

# Run tests with coverage reports
python -m pytest --cov=utils tests/
```
