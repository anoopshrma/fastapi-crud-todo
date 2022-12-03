# Start from the official Python image 
FROM python:3.8 

# Set the working directory 
WORKDIR /app 

# Copy the requirements file 
COPY requirements.txt . 

# Install the requirements 
RUN pip install -r requirements.txt 

# Copy the application code 
COPY . . 

# Expose the application's port 
EXPOSE 8000 

# Run the application 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]