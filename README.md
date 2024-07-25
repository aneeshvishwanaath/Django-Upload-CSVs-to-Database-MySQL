# Upload CSVs to Database

This project is a Django-based application that allows users to upload CSV files and merge them into a MySQL database table. It includes a user-friendly interface for uploading files and provides API endpoints for integrating with other systems. Swagger is used for API testing and documentation.

## Features

- Upload CSV files via a web interface
- Merge uploaded CSV data into a MySQL database
- API endpoints for file uploads and data retrieval
- Swagger documentation for easy API testing

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- MySQL 5.7+
- pip

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aneeshvishwanaath/Upload-CSVs-to-Database.git
    cd Upload-CSVs-to-Database
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database settings in `settings.py`:**

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

5. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

## Configuration

### Main Project Configuration (main project urls.py)

In the main project's `urls.py`, include the app URLs:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csv/', include('your_app_name.urls')),  # Replace 'your_app_name' with your app's name
]
```

### App Configuration (app's urls.py)

In your app's `urls.py`, define the URL patterns:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('data/', views.view_data, name='view_data'),
]
```

## Usage

1. **Upload CSV File:**
   - Navigate to `/csv/upload/` to access the upload interface.
   - Select a CSV file and upload it.

2. **View Data:**
   - Navigate to `/csv/data/` to view the merged data from the database.

## API Documentation

### Endpoints

1. **Upload CSV:**
   - **URL:** `/csv/upload/`
   - **Method:** POST
   - **Description:** Uploads a CSV file and merges the data into the database.
   - **Parameters:** `file` (multipart/form-data)

2. **View Data:**
   - **URL:** `/csv/data/`
   - **Method:** GET
   - **Description:** Retrieves the data from the database.

### Swagger

Swagger is used for API documentation and testing. To access the Swagger UI, navigate to `/swagger/`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.

## License

This project is licensed under the MIT License.
