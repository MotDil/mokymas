from django.db import models

# Create your models here.

class Paslauga(models.Model):
    pavadinimas = models.CharField('PASLAUGA', max_length=200, unique=True, help_text='Įveskite paslaugos pavadinimą')
    kaina = models.DecimalField('PASLAUGOS_KAINA', max_digits=10, decimal_places=2, help_text='Įveskite paslaugos kainą')

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'
        ordering = ['pavadinimas']

    def __str__(self):
        return f"Paslauga: {self.pavadinimas} - {self.kaina} EUR"

class AutomobilioModelis(models.Model):
    metai = models.CharField('AUTOMOBILIO_METAI', max_length=4, help_text='Įveskite automobilio pagaminimo metus')
    marke = models.CharField('AUTOMOBILIO_MARKĖ', max_length=20, help_text='Įveskite automobilio markę')
    modelis = models.CharField('AUTOMOBILIO_MODELIS', max_length=20, help_text='Įveskite automobilio modelį pvz. A4, M3, F10, G30, GS, LS')
    variklis = models.CharField('VARIKLIS', max_length=50, help_text='Įveskite varikio parametrus: litražą, kilovatus, kuro tipą')

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilių modeliai'
        ordering = ['marke']

    def __str__(self):
        return f"Automobilio modelis: {self.metai}, {self.marke}, {self.modelis}, {self.variklis}"

class AutomobilisKlientas(models.Model):
    valstybinis_nr = models.CharField('VALSTYBINIS_NUMERIS', max_length=15, unique=True, help_text='Įveskite automobilio valstybinius numerius')
    vin_kodas = models.CharField('VIN_KODAS', max_length=100, unique=True, help_text='Įveskite automobilio VIN kodą')
    klientas = models.CharField('KLIENTO_VARDAS_PAVARDĖ',max_length=50, help_text='Įveskite kliento vardą ir pavardę')
    modelis = models.ForeignKey(AutomobilioModelis, on_delete=models.CASCADE, help_text='Pasirinkite automobilį')

    class Meta:
        verbose_name = 'Kliento automobilis'
        verbose_name_plural = 'Klientų automobiliai'
        ordering = ['klientas']

    def __str__(self):
        return f"Klientas: {self.klientas}, {self.valstybinis_nr}, {self.vin_kodas}"

class Uzsakymas(models.Model):
    data = models.DateField('UŽSAKYMO_DATA', help_text='Įveskite užsakymo datą')
    automobilis = models.ForeignKey(AutomobilisKlientas, on_delete=models.CASCADE, help_text='Pasirinkite kliento automobilį')
    PASIRINKIMAI_STATUS = [
        ('L', 'Laukiama'),
        ('V', 'Vykdoma'),
        ('A', 'Atlikta'),
    ]
    statusas = models.CharField(max_length=10, choices=PASIRINKIMAI_STATUS, default='L', help_text='Pasirinkite užsakymo statusą',  blank=True)


    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'
        ordering = ['data']

    def __str__(self):
        return f"{self.automobilis}, {self.data}"

class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE, help_text='Įveskite užsakymo ID')
    paslauga = models.ForeignKey(Paslauga, on_delete=models.CASCADE, help_text='Pasirinkite paslaugas')
    kiekis = models.IntegerField('KIEKIS', help_text='Įveskite paslaugų kiekį')

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'

    def __str__(self):
        return f"Paslauga: {self.uzsakymas} {self.paslauga} - {self.kiekis} vnt."

