FROM pgvector/pgvector:pg16

# Install required system packages
RUN apt-get update \
    && apt-get install -y python3 python3-pip python3-venv libpq-dev git

# Copy the requirements file into the Docker image
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Path: Dockerfile
COPY . /app
WORKDIR /app

# Copy the entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script when the container starts
ENTRYPOINT ["/entrypoint.sh"]












# FROM pgvector/pgvector:pg16

# # Install python3-venv package
# RUN apt-get update \
#     && apt-get install -y python3-venv

# # Path: Dockerfile
# COPY . /app
# WORKDIR /app

# # Install required system packages
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip libpq-dev git

# # Install any dependencies required for your Python scripts
# RUN apt-get update && apt-get install -y python3 python3-pip

# # Create a virtual environment
# RUN python3 -m venv /venv
# ENV PATH="/venv/bin:$PATH"


# # Setup PostgreSQL tables and database
# RUN service postgresql start && \
#     sleep 10 && \
#     psql -U postgres -c "CREATE DATABASE totem;" && \
#     psql -U postgres -d totem -f /app/sql/schema.sql


# # RUN service postgresql start && \
# #     psql -U postgres -c "CREATE DATABASE totem;" && \
# #     psql -U postgres -d totem -f /app/sql/schema.sql


# # Run Python scripts
# CMD ["python3", "AllMpnetV2.py"]

# # # setup tables
# # RUN psql -U postgres -c "CREATE DATABASE totem;"
# # RUN psql -U postgres -d totem -f /app/sql/schema.sql


# # # Run the AllMpnetV2.py file and the NewQueryTool.py file
# # RUN python3 /app/AllMpnetV2.py
# # RUN python3 /app/NewQueryTool.py
