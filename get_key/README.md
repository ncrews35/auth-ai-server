# Get Key

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd get_key
   ```

4. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

## Deployment

1. Build docker image

   ``` bash
   $ docker build --platform linux/arm64 -t get_key_image .
   ```

2. Run docker image

   ```bash
   $ docker run --platform linux/arm64 --env-file=.env -p 9000:8080 --name auth_container get_key_image
   ```

3. Test function

   ```bash
   $ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d ''
   ```

4. Login to aws ecr

   ```bash
   $ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 297535061769.dkr.ecr.us-east-1.amazonaws.com
   ```

5. Create docker tag

   ```bash
   $ docker tag  get_key_image:latest 297535061769.dkr.ecr.us-east-1.amazonaws.com/get_key_image:latest
   ```

6. Push docker image

   ```bash
   $ docker push 297535061769.dkr.ecr.us-east-1.amazonaws.com/get_key_image:latest
   ```

For more information on deployments, refer to the [deployment docs](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-create).