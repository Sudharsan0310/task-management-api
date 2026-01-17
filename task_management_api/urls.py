from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="""
        A comprehensive REST API for task management with user authentication,
        CRUD operations, filtering, search, and more.
        
        ## Authentication
        This API uses JWT (JSON Web Token) authentication.
        
        ### To authenticate:
        1. Register at POST /api/auth/register/ or Login at POST /api/auth/login/
        2. Copy the "access" token from the response
        3. Click the "Authorize" button above
        4. Enter: Bearer YOUR_ACCESS_TOKEN (with the word "Bearer" and a space)
        5. Click "Authorize" and "Close"
        6. Now you can use all protected endpoints!
        
        ## Features
        - User authentication and profile management
        - Task CRUD operations
        - Categories and tags
        - Task assignment
        - Comments and attachments
        - Advanced filtering and search
        - Pagination
        """,
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('tasks.urls')),

    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='api-root'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )