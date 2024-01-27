# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables for your Django app
ENV DJANGO_SETTINGS_MODULE=settings.development

# Create and set the working directory
WORKDIR /opt/app/lifeapi

# Copy your Django app code into the container
COPY . .

# Install any dependencies from requirements.txt
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]