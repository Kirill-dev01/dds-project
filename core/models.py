from django.db import models
from django.utils import timezone

# --- Dictionaries (Справочники) ---


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    # A Category is linked to a Type (e.g., "Marketing" is a "Withdrawal" type)
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name="categories", verbose_name="Тип")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # A category name should be unique for its type
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подкатегория")
    # A SubCategory is linked to a Category (e.g., "Avito" is in the "Marketing" category)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="subcategories", verbose_name="Категория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        # A subcategory name should be unique for its category
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name

# --- Main Transaction Model ---


class Transaction(models.Model):
    created_date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(
        Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма (руб.)")
    comment = models.TextField(
        blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        ordering = ['-created_date']
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"Транзакция от {self.created_date.strftime('%d.%m.%Y')} на сумму {self.amount}"
