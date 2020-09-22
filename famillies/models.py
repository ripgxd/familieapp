from django.contrib.gis.db import models


class Surname(models.Model):
    surname = models.CharField(unique=True, max_length=100, verbose_name='прізвище')

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = "Прізвище"
        verbose_name_plural = "Прізвища"


class RelationType(models.Model):
    relation = models.CharField(unique=True, max_length=100, verbose_name='відношення')

    def __str__(self):
        return self.relation

    class Meta:
        verbose_name = "відношення родича"
        verbose_name_plural = "Відношення родичів"


class FamillieList(models.Model):
    surname = models.ForeignKey(Surname, on_delete=models.CASCADE, verbose_name='прізвище', db_index=True)
    relation = models.ForeignKey(RelationType, on_delete=models.CASCADE, verbose_name='відношення', db_index=True)
    name = models.CharField(max_length=100, verbose_name='ім\'я')
    date = models.DateField(verbose_name='вік')
    address = models.CharField(max_length=200, db_index=True)
    point = models.PointField(geography=True, default='POINT(0.0 0.0)')

    @property
    def list_of_coords(self):
        return [self.point.y, self.point.x]

    class Meta:
        verbose_name = "Родич"
        verbose_name_plural = "Родичі"
