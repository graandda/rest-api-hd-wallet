# Generated by Django 4.0.4 on 2022-12-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0005_alter_addresses_wallet_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="walletdetaildump",
            name="chain_code",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="entropy",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="language",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="mnemonic",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="root_xprivate_key",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="root_xpublic_key",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="seed",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="semantic",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="strength",
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="xprivate_key",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="walletdetaildump",
            name="xpublic_key",
            field=models.CharField(max_length=256),
        ),
    ]