# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt file into the container
COPY requirements.txt /app/

# Install the required dependencies. This layer will be cached as long as requirements.txt doesn't change.
RUN pip install -r requirements.txt
RUN pip install --upgrade 'transformers==4.24.0'

# Now copy the rest of your application files (this happens after dependencies are installed)
COPY . /app/

# Make port 8888 available to the outside world
EXPOSE 8888

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
