# Use the official PostgreSQL image
FROM postgres:16

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=zenonize
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=2P62dm>rDLC8wDI3-:<

# Copy initialization files
# COPY zenonize.sql /docker-entrypoint-initdb.d/01-schema.sql
COPY zenonize.sql /docker-entrypoint-initdb.d/init.sql

# Expose the PostgreSQL default port
EXPOSE 5432
