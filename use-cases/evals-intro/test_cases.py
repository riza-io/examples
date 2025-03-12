from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DataTransformationTestCase:
    id: str
    name: str
    description: str
    csv_sample: str
    csv_full: str
    desired_schema: Dict[str, Any]
    expected_json_out: Dict[str, Any]


# Desired output schemas

STANDARD_SCHEMA = {
    "type": "object",
    "properties": {
        "appraisers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "license": {"type": "string"}
                }
            }
        }
    }
}


# Test 1: Basic CSV -> JSON transform

BASIC_CSV_SUBSET = """License,Name,Company,Address,City,State,Zip,County,Phone
001507,"Smith, Amy",Amy Smith Inc.,1830 Castillo St,Santa Barbara,CA,93101,Santa Barbara,(123) 456-7890
001508,"Smith, Bob",Bob Smith Inc.,1458 Sutter St,San Francisco,CA,94109,San Francisco,(987) 654-3210"""

BASIC_CSV_FULL = "\n".join(
    [BASIC_CSV_SUBSET,
    """001509,"Johnson, Chris",Chris Johnson LLC,2500 Main St,Los Angeles,CA,90016,Los Angeles,(310) 555-1234
001510,"Davis, Emily",Emily Davis Co.,785 Market St,San Francisco,CA,94103,San Francisco,(415) 555-5678
001511,"Miller, Jason",Miller Enterprises,620 State St,Santa Barbara,CA,93101,Santa Barbara,(805) 555-9012"""])

TEST_CASE_BASIC = DataTransformationTestCase(
    id="basic-transform-001",
    name="Basic data transformation",
    description="Transform from CSV to JSON with three fields",
    csv_sample=BASIC_CSV_SUBSET,
    csv_full=BASIC_CSV_FULL,
    desired_schema=STANDARD_SCHEMA,
    expected_json_out={
        "appraisers": [
            {"name": "Smith, Amy", "phone": "(123) 456-7890", "license": "001507"},
            {"name": "Smith, Bob", "phone": "(987) 654-3210", "license": "001508"},
            {"name": "Johnson, Chris", "phone": "(310) 555-1234", "license": "001509"},
            {"name": "Davis, Emily", "phone": "(415) 555-5678", "license": "001510"},
            {"name": "Miller, Jason", "phone": "(805) 555-9012", "license": "001511"},
        ]
    }
)


# Test 2: Missing fields in the CSV data

MISSING_FIELDS_CSV_SUBSET = """License,Name,Company,Address,City,State,Zip,County,Phone
001507,"Smith, Amy",Amy Smith Inc.,1830 Castillo St,Santa Barbara,CA,93101,Santa Barbara,(123) 456-7890
001508,"Smith, Bob",Bob Smith Inc.,1458 Sutter St,San Francisco,CA,94109,San Francisco,
,"Johnson, Carl",,123 Main St,Los Angeles,CA,90001,Los Angeles,(555) 123-4567"""

MISSING_FIELDS_CSV_FULL = "\n".join(
    [MISSING_FIELDS_CSV_SUBSET,
    """001509,"Williams, Sarah",,500 Elm St,San Diego,CA,92101,San Diego,(619) 555-7890
001510,"Brown, David",Brown Consulting,,Sacramento,CA,95814,,(916) 555-2345
,"Taylor, Jessica",Jessica Taylor LLC,742 Oak Ave,San Jose,CA,,Santa Clara,(408) 555-6789"""])

TEST_CASE_MISSING_FIELDS = DataTransformationTestCase(
    id="missing-data-001",
    name="Missing data in CSV",
    description="Test handling missing data for some fields",
    csv_sample=MISSING_FIELDS_CSV_SUBSET,
    csv_full=MISSING_FIELDS_CSV_FULL,
    desired_schema=STANDARD_SCHEMA,
    expected_json_out={
        "appraisers": [
            {"name": "Smith, Amy", "phone": "(123) 456-7890", "license": "001507"},
            {"name": "Smith, Bob", "phone": "", "license": "001508"},
            {"name": "Johnson, Carl", "phone": "(555) 123-4567", "license": ""},
            {"name": "Williams, Sarah", "phone": "(619) 555-7890", "license": "001509"},
            {"name": "Brown, David", "phone": "(916) 555-2345", "license": "001510"},
            {"name": "Taylor, Jessica", "phone": "(408) 555-6789", "license": ""},
        ]
    }
)


# Test 3: Nested output schema

NESTED_SCHEMA = {
    "type": "object",
    "properties": {
        "licensees": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fullName": {"type": "string"},
                    "contactInfo": {
                        "type": "object",
                        "properties": {
                            "phone": {"type": "string"},
                            "address": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "zip": {"type": "string"}
                        }
                    },
                    "licenseNumber": {"type": "string"}
                }
            }
        }
    }
}

TEST_CASE_SCHEMA_VARIATION = DataTransformationTestCase(
    id="schema-variation-001",
    name="Nested schema transformation",
    description="Transform to a nested JSON schema",
    csv_sample=BASIC_CSV_SUBSET,
    csv_full=BASIC_CSV_FULL,
    desired_schema=NESTED_SCHEMA,
    expected_json_out={
        "licensees": [
            {
                "fullName": "Smith, Amy",
                "contactInfo": {
                    "phone": "(123) 456-7890",
                    "address": "1830 Castillo St",
                    "city": "Santa Barbara",
                    "state": "CA",
                    "zip": "93101"
                },
                "licenseNumber": "001507"
            },
            {
                "fullName": "Smith, Bob",
                "contactInfo": {
                    "phone": "(987) 654-3210",
                    "address": "1458 Sutter St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94109"
                },
                "licenseNumber": "001508"
            },
            {
                "fullName": "Johnson, Chris",
                "contactInfo": {
                    "phone": "(310) 555-1234",
                    "address": "2500 Main St",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90016"
                },
                "licenseNumber": "001509"
            },
            {
                "fullName": "Davis, Emily",
                "contactInfo": {
                    "phone": "(415) 555-5678",
                    "address": "785 Market St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94103"
                },
                "licenseNumber": "001510"
            },
            {
                "fullName": "Miller, Jason",
                "contactInfo": {
                    "phone": "(805) 555-9012",
                    "address": "620 State St",
                    "city": "Santa Barbara",
                    "state": "CA",
                    "zip": "93101"
                },
                "licenseNumber": "001511"
            }
        ]
    }
)


# Test 4: Pipe-delimited CSV format

PIPE_CSV_SUBSET = """License|Name|Company|Address|City|State|Zip|County|Phone
001507|"Smith, Amy"|Amy Smith Inc.|1830 Castillo St|Santa Barbara|CA|93101|Santa Barbara|(123) 456-7890
001508|"Smith, Bob"|Bob Smith Inc.|1458 Sutter St|San Francisco|CA|94109|San Francisco|(987) 654-3210"""

PIPE_CSV_FULL = "\n".join(
    [PIPE_CSV_SUBSET,
    """001509|"Johnson, Chris"|Chris Johnson LLC|2500 Main St|Los Angeles|CA|90016|Los Angeles|(310) 555-1234
001510|"Davis, Emily"|Emily Davis Co.|785 Market St|San Francisco|CA|94103|San Francisco|(415) 555-5678
001511|"Miller, Jason"|Miller Enterprises|620 State St|Santa Barbara|CA|93101|Santa Barbara|(805) 555-9012"""])

TEST_CASE_CSV_FORMAT_VARIATION = DataTransformationTestCase(
    id="csv-format-variation-001",
    name="CSV with pipe delimiter",
    description="Transform data from pipe-delimited format",
    csv_sample=PIPE_CSV_SUBSET,
    csv_full=PIPE_CSV_FULL,
    desired_schema=STANDARD_SCHEMA,
    expected_json_out={
        "appraisers": [
            {"name": "Smith, Amy", "phone": "(123) 456-7890", "license": "001507"},
            {"name": "Smith, Bob", "phone": "(987) 654-3210", "license": "001508"},
            {"name": "Johnson, Chris", "phone": "(310) 555-1234", "license": "001509"},
            {"name": "Davis, Emily", "phone": "(415) 555-5678", "license": "001510"},
            {"name": "Miller, Jason", "phone": "(805) 555-9012", "license": "001511"}
        ]
    }
)


ALL_TEST_CASES = [
  TEST_CASE_BASIC,
  TEST_CASE_MISSING_FIELDS,
  TEST_CASE_SCHEMA_VARIATION,
]
