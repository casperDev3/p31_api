from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*4(ib1)cugp4^30bi(*e%5%8cd0$x$tw9*9cl0elcuqd0zk9re'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'daphne',  # для підтримки ASGI та WebSocket
    # themes apps
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "unfold.contrib.location_field",  # optional, if django-location-field package is used
    "unfold.contrib.constance",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed apps
    'graphene_django',
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    # custom apps
    'news',
    'authentication',
    'factory',
    'static',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # 'CONFIG': {
        #     'hosts': [('127.0.0.1', 6379)],
        # }
    },
}

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False, # Не оновлювати refresh токени при кожному запиті на оновлення
    'BLACKLIST_AFTER_ROTATION': False, # Не додавати старі refresh токени до чорного списку після оновлення
    'UPDATE_LAST_LOGIN': True, # Оновлювати поле last_login користувача при кожному успішному запиті на отримання access токена
}


AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHENE = {
    'SCHEMA': 'core.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}



GRAPHQL_JWT = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

LIQPAY_PUBLIC_KEY = 'sandbox_i96919624816'
LIQPAY_PRIVATE_KEY = 'sandbox_uzxTKC2NscjtlNXs4giwqxN28g6kmb66mI08kBh5'

from core.dashboard import get_dashboard_stats, get_activity_chart, get_categories_chart

UNFOLD = {
    'SITE_TITLE': 'Адмін-панель Новин',
    'SITE_HEADER': 'Адмін-панель Новин',
    'SITE_SYMBOL': 'newspaper',
    'SHOW_HISTORY': True,
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",  # Основний колір (Purple)
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    'DASHBOARD': {
        'widgets': [
            {
                'wrapper_class': 'col-span-full', # Статистика на всю ширину зверху
                'widget_class': 'unfold.widgets.WidgetStatsControl',
                'args': {
                    'stats': get_dashboard_stats,
                },
            },
            {
                'wrapper_class': 'col-span-full md:col-span-6 lg:col-span-8', # Великий графік зліва
                'widget_class': 'unfold.widgets.WidgetChartBar',
                'args': lambda request: {
                    'title': 'Динаміка публікацій',
                    'subtitle': 'Кількість доданих новин по місяцях',
                    'data': get_activity_chart(request),
                },
            },
            {
                'wrapper_class': 'col-span-full md:col-span-6 lg:col-span-4', # Круговий або лінійний графік справа
                'widget_class': 'unfold.widgets.WidgetChartLine',
                'args': lambda request: {
                    'title': 'Аналітика категорій',
                    'subtitle': 'Популярність рубрик',
                    'data': get_categories_chart(request),
                },
            },
        ],
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': True,
        'navigation': [
            {
                'title': 'Головна',
                'separator': True,
                'items': [
                    {
                        'title': 'Дашборд',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Новини',
                'separator': True,
                'items': [
                    {
                        'title': 'Статті',
                        'icon': 'article',
                        'link': reverse_lazy('admin:news_article_changelist'),
                    },
                    {
                        'title': 'Категорії',
                        'icon': 'category',
                        'link': reverse_lazy('admin:news_category_changelist'),
                    },
                    {
                        'title': 'Теги',
                        'icon': 'sell',
                        'link': reverse_lazy('admin:news_tag_changelist'),
                    },
                ],
            },
            {
                'title': 'Користувачі та групи',
                'separator': True,
                'items': [
                    {
                        'title': 'Користувачі',
                        'icon': 'person',
                        'link': reverse_lazy('admin:auth_user_changelist'),
                    },
                    {
                        'title': 'Групи',
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                    },
                ],
            },
        ],
    },

}


