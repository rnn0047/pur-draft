import sys
#resolve env issues when gunicorn is invoked as service
sys.path.append("/home/ec2-user/tiger-styles")
sys.path.append("/home/ec2-user/tiger-styles/xform")
sys.path.append("/home/ec2-user/tiger-styles/xform/src")
sys.path.append("/home/ec2-user/tiger-styles/tools")
from app import app

if __name__ == "__main__":
    app.run()
