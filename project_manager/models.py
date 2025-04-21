from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    # 'required' est implicite si 'blank=False' (défaut)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # pas de 'min_length' ici


def save(self, *args, **kwargs):
    """
        Surcharge de la méthode `save()` du modèle Django.

        Avant d'enregistrer un objet User en base de données,
        cette méthode hache le mot de passe en utilisant la fonction `make_password`
        de Django. Cela permet de sécuriser le mot de passe en évitant de le stocker en clair.

        Args:
            *args: Arguments positionnels standards pour la méthode save().
            **kwargs: Arguments nommés standards pour la méthode save().
        """
    # Hacher le mot de passe avant sauvegarde
    self.password = make_password(self.password)
    super().save(*args, **kwargs)

    def __str__(self):
        """
     Représentation texte de l'objet User.

     Retourne le nom d'utilisateur (username), utile notamment
     dans l'interface d'administration Django ou pour le debug.

     Returns:
         str: Le nom d'utilisateur de l'utilisateur.
     """
    return self.username


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True,
                             default="Untitled Project")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title
