from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UsuarioForm
from django.contrib.auth.models import Permission


def home(request):
    return render(request, 'index.html')

@login_required
def perfil(request):
    return render(request, 'perfil.html')

def autenticar(request):
    if request.POST:
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            return render(request, 'registration\login.html')
    else:
        return render(request, 'registration\login.html')
    
def desconectar(request):
    logout(request)
    return redirect('home')

def registro(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        usuario = form.save()
        
        tipo = request.POST['perfil']
        if tipo=='professor':
            permissao = Permission.objects.get(codename='professor')
            usuario.user_permissions.add(permissao)
            usuario.save()
        elif tipo=='aluno':
            permissao = Permission.objects.get(codename='aluno')
            usuario.user_permissions.add(permissao)
            usuario.save()
        elif tipo=='admin':
            usuario.is_superuser = True
            usuario.save()

        return redirect('login')
    contexto = {
        'form': form
    }
    return render(request, 'registro.html', contexto)

@login_required
@permission_required('core.professor')
def diarios(request):
    return render(request, 'diarios.html')


def notas(request):
    if request.user.has_perm('core.professor') or request.user.has_perm('core.aluno'):
        return render (request, 'notas.html')
    else:
        return redirect(request, 'login')