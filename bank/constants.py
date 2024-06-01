from django.db.models import TextChoices


class BankCodes(TextChoices):
    american_express = ("american_express", "American Express")
    banorte = ("banorte", "Banorte")
    banco_azteca = ("banco_azteca", "Banco Azteca")
    hsbc = ("hsbc", "Hsbc")
    banca_coppel = ("banca_coppel", "Banca Coppel")
    invex_banco = ("invex_banco", "INVEX Banco")
    bbva_bancomer = ("bbva_bancomer", "BBVA Bancomer")
    konfio_red_amigo_dal = ("konfio_red_amigo_dal", "Konfio Red Amigo DAL")
    citibanamex = ("citibanamex", "CitiBanamex")
    scotiabank = ("scotiabank", "Scotiabank")
    santander = ("santander", "Santander")
    banco_bajio = ("banco_bajio", "Banco Bajío")
    inbursa = ("inbursa", "Inbursa")
