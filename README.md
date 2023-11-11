How to zip:
```
pip install --target ./ <boto3>

# or 

pip install --platform manylinux2014_x86_64 --target=package --implementation cp --python-version 3.11 --only-binary=:all: --upgrade --target ./ <package>

Compress-Archive -Path ./* -DestinationPath deployment.zip -Force
```