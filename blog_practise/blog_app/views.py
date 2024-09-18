from django.shortcuts import render

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from blog_app.forms import PostForm
from blog_app.models import Post
from django.contrib.auth.decorators import (
    login_required,
)  #: This mixin ensures that the user must be logged in to access the view. If a user who

# is not authenticated tries to access this view, they will be redirected to the login page.
from django.utils import timezone

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
    DeleteView,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"

    def get_queryset(Self):
        posts = Post.objects.filter(published_at__isnull=False).order_by(
            "-published_at"
        )
        return posts


# class PostDetailView(LoginRequiredMixin, DetailView):
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset


class DraftsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "posts"

    def get_queryset(Self):
        posts = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
        return posts


class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "draft_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        messages.success(self.request, "Post was Deleted Successfully")
        return super().form_valid(form)


class DraftPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.published_at = timezone.now()
        post.save()
        messages.success(request, "Post was Published Successfully")
        return redirect("post-detail", pk)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    # success_url = reverse_lazy("post-list")

    def get_success_url(self) -> str:
        return reverse_lazy("draft-detail", kwargs={"pk": self.object.pk})

    # get_success_url: This method is overridden to define the URL to which the user should be redirected after successfully creating a Post.

    def form_valid(self, form):
        form.instance.author = (
            self.request.user
        )  # author vane table jasle naya blog banayeko tesko name set huncha
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        # Redirect based on the `published_at` field
        if post.published_at:
            return reverse_lazy("post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("draft-detail", kwargs={"pk": post.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Post updated successfully!')
        return response
    # Optionally, if you need custom queryset filtering, you can override get_queryset like this:
    # def get_queryset(self):
    #     return Post.objects.filter(user=self.request.user)  # Example filter by user


# The get_queryset method is intended to return the queryset that will be used to retrieve the object that needs to be updated. 
# However, in your code, this method is implemented to return a URL rather than a queryset, which is not the typical use of get_queryset.Here’s what’s happening:

# self.get_object(): Retrieves the Post object that is being updated.
# post.published_at: Checks if the post has a published_at timestamp.
# If post.published_at is present, it returns the URL for the post detail view ("post-detail").
# If post.published_at is not present, it returns the URL for the draft detail view ("draft-detail").