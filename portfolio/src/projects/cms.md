# Safe Passages Case Management System

## Summary

HIPAA-aligned case management platform that replaces legacy Zoho workflows with a normalized client hub, audit logging, and automated data entry for Safe Passages.

## Highlights

- Refactored a legacy Zoho Creator case management system into a normalized client-hub architecture, converting subform-based records into standalone forms keyed on a permanent Client ID and migrating historical data with Deluge batch scripts.
- Built HIPAA-aligned safeguards into the app: field-level ePHI/PII tagging and encryption, granular team-based permissions, and a custom audit log across create, update, delete, search, and enrollment events that flags deletes and cross-program enrollment.
- Automated the end-to-end data workflow as a data pipeline, replacing manual Excel lookups and copy-paste entry required of every member of an 8+ person team. Search pages with exact and fuzzy (2-of-3) matching on name and date of birth prevent duplicate client records and prefill downstream forms.
- Digitized a paper-based grant program (HHIP) into Zoho forms with conditional show/hide workflows, award-letter tracking, and file-upload document checklists, creating a structured, auditable record where none existed.
- Authored a documentation library (architecture, design rationale, and technical build guides) so future team members can maintain the system after the AmeriCorps term ends.
