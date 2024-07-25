from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction, connection
import csv
from io import TextIOWrapper
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter(
            'file',
            openapi.IN_FORM,
            description="Upload CSV file",
            type=openapi.TYPE_FILE,
            required=True
        )
    ],
    responses={201: 'CSV data uploaded successfully'}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def upload_csv(request):
    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return Response({"error": "File is not CSV"}, status=status.HTTP_400_BAD_REQUEST)

    table_name = "csvdata"

    csv_file = TextIOWrapper(file.file, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file)

    # Create table schema if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        ac_year VARCHAR(10),
        age INT,
        state_cd VARCHAR(10),
        state_name VARCHAR(255),
        district_cd VARCHAR(10),
        district_name VARCHAR(255),
        class_1_boys INT,
        class_2_boys INT,
        class_3_boys INT,
        class_4_boys INT,
        class_5_boys INT,
        class_6_boys INT,
        class_7_boys INT,
        class_8_boys INT,
        class_9_boys INT,
        class_10_boys INT,
        class_11_boys INT,
        class_12_boys INT,
        class_1_girls INT,
        class_2_girls INT,
        class_3_girls INT,
        class_4_girls INT,
        class_5_girls INT,
        class_6_girls INT,
        class_7_girls INT,
        class_8_girls INT,
        class_9_girls INT,
        class_10_girls INT,
        class_11_girls INT,
        class_12_girls INT
    )
    """

    with connection.cursor() as cursor:
        cursor.execute(create_table_query)

        try:
            with transaction.atomic():
                for row in csv_reader:
                    cursor.execute(f"""
                        INSERT INTO {table_name} (
                            ac_year, age, state_cd, state_name, district_cd, district_name,
                            class_1_boys, class_2_boys, class_3_boys, class_4_boys, class_5_boys,
                            class_6_boys, class_7_boys, class_8_boys, class_9_boys, class_10_boys,
                            class_11_boys, class_12_boys, class_1_girls, class_2_girls, class_3_girls,
                            class_4_girls, class_5_girls, class_6_girls, class_7_girls, class_8_girls,
                            class_9_girls, class_10_girls, class_11_girls, class_12_girls
                        ) VALUES (
                            %(ac_year)s, %(age)s, %(state_cd)s, %(state_name)s, %(district_cd)s, %(district_name)s,
                            %(class_1_boys)s, %(class_2_boys)s, %(class_3_boys)s, %(class_4_boys)s, %(class_5_boys)s,
                            %(class_6_boys)s, %(class_7_boys)s, %(class_8_boys)s, %(class_9_boys)s, %(class_10_boys)s,
                            %(class_11_boys)s, %(class_12_boys)s, %(class_1_girls)s, %(class_2_girls)s, %(class_3_girls)s,
                            %(class_4_girls)s, %(class_5_girls)s, %(class_6_girls)s, %(class_7_girls)s, %(class_8_girls)s,
                            %(class_9_girls)s, %(class_10_girls)s, %(class_11_girls)s, %(class_12_girls)s
                        )
                    """, row)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "CSV data uploaded successfully", "table_name": table_name},
                    status=status.HTTP_201_CREATED)

# The file's content is processed directly from this in-memory representation without being saved to the file system. Here's a detailed explanation of how the process works:
# File Upload: The file is uploaded via an HTTP POST request to the API endpoint, and Django handles the file upload. The file is temporarily stored in memory.
# File Reading: The TextIOWrapper is used to read the file content. This is done directly from the in-memory file object (file.file) provided by Django.
# Processing the File: The CSV reader processes the file line by line. Each row of the CSV is inserted into the database table csvdata.
# Memory Management: Once the file content is read and processed, the temporary in-memory file is automatically managed by Django. There's no need to manually delete the file, as Django's file handling system takes care of it.
#
# csv_file = TextIOWrapper(file.file, encoding='utf-8')
# csv_reader = csv.DictReader(csv_file)



@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'ac_year',
            openapi.IN_QUERY,
            description="Academic year",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'state_name',
            openapi.IN_QUERY,
            description="State name",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="Limit the number of rows",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={200: 'Data retrieved successfully'}
)
@api_view(['GET'])
def get_filtered_data(request):
    table_name = "csvdata"
    ac_year = request.GET.get('ac_year')
    state_name = request.GET.get('state_name')
    limit = request.GET.get('limit')

    query = f"SELECT * FROM {table_name} WHERE 1=1"
    params = {}

    if ac_year:
        query += " AND ac_year = %(ac_year)s"
        params['ac_year'] = ac_year

    if state_name:
        query += " AND state_name = %(state_name)s"
        params['state_name'] = state_name

    if limit:
        query += " LIMIT %(limit)s"
        params['limit'] = int(limit)  # Ensure limit is treated as an integer

    # Debug print
    print("Executing query:", query)
    print("With parameters:", params)

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            # Generate HTML content
            html = "<html><body><h2>Filtered Data</h2><table border='1' style='border-collapse:collapse;'>"
            # Add table header
            html += "<tr>"
            for column in columns:
                html += f"<th style='padding: 5px;'>{column}</th>"
            html += "</tr>"
            # Add table rows
            for row in rows:
                html += "<tr>"
                for value in row:
                    html += f"<td style='padding: 5px;'>{value}</td>"
                html += "</tr>"
            html += "</table></body></html>"

            return Response(html, status=status.HTTP_200_OK, content_type="text/html")
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
