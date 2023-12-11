# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Python and unbuffered mode
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and start virtual environment
RUN python -m venv venv

# Install any needed packages specified in requirements.txt
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"  

# Make port 8000 available to the world outside this container
EXPOSE 8000

CMD ["venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "--env", "DJANGO_SETTINGS_MODULE=donation_platform.settings", "donation_platform.wsgi:application"]
# CMD ["gunicorn", "DJANGO_SETTINGS_MODULE=donation_platform.settings", "donation_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
