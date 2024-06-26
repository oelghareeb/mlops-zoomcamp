FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# Update pip and install pipenv
RUN pip install -U pip && pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock for pipenv installation
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Copy your Python script into the Docker image
COPY starter.py .

# Command to run the script with arguments passed from docker run
ENTRYPOINT ["python", "starter.py"]
CMD ["2023", "5"]
