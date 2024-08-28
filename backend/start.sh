#!/bin/sh

alembic upgrade head
exec python /api/main.py
