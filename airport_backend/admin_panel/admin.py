from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from airport_backend.users.models import CustomUser
from bookings.models import Booking, BookingLog
from .models import AdminActionLog
from locations.models import Airport, Lounge, LoungeSchedule, EntryCondition, Feature, GalleryImage
from .forms import BookingAnalyticsForm
from airport_backend.utils import send_telegram_notification 


class AdminActionLoggingMixin:
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        action = "обновлена" if change else "создана"
        AdminActionLog.objects.create(
            admin_user=request.user,
            action=f"Запись {obj} была {action} администратором {request.user.username}.")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        AdminActionLog.objects.create(
            admin_user=request.user,
            action=f"Запись {obj} была удалена администратором {request.user.username}.")


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('name', 'code', 'city', 'country')
    search_fields = ('name', 'code', 'city', 'country')
    list_filter = ('country',)


@admin.register(Lounge)
class LoungeAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('name', 'airport_id', 'terminal', 'base_price')
    search_fields = ('name', 'airport_id__name', 'terminal')
    list_filter = ('airport_id',)


@admin.register(LoungeSchedule)
class LoungeScheduleAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('lounge', 'valid_from_time',
                    'valid_till_time', 'valid_days')
    list_filter = ('lounge',)


@admin.register(EntryCondition)
class EntryConditionAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('lounge', 'type', 'cost', 'max_stay_duration')
    list_filter = ('lounge', 'type')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('lounge', 'name')
    search_fields = ('name',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('lounge', 'image_url')
    search_fields = ('lounge__name',)


@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('admin_user', 'action', 'timestamp')
    search_fields = ('admin_user__username', 'action')
    list_filter = ('timestamp',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    # change_list_template = 'admin/booking_analytics.html'
    list_display = ('id', 'user', 'lounge', 'status', 'first_name', 'last_name', 'guest_count', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'lounge__name', 'last_name')
    actions = ['confirm_booking']

    @admin.action(description='Подтвердить выбранные бронирования')
    def confirm_booking(self, request, queryset):
        for booking in queryset:
            booking.status = 'confirmed'
            booking.save()
            AdminActionLog.objects.create(
                admin_user=request.user,
                action=f"Бронирование #{booking.id} было подтверждено администратором {request.user.username}."
            )
            send_telegram_notification(booking.user.telegram_id, f"Ваше бронирование бизнес-зала {booking.lounge.name} подтверждено.")



@admin.register(BookingLog)
class BookingLogAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('booking_id', 'timestamp')
    list_filter = ('timestamp',)


# Добавление новых администраторов
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff',)
    actions = ['make_admin']

    @admin.action(description='Назначить выбранных пользователей администраторами')
    def make_admin(self, request, queryset):
        queryset.update(is_staff=True, is_superuser=True)
        for user in queryset:
            AdminActionLog.objects.create(
                admin_user=request.user,
                action=f"Пользователь {user.username} назначен администратором.")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminActionLoggingMixin):
    change_list_template = 'admin/booking_analytics.html'
    list_display = ('id', 'user', 'lounge', 'status', 'first_name',
                    'last_name', 'guest_count', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'lounge__name', 'last_name')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_site.admin_view(self.analytics_view),
                 name='booking-analytics'),
        ]
        return custom_urls + urls

    def analytics_view(self, request):
        form = BookingAnalyticsForm(request.POST or None)
        analytics_data = None

        if form.is_valid():
            analytics_data = form.get_analytics()
            AdminActionLog.objects.create(
                admin_user=request.user,
                action=f"Администратор {request.user.username} запросил аналитику.")

        return TemplateResponse(request, 'admin/booking_analytics.html', {
            'form': form,
            'analytics_data': analytics_data,
        })
