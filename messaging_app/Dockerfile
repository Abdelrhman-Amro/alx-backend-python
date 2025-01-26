FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Command to run the Django app
# dockerk run -p 8000:8000 msg_app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
