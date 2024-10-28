# Use official Python image
FROM python:3.10

# Set environment variables for Flask
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Install npm and necessary packages (for running Tailwind CSS commands)
RUN apt-get update && apt-get install -y nodejs npm
COPY app/package.json package.json
RUN npm install

# Expose Flask port
EXPOSE 8000

# Command to run on container start
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000", "--debug"]