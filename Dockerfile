# Dockerfile

# Stage 1: Use an official Python slim image for a smaller footprint.
FROM python:3.11-slim

# Stage 2: Set the working directory inside the container.
WORKDIR /app

# Stage 3: Copy and install dependencies.
# This is done in a separate step to leverage Docker's layer caching.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Stage 4: Copy the application source code into the container.
COPY . .

# Stage 5: Expose the port the app will run on.
EXPOSE 8000

# Stage 6: Define the command to run the application.
# The --host 0.0.0.0 flag makes the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
