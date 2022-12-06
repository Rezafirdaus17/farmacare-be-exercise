import uuid as uuid

from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField()
    identifier = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pokemon"


class PokemonArena(models.Model):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pokemon_arena"

    def __str__(self):
        return str(self.uuid)


class PokemonMatch(models.Model):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, db_index=True, unique=True)
    pokemon = models.ForeignKey(
        Pokemon, related_name="matches", on_delete=models.CASCADE
    )
    arena = models.ForeignKey(
        PokemonArena, related_name="arenas", on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField()
    is_win = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pokemon_match"
        ordering = ["-is_win", "-score"]
