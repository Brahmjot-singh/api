
from django.contrib import admin
from django.urls import path
from . import views
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
import base64

# Encryption
def encrypt_url(url):
    key = b'your_secret_key_here'  # Should be 32 bytes for AES-256
    iv = b'your_iv_here'  # Should be 16 bytes for AES
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_url = encryptor.update(url.encode()) + encryptor.finalize()
    
    return base64.urlsafe_b64encode(iv + encrypted_url).decode()

# Decryption
def decrypt_url(encrypted_url):
    key = b'your_secret_key_here'
    encrypted_data = base64.urlsafe_b64decode(encrypted_url.encode())
    iv = encrypted_data[:16]
    data = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_url = decryptor.update(data) + decryptor.finalize()
    
    return decrypted_url.decode()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ops/login/', views.ops_login),
    path('ops/upload/', views.ops_upload_file),
    path('client/signup/', views.client_signup),
    path('client/verify_email/<str:token>/', views.verify_email),
    path('client/login/', views.client_login),
    path('client/download/<str:filename>/', views.client_download_file),
    path('client/list_files/', views.client_list_files),
]