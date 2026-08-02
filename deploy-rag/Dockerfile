# Use te AWS base image for python 3.12
FROM public.ecr.aws/lambda/python:3.12

# Install build-essential compiler and tools
RUN microdnf update -y && microdnf install -y gcc-c++ make

# COPY the requirements.txt file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the libs in requirements.txt
RUN pip install -r requirements.txt

# COPY pdf file
COPY manual.pdf ${LAMBDA_TASK_ROOT}/manual.pdf

# COPY the function code
COPY naiveRAG.py ${LAMBDA_TASK_ROOT}

# Set permission to make the file executable
RUN chmod +x naiveRAG.py

# Set CMD to your handler
CMD ["naiveRAG.lambda_handler"]