from waitress import serve
from day16.wsgi import application

from whitenoise import WhiteNoise
import os

# 添加静态资源支持（staticfiles 是 collectstatic 后生成的）
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), 'staticfiles'))
serve(
    application,
    host='0.0.0.0',  # 公网可访问
    port=80,
    threads=8
)
