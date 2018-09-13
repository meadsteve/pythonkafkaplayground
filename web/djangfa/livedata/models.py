from django.db import models


class RandomRun(models.Model):
    run_id = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"Random run: {self.run_id}"

class RandomEntry(models.Model):
    random_run = models.ForeignKey(RandomRun, on_delete=models.CASCADE, to_field='run_id')
    payload = models.CharField(max_length=200)