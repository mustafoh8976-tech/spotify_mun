from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *

AUDIO_EXT = ('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac', '.opus')
AUDIO_ERROR = "Загрузите аудиофайл (mp3, wav, ogg, m4a, flac)"


def is_audio(f):
    return (f.content_type or '').startswith('audio/') or f.name.lower().endswith(AUDIO_EXT)


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not username or not email or not password or not password2:
            return render(request, "register.html", context={"error": "Заполните все поля"},)
        if password != password2:
            return render(request, "register.html", context={"error": "Пароли не совпадают"},)
        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", context={"error": "Такой username уже есть"},)
        if CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", context={"error": "Такой email уже есть"},)

        CustomUser.objects.create_user(username=username, email=email, password=password)
        return redirect("login")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "login.html", context={"error": "Заполните все поля"},)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", context={"error": "Неверный username или пароль"},)

        login(request, user)
        return redirect("musice_list")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def musice_list_view(request):
    musics = Musice.objects.all()
    return render(request, "musice_list.html", context={"musics": musics})


@login_required
def musice_create_view(request):
    if request.method == "POST":
        name_music = request.POST.get("name_music")
        musice = request.FILES.get("musice")

        if not name_music or not musice:
            return render(request, "musice_create.html", context={"error": "Заполните все поля"},)
        if not is_audio(musice):
            return render(request, "musice_create.html", context={"error": AUDIO_ERROR},)

        Musice.objects.create(name_music=name_music, musice=musice, user_id=request.user)
        return redirect("musice_list")
    return render(request, "musice_create.html")


@login_required
def musice_update_view(request, id):
    music = get_object_or_404(Musice, id=id, user_id=request.user)
    if request.method == "POST":
        name_music = request.POST.get("name_music")
        musice = request.FILES.get("musice")

        if not name_music:
            return render(request, "musice_update.html", context={"music": music, "error": "Введите название"},)

        if musice and not is_audio(musice):
            return render(request, "musice_update.html", context={"music": music, "error": AUDIO_ERROR},)

        music.name_music = name_music
        if musice:
            music.musice = musice
        music.save()
        return redirect("musice_list")
    return render(request, "musice_update.html", context={"music": music})


@login_required
@require_POST
def musice_delete_view(request, id):
    music = get_object_or_404(Musice, id=id, user_id=request.user)
    music.delete()
    return redirect("musice_list")



@login_required
def genere_list_view(request):
    generes = Genere.objects.all()
    return render(request, "genere_list.html", context={"generes": generes})


@login_required
def genere_create_view(request):
    if request.method == "POST":
        name_g = request.POST.get("name_g")

        if not name_g:
            return render(request, "genere_create.html", context={"error": "Введите название жанра"},)

        Genere.objects.create(name_g=name_g)
        return redirect("genere_list")
    return render(request, "genere_create.html")


@login_required
def genere_update_view(request, id):
    genere = get_object_or_404(Genere, id=id)
    if request.method == "POST":
        name_g = request.POST.get("name_g")

        if not name_g:
            return render(request, "genere_update.html", context={"genere": genere, "error": "Введите название жанра"},)

        genere.name_g = name_g
        genere.save()
        return redirect("genere_list")
    return render(request, "genere_update.html", context={"genere": genere})


@login_required
@require_POST
def genere_delete_view(request, id):
    genere = get_object_or_404(Genere, id=id)
    genere.delete()
    return redirect("genere_list")


@login_required
def alsbome_list_view(request):
    alsbomes = Alsbome.objects.all()
    return render(request, "alsbome_list.html", context={"alsbomes": alsbomes})


@login_required
def alsbome_create_view(request):
    if request.method == "POST":
        name_als = request.POST.get("name_als")

        if not name_als:
            return render(request, "alsbome_create.html", context={"error": "Введите название альбома"},)

        Alsbome.objects.create(name_als=name_als)
        return redirect("alsbome_list")
    return render(request, "alsbome_create.html")


@login_required
def alsbome_update_view(request, id):
    alsbome = get_object_or_404(Alsbome, id=id)
    if request.method == "POST":
        name_als = request.POST.get("name_als")

        if not name_als:
            return render(request, "alsbome_update.html", context={"alsbome": alsbome, "error": "Введите название альбома"},)

        alsbome.name_als = name_als
        alsbome.save()
        return redirect("alsbome_list")
    return render(request, "alsbome_update.html", context={"alsbome": alsbome})


@login_required
@require_POST
def alsbome_delete_view(request, id):
    alsbome = get_object_or_404(Alsbome, id=id)
    alsbome.delete()
    return redirect("alsbome_list")


@login_required
def like_list_view(request):
    likes = Like.objects.filter(user_id=request.user)
    return render(request, "like_list.html", context={"likes": likes})


@login_required
@require_POST
def like_create_view(request):
    Like.objects.create(user_id=request.user)
    return redirect("like_list")


@login_required
@require_POST
def like_delete_view(request, id):
    like = get_object_or_404(Like, id=id, user_id=request.user)
    like.delete()
    return redirect("like_list")
