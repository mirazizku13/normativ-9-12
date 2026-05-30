from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy


from accounts.models import UserRole
from accounts.utils import login_required_custom, is_poster, is_moderator
from .models import Game, Status
from .forms import GameModelForm
from common.service import thread_send_mail


def game_list(request):
    search = request.GET.get('search','')
    page = request.GET.get('page')
    games = Game.objects.all()
    if request.user.is_authenticated and request.user.role == UserRole.Poster:
        games = games.filter(created_by=request.user)
    elif request.user.is_authenticated and request.user.role == UserRole.Moderator:
        games = games.filter(status=Status.DRAFT)
    else:
        games = games.filter(status=Status.PUBLISHED)
    if search:
        games = games.filter(title__icontains=search)

    paginator = Paginator(games, 5)
    games = paginator.get_page(page)
    return render(request, 'games/game_list.html', {'games': games, 'search': search, 'page': page, 'UserRole': UserRole})

def game_detail(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request, 'games/game_detail.html', {'game': game, 'UserRole': UserRole})

# @is_poster
# def game_create(request):
#     if request.method == 'POST':
#         form = GameModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('games:game_list')
#     else:
#         form = GameModelForm()
#     return render(request, 'games/game_create.html', {'form': form})


@is_poster
def game_create(request):
    form = GameModelForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
            return redirect('games:game_list')
    return render(request, 'games/game_create.html', {'form': form})

@is_poster
def game_update(request, id):
    game = get_object_or_404(Game, id=id)
    if request.method == 'POST':
        form = GameModelForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('games:game_list')
    else:
        form = GameModelForm(instance=game)
    return render(request, 'games/game_create.html', {'form': form})
@is_poster
def game_delete(request, id):
    game = get_object_or_404(Game, id=id)
    if request.method == 'POST':
        game.delete()
        return redirect('games:game_list')
    return render(request, 'games/game_confirm_delete.html', {'game': game})

# @is_moderator
# def game_published(request, pk=None):
#     game = Game.objects.filter(id=pk).first()
#     game.status = Status.PUBLISHED
#     game.save()
#     return redirect('games:game_list')

@is_moderator
def game_published(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.status = Status.PUBLISHED
    game.save()
    return redirect('games:game_list')


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    queryset = Game.objects.all().order_by('-id')
    paginate_by = 5

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['search'] = \
            self.request.GET.get('search', '')
        return context

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        if self.request.user.is_authenticated and self.request.user.role == UserRole.Poster:
            games = self.queryset.filter(created_by=self.request.user)
        elif self.request.user.is_authenticated and self.request.user.role == UserRole.Moderator:
            games = self.queryset.filter(status=Status.DRAFT)
        else:
            games = self.queryset.filter(status=Status.PUBLISHED)

        if search:
            games = games.filter(title__icontains=search)

        return games

class GamesCreateView(PermissionRequiredMixin, CreateView):
    model = Game
    template_name = 'games/game_create.html'
    form_class = GameModelForm
    success_url = reverse_lazy('games:game_list')
    permission_required = 'games.add_game'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GamesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Game
    template_name = 'games/game_create.html'
    form_class = GameModelForm
    permission_required = 'games.change_game'
    success_url = reverse_lazy('games:game_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class GamesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Game
    template_name = 'games/game_confirm_delete.html'
    permission_required = 'games.delete_game'
    success_url = reverse_lazy('games:game_list')
    pk_url_kwarg = 'pk'

class SendEmailView(View):

    template_name = 'games/send_masage.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            thread_send_mail(email, subject, message)
            print(f"Email {email} ga {message} yuborildi!")
            return redirect('games:game_list')

        except Exception as e:
            return HttpResponse(f"Error: {e}")


class SendFileToEmailView(View):
    template_name = 'games/send_massage.html'
    def get(self, request):
        pass