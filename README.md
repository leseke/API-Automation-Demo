# API Automation Demo

A small, reproducible proof-of-concept for fetching JSON from a REST API, validating the payload, transforming records and exporting clean CSV data.

## What this demonstrates

- HTTP GET requests with timeout handling;
- explicit response validation;
- JSON-to-structured-record transformation;
- filtering and normalization;
- CSV export;
- clear error handling for bad status codes and malformed payloads;
- automated tests without depending on a live third-party service.

## Quick start

```bash
python -m pip install -r requirements.txt
python api_automation.py https://example.com/api/customers output/customers.csv
pytest -q
```

The tests mock the HTTP layer so the proof remains deterministic and safe to reproduce.

## Example client uses

- synchronize data from a supplier or CRM API;
- fetch records on a schedule and export them to CSV;
- normalize inconsistent JSON fields before import;
- connect a small internal workflow to an external service;
- add validation and logging around an existing API process.

## Scope and limitations

This repository demonstrates the integration pattern using generic customer-like records. Real projects may require authentication, pagination, rate-limit handling, retries, webhooks or provider-specific schemas; those are adapted to the target API rather than assumed here.

## Author

Ylan Bitang — automation and data tools.