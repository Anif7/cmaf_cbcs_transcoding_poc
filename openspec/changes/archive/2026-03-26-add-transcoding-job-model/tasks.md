## 1. Implement TranscodingJob Model

- [x] 1.1 Define `TranscodingJob` in `app/models/transcoding.py`, inheriting from `model_utils.models.TimeStampedModel`.
- [x] 1.2 Define `Status` choices, URL fields, and JSON fields.
- [x] 1.3 Export `TranscodingJob` in `app/models/__init__.py`.

## 2. Database Migrations

- [x] 2.1 Run `python manage.py makemigrations`.
- [x] 2.2 Run `python manage.py migrate`.

## 3. Django Admin Registration

- [x] 3.1 Create `TranscodingJobAdmin` in `app/admin/transcoding.py`.
- [x] 3.2 Register `TranscodingJob` in `app/admin.py` or `app/admin/__init__.py`.
