
from django.urls import path
from blog_app import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list" ),
    path("draft-list", views.DraftsListView.as_view(), name="draft-list" ),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("draft-detail/<int:pk>/", views.DraftDetailView.as_view(), name="draft-detail"),
    path("post-delete/<int:pk>/", views.PostDeleteView.as_view(),name="post-delete"),

    path("draft-publish/<int:pk>/", views.DraftPublishView.as_view(),name="draft-publish"),
    path("post-create",views.PostCreateView.as_view(), name="post-create"), 
    path("post-update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
]