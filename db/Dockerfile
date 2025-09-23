# Use the official PostgreSQL image
FROM postgres:16

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=zenonize
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=2P62dm>rDLC8wDI3-:<

# Copy the SQL initialization script
RUN mkdir -p /tmp/psql_data/

COPY zenonize.sql /tmp/psql_data/
COPY init_docker_postgres.sh /docker-entrypoint-initdb.d/
# Ensure the initialization script is executable
RUN chmod +x /docker-entrypoint-initdb.d/init_docker_postgres.sh

# Expose the PostgreSQL default port
EXPOSE 5432
